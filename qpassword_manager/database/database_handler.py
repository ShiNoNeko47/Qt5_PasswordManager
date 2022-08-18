"""This class handles all http requests"""

import os
import sqlite3
import requests
from qpassword_manager.conf.connectorconfig import Config
from qpassword_manager.messagebox import MessageBox


def check_server(func):
    """Wrapper that checks for exceptions"""

    def wrapper(*args):
        try:
            return func(*args)
        except Exception as exception:  # pylint: disable=broad-except
            messagebox = MessageBox(str(exception))
            messagebox.show()
            return None

    return wrapper


class DatabaseHandler:
    """This class handles all http requests"""

    @staticmethod
    @check_server
    def remove_from_database(row_id, auth) -> None:
        """Function for working with only one row in database"""

        if Config.config()["database_online"]:
            requests.post(
                url=Config.config()["url"] + "/remove_from_database",
                json={"id": row_id},
                auth=auth,
            )
            return

        conn = sqlite3.connect(auth[0] + ".db")
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
    @check_server
    def get_entry(row_id, auth) -> list:
        """Function for working with only one row in database"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/get_entry",
                json={"id": row_id},
                auth=auth,
            ).json()

        conn = sqlite3.connect(auth[0] + ".db")
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
    @check_server
    def get_all(auth) -> list:
        """Function for working with multiple rows in database"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/get_all",
                auth=auth,
            ).json()

        conn = sqlite3.connect(auth[0] + ".db")
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
    @check_server
    def get_entry_ids(auth) -> list:
        """Returns id value of every password in table"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/get_entry_ids",
                auth=auth,
            ).json()

        conn = sqlite3.connect(auth[0] + ".db")
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
    @check_server
    def add_to_database(website, username, password, auth) -> None:
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
            return

        conn = sqlite3.connect(auth[0] + ".db")
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
        return

    @staticmethod
    @check_server
    def register(username, email, master_key) -> str:
        """Function for adding a new user to database"""

        if Config.config()["database_online"]:
            return requests.post(
                url=Config.config()["url"] + "/register",
                json={
                    "username": username,
                    "email": email,
                    "password": master_key,
                },
            ).text

        if os.path.exists(username + ".db"):
            return "Username already taken"

        conn = sqlite3.connect(username + ".db")
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

        return "Registration successfull!"

    @staticmethod
    @check_server
    def check_credentials(username, master_key) -> bool:
        """Function that returns user id if user-password combination exists"""

        if Config.config()["database_online"]:
            if requests.post(
                url=Config.config()["url"] + "/check_credentials",
                auth=(
                    username,
                    master_key,
                ),
            ).text:
                return True

        elif os.path.exists(username + ".db"):
            conn = sqlite3.connect(username + ".db")
            cursor = conn.cursor()
            cursor.execute("select password from passwords where (id = 1)")
            master_key_db = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            if master_key == master_key_db:
                return True

        messagebox = MessageBox("Wrong username or password!")
        messagebox.show()
        return False
