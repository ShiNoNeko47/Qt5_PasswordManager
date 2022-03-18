from qpassword_manager.conf.connectorconfig import Config
import requests


class Database_handler():
    online = Config.config()["database_online"]

    def action_row(action, row_id, auth):
        return requests.post(
            data={"action": action, "id": row_id},
            auth=(auth),
            **Config.config()["host"]).json()

    def action(action, auth):
        return requests.post(
            data={"action": action},
            auth=auth,
            **Config.config()["host"]).json()

    def add_to_database(data, auth):
        requests.post(
            data={
                "action": "add",
                "password": data[2],
                "username": data[1],
                "website": data[0],
            },
            auth=auth,
            **Config.config()["host"],
        )

    def add_user(username, master_key):
        return requests.post(
            data={
                "action": "new_user",
                "user": username,
                "master_key": master_key,
            },
            **Config.config()["host"]
        ).text

    def get_id(username, master_key):
        return requests.post(
            data={"action": "get_id"},
            auth=(
                username,
                master_key,
            ),
            **Config.config()["host"],
        ).text
