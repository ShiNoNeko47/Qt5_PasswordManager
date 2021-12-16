import logging
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.Qt import Qt
import requests
from Crypto.Hash import SHA256
from qpassword_manager.messagebox import MessageBox
from qpassword_manager.conf.connectorconfig import Config


class SetupWindow(QWidget):
    def __init__(self, window_main):
        super().__init__()

        self.window_main = window_main
        self.layout = QGridLayout()
        self.setWindowTitle("New user")
        self.setFixedHeight(150)
        self.setFixedWidth(600)

        self.username_setup_le = QLineEdit()
        self.username_setup_le.setPlaceholderText("New username")
        self.layout.addWidget(self.username_setup_le, 0, 0)

        self.key_setup_le = QLineEdit()
        self.key_setup_le.setEchoMode(QLineEdit.Password)
        self.key_setup_le.textChanged.connect(self.check_password)
        self.key_setup_le.setPlaceholderText("Master key")
        self.layout.addWidget(self.key_setup_le, 1, 0)

        self.key_reenter_le = QLineEdit()
        self.key_reenter_le.setEchoMode(QLineEdit.Password)
        self.key_reenter_le.textChanged.connect(self.check_password)
        self.key_reenter_le.setPlaceholderText("Confirm master key")
        self.layout.addWidget(self.key_reenter_le, 2, 0)

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.add_user)
        self.layout.addWidget(self.ok_btn, 2, 1)

        self.setLayout(self.layout)
        self.messagebox = MessageBox(self, "message")

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        if event.key() == Qt.Key_Return:
            self.ok_btn.click()

    def check_password(self):
        self.ok_btn.setEnabled(False)
        if all(
            [
                self.key_setup_le.text() == self.key_reenter_le.text(),
                len(self.key_setup_le.text()) > 3,
            ]
        ):
            self.ok_btn.setEnabled(True)

    def add_user(self):
        master_key = SHA256.new(self.key_setup_le.text().encode()).hexdigest()
        msg = requests.post(
            Config.config()["host"],
            {
                "action": "new_user",
                "user": self.username_setup_le.text(),
                "master_key": master_key,
            },
        ).text
        logging.debug(msg)
        if msg:
            if msg.startswith("Duplicate entry"):
                msg = "User exists. Login?"

            self.messagebox = MessageBox(self, msg)
            self.messagebox.show()

        else:
            self.window_main.key_input.setText(self.key_setup_le.text())
            self.window_main.name_input.setText(self.username_setup_le.text())
            self.close()

    def messagebox_handler(self, choice):
        if choice == 1:
            self.window_main.name_input.setText(self.username_setup_le.text())
            self.window_main.key_input.setText("")
            self.close()

    def reset_entries(self):
        self.username_setup_le.setText("")
        self.key_setup_le.setText("")
        self.key_reenter_le.setText("")

    def closeEvent(self, event):  # pylint: disable=invalid-name
        if self.messagebox.isVisible():
            self.messagebox.close()
        self.reset_entries()
        event.accept()
