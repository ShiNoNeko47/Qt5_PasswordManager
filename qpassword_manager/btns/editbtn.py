'''EditBtn class'''

import logging
import requests
from PyQt5.QtWidgets import QPushButton
from qpassword_manager.conf.connectorconfig import Config


class EditBtn(QPushButton):
    '''Button that copies data from a row in table to line edits

    Attributes:
        row_id: id of the row to copy from database
        edit_btns: list of EditBtn objects in the table
        window: parent wondow (ManagePasswordsWindow)
        fernet: Fernet object used for decryption
    '''

    def __init__(self, row_id, edit_btns, window):
        super().__init__()
        self.row_id = row_id
        self.edit_btns = edit_btns
        self.window = window
        self.fernet = self.window.fernet

        self.setText("+")
        self.clicked.connect(self.edit_row)

    def edit_row(self):
        '''Copies data from a row in table to line edits'''

        if self.text() == "+":
            for btn in self.edit_btns:
                btn.setText("+")

            self.setText("-")
            row = requests.post(
                Config.config()["host"],
                {"action": "get_row", "id": self.row_id},
                auth=(self.window.auth),
            ).json()
            logging.debug(self.row_id)
            self.window.new_website_le.setText(row["0"])
            self.window.new_username_le.setText(row["1"])
            password = self.fernet.decrypt(row["2"].encode()).decode()
            self.window.new_password_le.setText(password)
            self.window.re_new_password_le.setText(password)

        else:
            self.setText("+")
            self.window.reset_entries()
