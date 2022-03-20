"""The window used for adding and removing passwords"""

import logging
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
)
from cryptography.fernet import Fernet
from qpassword_manager.messagebox import MessageBox
from qpassword_manager.btns.removebtn import RemoveBtn
from qpassword_manager.btns.editbtn import EditBtn
from qpassword_manager.database.database_handler import DatabaseHandler


class ManagePasswordsWindow(QWidget):
    """
    The window used for adding and removing passwords

    Attributes:
        fernet: Fernet object used for decryption
        btn: manage_passwords_btn on MainWindow
    """

    def __init__(self, window_display_passwords, btn):
        super().__init__()
        self.fernet = None
        self.btn = btn
        self.row_ids = []
        self.window_display_passwords = window_display_passwords

        self.setWindowTitle("Manage Passwords")
        self.layout = QGridLayout()

        self.new_website_le = QLineEdit()
        self.new_website_le.textChanged.connect(self.valid_input_check)
        self.new_website_le.setPlaceholderText("Website")
        self.layout.addWidget(self.new_website_le, 0, 0, 2, 1)

        self.new_username_le = QLineEdit()
        self.new_username_le.setPlaceholderText("Username")
        self.new_username_le.textChanged.connect(self.valid_input_check)
        self.layout.addWidget(self.new_username_le, 0, 1, 2, 1)

        self.new_password_le = QLineEdit()
        self.new_password_le.setPlaceholderText("Password")
        self.new_password_le.setEchoMode(QLineEdit.Password)
        self.new_password_le.textChanged.connect(self.valid_input_check)
        self.layout.addWidget(self.new_password_le, 0, 2)

        self.re_new_password_le = QLineEdit()
        self.re_new_password_le.setPlaceholderText("Confirm Password")
        self.re_new_password_le.setEchoMode(QLineEdit.Password)
        self.re_new_password_le.textChanged.connect(self.valid_input_check)
        self.layout.addWidget(self.re_new_password_le, 1, 2)

        self.add_btn = QPushButton("Add")
        self.add_btn.clicked.connect(self.add_password)
        self.add_btn.setDisabled(True)
        self.layout.addWidget(self.add_btn, 0, 3, 2, 1)

        self.save_btn = QPushButton("Save")
        self.save_btn.setDisabled(True)
        self.save_btn.clicked.connect(self.commit_changes)
        self.layout.addWidget(self.save_btn, 3, 3)

        self.table = QTableWidget()
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.layout.addWidget(self.table, 2, 0, 1, 4)

        self.setLayout(self.layout)
        self.setFixedWidth(640)

        self.messagebox = MessageBox(self, "Save changes?")

    def messagebox_handler(self, choice):
        """
        MessageBox choice handler

        Arguments:
            choice: 1 or 0 based on the button clicked on MessageBox window
        """

        if choice == 1:
            self.commit_changes()
            self.close()
        else:
            self.actions.clear()
            RemoveBtn.marked.clear()
            self.save_btn.setDisabled(True)
            self.close()

    def set_key(self, key):
        """
        Creates Fernet object using a key

        Parameters:
            key: key used for creating a Fernet object
        """

        self.fernet = Fernet(key)

    def create_table(self):
        """Updates data in the table"""

        self.actions = []

        self.table.clear()
        self.table.setRowCount(0)
        self.table.setColumnCount(5)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Stretch
        )
        self.table.setHorizontalHeaderLabels(
            ["Website", "Username", "Password", "", ""]
        )
        data = DatabaseHandler.create_table(self.auth)

        self.row_ids = DatabaseHandler.get_row_ids(self.auth)
        logging.debug("row_ids:", self.row_ids)

        for i in range(3):
            self.table.setColumnWidth(i, 180)
        self.table.setColumnWidth(3, 30)
        self.table.setColumnWidth(4, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for i, row in enumerate(data):
            self.table.insertRow(i)
            for j in range(2):
                item = row[j]
                logging.debug(item)
                self.table.setItem(i, j, (QTableWidgetItem(item)))
            data = "*" * len(self.fernet.decrypt(row[2].encode()))
            self.table.setItem(i, 2, (QTableWidgetItem(data)))
        self.create_btns()

        self.table.setFixedWidth(620)

    def create_btns(self):
        """Adds buttons to the table"""

        remove_btns = []
        edit_btns = []

        for i, row_id in enumerate(self.row_ids):
            edit_btns.append(EditBtn(row_id, edit_btns, self))
            self.table.setCellWidget(i, 3, edit_btns[i])
            remove_btns.append(
                RemoveBtn(
                    row_id,
                    self,
                )
            )
            self.table.setCellWidget(i, 4, remove_btns[i])

    def valid_input_check(self):
        """Checks if none of entries are empty and passwords match"""

        check = [
            all(
                [
                    self.new_website_le.text() != "",
                    self.new_username_le.text() != "",
                    self.new_password_le.text() != "",
                    self.re_new_password_le.text() != "",
                ]
            ),
            self.new_password_le.text() == self.re_new_password_le.text(),
        ]

        if all(check):
            self.add_btn.setDisabled(False)
            return True

        self.add_btn.setDisabled(True)
        return False

    def add_password(self):
        """Adds action to queue and a row to table"""

        if self.valid_input_check():
            self.actions.append(
                [
                    self.new_website_le.text(),
                    self.new_username_le.text(),
                    self.fernet.encrypt(
                        self.new_password_le.text().encode()
                    ).decode(),
                    "add",
                ]
            )

            self.save_btn.setDisabled(not self.actions)

            row_count = self.table.rowCount()
            self.table.insertRow(row_count)

            website = self.new_website_le.text()
            self.table.setItem(
                row_count, 0, (QTableWidgetItem("+ " + website)))

            username = self.new_username_le.text()
            self.table.setItem(
                row_count, 1, (QTableWidgetItem("+ " + username))
            )

            password = "*" * len(self.new_password_le.text())
            self.table.setItem(
                row_count, 2, (QTableWidgetItem("+ " + password))
            )

            self.new_website_le.setText("")
            self.new_username_le.setText("")
            self.new_password_le.setText("")
            self.re_new_password_le.setText("")

            self.create_btns()

    def commit_changes(self):
        """Saves changes from queue to database"""

        for action in self.actions:
            if action.pop() == "add":
                DatabaseHandler.add_to_database(
                    action[2], action[1], action[0], self.auth
                )
            else:
                DatabaseHandler.delete_row(action, self.auth)

        RemoveBtn.marked.clear()
        self.actions.clear()

        self.create_table()
        self.window_display_passwords.create_table()
        self.save_btn.setDisabled(True)

    def reset_entries(self):
        """Sets all entries to \"\" """

        self.new_website_le.setText("")
        self.new_username_le.setText("")
        self.new_password_le.setText("")
        self.re_new_password_le.setText("")

    def closeEvent(self, event):  # pylint: disable=invalid-name
        """Closes ManagePasswordsWindow if queue is empty, otherwise opens
        MessageBox"""

        if not self.actions:
            self.btn.setDisabled(False)
            self.reset_entries()
            event.accept()
        else:
            event.ignore()
            self.messagebox.close()
            self.messagebox.show()
