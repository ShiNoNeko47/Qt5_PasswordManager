"""Setup window"""

import logging
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QGridLayout
from PyQt5.Qt import Qt
from Crypto.Hash import SHA256
from qpassword_manager.messagebox import MessageBox
from qpassword_manager.database.database_handler import DatabaseHandler
from qpassword_manager.entry_input import NewPasswordInput
from qpassword_manager.conf.connectorconfig import Config


class SetupWindow(QWidget):
    """
    Setup window

    Attributes:
        window_login: login window

    """

    def __init__(self, window_login) -> None:
        super().__init__()

        self.window_login = window_login

        self.layout = QGridLayout()
        self.setWindowTitle("New user")
        self.setFixedHeight(150)
        self.setFixedWidth(600)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.layout.addWidget(self.username_input, 0, 0, 1, 3)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")
        if Config.config()["database_online"]:
            self.layout.addWidget(self.email_input, 1, 0, 1, 3)

        self.key_input = NewPasswordInput()
        self.key_input.textChanged.connect(self.check_password)
        self.key_input.setPlaceholderText("Master key")
        self.layout.addWidget(self.key_input, 2, 0, 1, 3)

        self.ok_btn = QPushButton("Register")
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.add_user)
        self.layout.addWidget(self.ok_btn, 3, 1)

        self.setLayout(self.layout)
        self.messagebox = MessageBox(" ")

    def keyPressEvent(self, event) -> None:  # pylint: disable=invalid-name
        """Clicks ok when you press enter"""

        if event.key() == Qt.Key_Return:
            self.ok_btn.click()

    def check_password(self) -> None:
        """Checks if password entered is longer than 3 characters"""

        self.ok_btn.setEnabled(False)
        if all(
            [
                self.key_input.text() == self.key_input.other_text,
                len(self.key_input.text()) > 3,
            ]
        ):
            self.ok_btn.setEnabled(True)

    def add_user(self) -> None:
        """Adds new user to database"""

        master_key = SHA256.new(self.key_input.text().encode()).hexdigest()
        msg = DatabaseHandler.register(
            self.username_input.text(), self.email_input.text(), master_key
        )

        logging.debug(msg)
        if msg in [
            "Registration successfull!",
            "Please confirm your email to finish the registration",
        ]:
            self.window_login.key_input.setText(self.key_input.text())
            self.window_login.name_input.setText(self.username_input.text())
            self.close()

        self.messagebox = MessageBox(msg, self)
        self.messagebox.show()

    def messagebox_handler(self, choice) -> None:
        """
        MessageBox choice handler

        Arguments:
            choice: 1 or 0 based on the button clicked on MessageBox window
        """

        if choice == 1:
            self.window_login.name_input.setText(self.username_input.text())
            self.window_login.key_input.setText("")
            self.close()

    def reset_entries(self) -> None:
        """Sets all entries to \"\" """

        self.username_input.setText("")
        self.key_input.setText("")
        self.key_input.other_text = ""

    def closeEvent(self, event) -> None:  # pylint: disable=invalid-name
        """Closes MessageBox and sets all entries to \"\" when closing
        SetupWindow"""

        if self.messagebox.isVisible():
            self.messagebox.close()
        self.reset_entries()
        event.accept()
