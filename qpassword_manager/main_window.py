"""The window used for copying passwords from database"""

import logging
import os
import time
import threading
import json
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QLineEdit,
)
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from cryptography.fernet import Fernet
import pyperclip
from qpassword_manager.password_table import PasswordTable
from qpassword_manager.messagebox import MessageBox


class MainWindow(QWidget):
    """
    The window used for copying passwords from database

    Attributes:
        fernet: Fernet object used for decryption
        login_window: LoginWindow
    """

    def __init__(self, login_window) -> None:
        super().__init__()

        self.fernet = None
        self.login_window = login_window
        self.database_handler = login_window.database_handler

        self.setWindowTitle("Passwords")
        self.layout = QGridLayout()

        self.search_input = QLineEdit()
        self.layout.addWidget(self.search_input, 0, 0)
        self.search_input.hide()
        self.search_input.textChanged.connect(self.select)

        self.table = PasswordTable(self)
        self.layout.addWidget(self.table, 1, 0)
        self.selected = None

        self.cmd_input = QLineEdit()
        self.layout.addWidget(self.cmd_input, 3, 0)
        self.cmd_input.hide()

        self.setFixedWidth(640)
        self.setLayout(self.layout)

        self.auth = (
            self.login_window.name_input.text(),
            self.login_window.key_input_hashed.hexdigest()
        )

        self.set_key(self.login_window.get_key())
        self.table.fill_table()

        self.changes = []
        self.load_changes()

        self.messagebox = MessageBox("Save changes?", self)

        self.last_event_time = 0
        self.checking_inactivity = threading.Thread(
            target=self.check_inactivity, daemon=True)
        self.checking_inactivity.start()

    def set_key(self, key) -> None:
        """
        Creates Fernet object using a key

        Parameters:
            key: key used for creating a Fernet object
        """

        self.fernet = Fernet(key)

    def search(self) -> list:
        """Searches trough the table and returns a list of results"""

        search_string = self.search_input.text()

        if not search_string:
            return []

        items = self.table.findItems(
            ".*" + search_string + ".*", QtCore.Qt.MatchRegExp
        )
        items.sort(key=lambda x: x.row())
        return items

    def select(self) -> None:
        """Selects search results"""

        self.table.setCurrentItem(None)
        items = self.search()
        if items:
            for item in items:
                item.setSelected(True)

    def add_to_changes(self, change) -> None:
        """Appends to self.changes"""

        self.changes.append(change)
        if change[0]:
            self.table.entry_ids.append(len(self.changes) * -1)

    def commit_changes(self) -> None:
        """Commits changes to database"""

        current_cell = (self.table.currentRow(), self.table.currentColumn())

        for change in self.changes:
            if change[0] == -1:
                continue

            if change[0]:
                self.database_handler.add_to_database(*change[1], self.auth)
                continue

            self.database_handler.remove_from_database(change[2], self.auth)

        self.table.fill_table()
        self.table.setCurrentCell(*current_cell)
        self.changes.clear()

    def store_changes(self) -> None:
        """Stores changes to a file and clears the array"""

        if self.changes:
            with open("changes_" + self.auth[0], "wb+") as changes_file:
                changes_file.write(self.fernet.encrypt(
                    json.dumps(self.changes).encode()))

            self.changes.clear()

    def load_changes(self) -> None:
        """Loads changes stored in a file"""

        if os.path.exists("changes_" + self.auth[0]):
            with open("changes_" + self.auth[0], "rb") as changes_file:
                self.changes = json.loads(
                    self.fernet.decrypt(changes_file.read()))

            os.remove("changes_" + self.auth[0])

            for change in self.changes:
                if change[0]:
                    self.table.fill_row(change[1])

                else:
                    self.table.removeRow(change[1])

    def run_cmd(self) -> None:
        """Runs the command in cmd_input"""

        cmd = self.cmd_input.text()[1::]
        logging.debug(cmd)

        if cmd == "w":
            self.commit_changes()

        elif cmd == "q":
            self.close()

        elif cmd == "wq":
            self.commit_changes()
            self.close()

        elif cmd == "q!":
            self.changes.clear()
            self.close()

    def keyPressEvent(self, event) -> None:  # pylint: disable=invalid-name
        """Copy selected item in table"""

        if event.key() == Qt.Key_Return:
            if self.table.hasFocus():
                if self.table.selectedIndexes()[0].column() != 2:
                    logging.debug(self.table.selectedItems()[0].text())
                    pyperclip.copy(self.table.selectedItems()[0].text())

                else:
                    pyperclip.copy(
                        self.fernet.decrypt(
                            self.table.data[self.table.selectedIndexes()[0].row()][
                                2
                            ].encode()
                        ).decode()
                    )

            elif all(self.table.insert_mode()):
                if self.table.check_entry_input():
                    self.add_to_changes(
                        [1, self.table.get_entry_input(self.fernet)]
                    )
                    self.table.fill_row(
                        self.table.get_entry_input(self.fernet))
                    self.table.removeRow(self.table.entry_row_index)
                    self.table.setFocus()

            else:
                self.search_input.hide()
                self.run_cmd()
                self.cmd_input.hide()

        elif event.key() == Qt.Key_Escape:
            self.search_input.hide()
            self.search_input.clear()
            self.cmd_input.hide()
            if all(self.table.insert_mode()):
                self.table.setCurrentCell(
                    self.table.entry_row_index - 1,
                    self.table.currentColumn(),
                )
                self.table.setFocus()
            if self.table.insert_mode()[0] and all(
                entry.text() == "" for entry in self.table.entry_input
            ):
                self.table.removeRow(self.table.entry_row_index)
                self.table.setFocus()

    def messagebox_handler(self, choice) -> None:
        """
        MessageBox choice handler

        Arguments:
            choice: 1 or 0 based on the button clicked on MessageBox window
        """

        if choice:
            self.commit_changes()
            self.close()
        else:
            self.changes.clear()
            self.close()

    def check_inactivity(self) -> None:
        """Logs out after 5 minutes of inactivity"""

        while True:
            time.sleep(30)

            if self.isHidden():
                break

            if time.time() - self.last_event_time > 300:
                self.store_changes()
                self.close()
                break

    def event(self, event) -> bool:
        """Sets self.last_event_time to current time"""

        self.last_event_time = time.time()

        return QWidget.event(self, event)

    def closeEvent(self, event) -> None:  # pylint: disable=invalid-name
        """Closes the window and enables the login button if action queue is
        empty, otherwise open messagebox"""

        if not self.changes:
            event.accept()
            self.login_window.show()
        else:
            event.ignore()
            self.messagebox.close()
            self.messagebox.show()
