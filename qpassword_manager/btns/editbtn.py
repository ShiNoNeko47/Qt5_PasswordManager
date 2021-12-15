from PyQt5.QtWidgets import QPushButton
import requests
import logging
from qpassword_manager.conf.connectorconfig import Config


class Edit_btn(QPushButton):
    def __init__(self, rowId, edit_btns, window):
        super().__init__()
        self.rowId = rowId
        self.edit_btns = edit_btns
        self.w = window
        self.clicked.connect(self.edit_row)
        self.f = self.w.f
        self.setText("+")

    def edit_row(self):
        if self.text() == "+":
            for btn in self.edit_btns:
                btn.setText("+")

            self.setText("-")
            row = requests.post(
                Config.config()["host"],
                {"action": "get_row", "id": self.rowId},
                auth=(self.w.auth),
            ).json()
            logging.debug(self.rowId)
            self.w.newWebsite_le.setText(row["0"])
            self.w.newUsername_le.setText(row["1"])
            password = self.f.decrypt(row["2"].encode()).decode()
            self.w.newPassword_le.setText(password)
            self.w.reNewPassword_le.setText(password)

        else:
            self.setText("+")
            self.w.reset_entries()
