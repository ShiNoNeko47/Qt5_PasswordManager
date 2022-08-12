"""This class handles all http requests"""

import os
import sqlite3
from xdg import xdg_data_home
import requests
from qpassword_manager.conf.connectorconfig import Config


class DatabaseHandler:
    """This class handles all http requests"""

    @staticmethod
    def delete_row(row_id, auth):
        """Function for working with only one row in database"""

        if Config.config()["database_online"]:
            requests.post(
                url=Config.config()["url"] + "/remove_from_database",
                json={"id": row_id},
                auth=auth,
            )
            return

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            f"""delete
                from passwords
                where (id = {row_id})"""
        )
        conn.commit()
        cursor.close()
        conn.close()
        return

    @staticmethod
    def get_row(row_id, auth):
        """Function for working with only one row in database"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/get_entry",
                json={"id": row_id},
                auth=auth,
            ).json()

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            f"""select website, username, password
               from passwords
               where (id = {row_id})"""
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def create_table(auth):
        """Function for working with multiple rows in database"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/get_all",
                auth=auth,
            ).json()

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            """select website, username, password
               from passwords
               where (id > 1)"""
        )
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def get_row_ids(auth):
        """Returns id value of every password in table"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/get_entry_ids",
                auth=auth,
            ).json()

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            """select id
               from passwords
               where (id > 1)"""
        )
        data = cursor.fetchall()
        data = list(map(lambda x: x[0], data))
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def add_to_database(website, username, password, auth):
        """Function for adding a password to database"""

        if Config.config()["database_online"]:
            requests.post(
                url=Config.config()["url"] + "/add_to_database",
                json={
                    "website": website,
                    "username": username,
                    "password": password,
                },
                auth=auth,
            )
            return 0

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            f"""insert into passwords
               (website, username, password)
               values
               (\"{website}\",
               \"{username}\",
               \"{password}\")"""
        )
        conn.commit()
        cursor.close()
        conn.close()
        return 0

    @staticmethod
    def add_user(username, master_key):
        """Function for adding a new user to database"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/register",
                json={
                    "username": username,
                    "password": master_key,
                    "email": "email",
                },
            ).text

        if os.path.exists(
            os.path.join(xdg_data_home(), "qpassword_manager", username + ".db")
        ):
            return "Username already taken"

        conn = sqlite3.connect(DatabaseHandler.get_database(username))
        cursor = conn.cursor()
        cursor.execute(
            """create table passwords
               (id integer primary key autoincrement,
               website varchar(50),
               username varchar(50),
               password varchar(64))"""
        )
        cursor.execute(
            f"""insert into passwords
                (website, username, password)
                values
                (\"Master\",
                \"Key\",
                \"{master_key}\")"""
        )
        conn.commit()
        cursor.close()
        conn.close()

        return 0

    @staticmethod
    def get_id(username, master_key):
        """Function that returns user id if user-password combination exists"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/check_credentials",
                auth=(
                    username,
                    master_key,
                ),
            ).text

        if os.path.exists(DatabaseHandler.get_database(username)):
            conn = sqlite3.connect(DatabaseHandler.get_database(username))
            cursor = conn.cursor()
            cursor.execute("select password from passwords where (id = 1)")
            master_key_db = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            if master_key == master_key_db:
                return 1

        return 0

    @staticmethod
    def get_database(username):
        """Returns database path in offline mode"""

        directory = os.path.join(xdg_data_home(), "qpassword_manager")
        if not os.path.exists(directory):
            os.makedirs(directory)
        return os.path.join(
            xdg_data_home(), "qpassword_manager", username + ".db"
        )
