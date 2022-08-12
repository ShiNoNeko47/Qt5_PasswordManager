"""The window used for copying passwords from database"""

import logging
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QAbstractItemView,
    QHeaderView,
    QLineEdit,
)
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from cryptography.fernet import Fernet
import pyperclip
from qpassword_manager.database.database_handler import DatabaseHandler
from qpassword_manager.password_table import PasswordTable
from qpassword_manager.messagebox import MessageBox


class MainWindow(QWidget):
    """
    The window used for copying passwords from database

    Attributes:
        fernet: Fernet object used for decryption
        btn: login_btn on LoginWindow
    """

    def __init__(self, btn):
        super().__init__()

        self.fernet = None
        self.btn = btn

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

        self.changes = []
        self.data = None

        self.messagebox = MessageBox(self, "Save changes?")

    def set_key(self, key):
        """
        Creates Fernet object using a key

        Parameters:
            key: key used for creating a Fernet object
        """

        self.fernet = Fernet(key)

    def search(self):
        """Searches trough the table and returns a list of results"""

        search_string = self.search_input.text()

        if not search_string:
            return []

        items = self.table.findItems(
            ".*" + search_string + ".*", QtCore.Qt.MatchRegExp
        )
        items.sort(key=lambda x: x.row())
        return items

    def select(self):
        """Selects search results"""

        self.table.setCurrentItem(None)
        items = self.search()
        if items:
            for item in items:
                item.setSelected(True)

    def create_table(self):
        """Updates data in the table"""

        self.table.clear()
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )
        self.table.setHorizontalHeaderLabels(
            ["Website", "Username", "Password"]
        )
        self.data = DatabaseHandler.create_table(self.auth)
        logging.debug(self.data)

        for i in range(3):
            self.table.setColumnWidth(i, 190)

        self.table.setColumnWidth(3, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        for i, row in enumerate(self.data):
            self.table.fill_row(row, i)

        if self.table.rowCount():
            self.table.setCurrentCell(0, 0)

        self.table.entry_ids = DatabaseHandler.get_row_ids(self.auth)

    def add_to_changes(self, change):
        """Appends to self.changes"""

        self.changes.append(change)
        if change[0]:
            self.table.entry_ids.append(len(self.changes) * -1)

    def commit_changes(self):
        """Commits changes to database"""

        current_cell = (self.table.currentRow(), self.table.currentColumn())

        for change in self.changes:
            if change[0] == -1:
                continue

            if change[0]:
                DatabaseHandler.add_to_database(*change[1], self.auth)
                continue

            DatabaseHandler.delete_row(change[2], self.auth)

        self.create_table()
        self.table.setCurrentCell(*current_cell)
        self.changes.clear()

    def run_cmd(self):
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

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Copy selected item in table"""

        if event.key() == Qt.Key_Return:
            if self.table.hasFocus():
                if self.table.selectedIndexes()[0].column() != 2:
                    logging.debug(self.table.selectedItems()[0].text())
                    pyperclip.copy(self.table.selectedItems()[0].text())

                else:
                    pyperclip.copy(
                        self.fernet.decrypt(
                            self.data[
                                self.table.selectedIndexes()[0].row()
                            ][2].encode()
                        ).decode()
                    )

            elif all(self.table.insert_mode()):
                if self.table.check_entry_input():
                    self.add_to_changes(
                        [1, self.table.get_entry_input(self.fernet)]
                    )
                    self.table.fill_row(
                        self.table.get_entry_input(self.fernet)
                    )
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

    def messagebox_handler(self, choice):
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

    def closeEvent(self, event):  # pylint: disable=invalid-name
        """Closes the window and enables the login button if action queue is
        empty, otherwise open messagebox"""

        if not self.changes:
            event.accept()
            self.btn.setDisabled(False)
        else:
            event.ignore()
            self.messagebox.close()
            self.messagebox.show()
