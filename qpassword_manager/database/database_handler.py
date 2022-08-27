"""This class handles all http requests"""

import os
import sqlite3
import requests
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

    def __init__(self, config) -> None:
        self.config = config

    @check_server
    def remove_from_database(self, row_id, auth) -> None:
        """Function for working with only one row in database"""

        if self.config["database_online"]:
            requests.post(
                url=self.config["url"] + "/remove_from_database",
                timeout=5,
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

    @check_server
    def get_entry(self, row_id, auth) -> list:
        """Function for working with only one row in database"""

        if self.config["database_online"]:
            return requests.post(
                url=self.config["url"] + "/get_entry",
                timeout=5,
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

    @check_server
    def get_all(self, auth) -> list:
        """Function for working with multiple rows in database"""

        if self.config["database_online"]:
            return requests.post(
                url=self.config["url"] + "/get_all",
                timeout=5,
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

    @check_server
    def get_entry_ids(self, auth) -> list:
        """Returns id value of every password in table"""

        if self.config["database_online"]:
            return requests.post(
                url=self.config["url"] + "/get_entry_ids",
                timeout=5,
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

    @check_server
    def add_to_database(self, website, username, password, auth) -> None:
        """Function for adding a password to database"""

        if self.config["database_online"]:
            requests.post(
                url=self.config["url"] + "/add_to_database",
                timeout=5,
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

    @check_server
    def register(self, username, email, master_key) -> str:
        """Function for adding a new user to database"""

        if self.config["database_online"]:
            return requests.post(
                url=self.config["url"] + "/register",
                timeout=5,
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

    @check_server
    def check_credentials(self, username, master_key) -> bool:
        """Function that returns user id if user-password combination exists"""

        if self.config["database_online"]:
            if requests.post(
                url=self.config["url"] + "/check_credentials",
                timeout=5,
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
