"""This class handles all http requests"""

import os
import sqlite3
import requests
from qpassword_manager.conf.connectorconfig import Config


class DatabaseHandler:
    """This class handles all http requests"""

    @staticmethod
    def json_parser(data):
        """Parses requests json into list"""

        data_list = []
        for row in data:
            data_list.append([row[x] for j, x in enumerate(row) if j % 2])
        return data_list

    @staticmethod
    def delete_row(row_id, auth):
        """Function for working with only one row in database"""

        if Config.config()["database_online"]:
            requests.post(
                data={"action": "delete", "id": row_id},
                auth=auth,
                **Config.config()["host"]
            )
            return

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            f"""delete
                from passwords
                where (id = {row_id[0][0]})"""
        )
        conn.commit()
        cursor.close()
        conn.close()
        return

    @staticmethod
    def get_row(row_id, auth):
        """Function for working with only one row in database"""

        if Config.config()["database_online"]:
            return DatabaseHandler.json_parser(
                [requests.post(
                    data={"action": "get_row", "id": row_id},
                    auth=auth,
                    **Config.config()["host"]
                ).json()])[0]

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            f"""select website, username, password
               from passwords
               where (id = {row_id[0]})"""
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def create_table(auth):
        """Function for working with multiple rows in database"""

        if Config.config()["database_online"]:
            return DatabaseHandler.json_parser(
                requests.post(
                    data={"action": "create_table"},
                    auth=auth,
                    **Config.config()["host"]
                ).json())

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
                data={"action": "get_pass_ids"},
                auth=auth,
                **Config.config()["host"]
            ).json()

        conn = sqlite3.connect(DatabaseHandler.get_database(auth[0]))
        cursor = conn.cursor()
        cursor.execute(
            """select id
               from passwords
               where (id > 1)"""
        )
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def add_to_database(password, username, website, auth):
        """Function for adding a password to database"""

        if Config.config()["database_online"]:
            requests.post(
                data={
                    "action": "add",
                    "password": password,
                    "username": username,
                    "website": website,
                },
                auth=auth,
                **Config.config()["host"],
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
                data={
                    "action": "new_user",
                    "user": username,
                    "master_key": master_key,
                },
                **Config.config()["host"],
            ).text
        if os.path.exists(os.path.join(__file__, username + ".db")):
            return "Duplicate entry"
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
                data={"action": "get_id"},
                auth=(
                    username,
                    master_key,
                ),
                **Config.config()["host"],
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
        return

    @staticmethod
    def get_database(username):
        """Returns database path in offline mode"""

        return os.path.join(os.path.dirname(__file__), username + ".db")
