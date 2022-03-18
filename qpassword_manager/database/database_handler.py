"""This class handles all http requests"""

import requests
from qpassword_manager.conf.connectorconfig import Config


class DatabaseHandler:
    """This class handles all http requests"""

    online = Config.config()["database_online"]

    @staticmethod
    def action_row(action, row_id, auth):
        """Function for working with only one row in database"""

        return requests.post(
            data={"action": action, "id": row_id},
            auth=(auth),
            **Config.config()["host"],
        ).json()

    @staticmethod
    def action(action, auth):
        """Function for working with multiple rows in database"""

        return requests.post(
            data={"action": action}, auth=auth, **Config.config()["host"]
        ).json()

    @staticmethod
    def add_to_database(password, username, website, auth):
        """Function for adding a password to database"""

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

    @staticmethod
    def add_user(username, master_key):
        """Function for adding a new user to database"""

        return requests.post(
            data={
                "action": "new_user",
                "user": username,
                "master_key": master_key,
            },
            **Config.config()["host"],
        ).text

    @staticmethod
    def get_id(username, master_key):
        """Function that returns user id if user-password combination exists"""

        return requests.post(
            data={"action": "get_id"},
            auth=(
                username,
                master_key,
            ),
            **Config.config()["host"],
        ).text
