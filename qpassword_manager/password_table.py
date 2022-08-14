"""QTableWidget in main_window"""

import json
import logging
from pynput.keyboard import Key, Controller
import pyperclip
from PyQt5.QtWidgets import (
    QTableWidget,
    QLineEdit,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from qpassword_manager.database.database_handler import DatabaseHandler
from qpassword_manager.entry_input import NewPasswordInput, NewWebsiteInput


class PasswordTable(QTableWidget):
    """
    Reimplementation of QTableWidget class

    Attributes:
        keybinds: dictionary for keybind translations
        keyboard: controller that sends keys
    """

    def __init__(self, window):
        super().__init__()
        self.window = window

        self.keybinds = {
            "h": [Key.left],
            "j": [Key.down],
            "k": [Key.up],
            "l": [Key.right],
            "0": [Key.home],
            "$": [Key.end],
        }
        self.keyboard = Controller()

        self.current_index = 0
        self.setTabKeyNavigation(False)

        self.entry_ids = []
        self.entry_row_index = 0
        self.entry_input = None
        self.data = None

    def keyboardSearch(
        self, key
    ):  # pylint: disable=invalid-name, too-many-branches
        """Handles keys based on keybinds"""

        logging.debug(key)
        if key in self.keybinds:
            for keybind in self.keybinds[key]:
                self.keyboard.press(keybind)

            for keybind in self.keybinds[key]:
                self.keyboard.release(keybind)

        elif key == "/":
            self.window.search_input.clear()
            self.window.search_input.show()
            self.window.search_input.setFocus()
            if self.window.table.selectedItems():
                self.window.selected = self.window.table.selectedItems()[0]

            self.window.select()

        elif key in ["g", "G"]:
            self.setCurrentCell(
                0 if key == "g" else self.rowCount() - 1, self.currentColumn()
            )

        elif key in ["n", "N"]:
            self.search_next_prev(key, self.window.search())

        elif key == ":":
            self.window.cmd_input.setText(":")
            self.window.cmd_input.show()
            self.window.cmd_input.setFocus()

        elif key in ["i", "I", "a", "A", "o", "O"]:
            if not self.insert_mode()[0]:
                self.entry_row_index = self.rowCount()
                self.insertRow(self.entry_row_index)

                self.entry_input = [
                    NewWebsiteInput(),
                    QLineEdit(),
                    NewPasswordInput(),
                ]

                for i in range(3):
                    self.setCellWidget(
                        self.entry_row_index, i, self.entry_input[i]
                    )
            self.focus_entry_input()

        elif key in ["y", "Y"]:
            entry_id = self.entry_ids[self.currentRow()]
            pyperclip.copy(
                json.dumps(
                    DatabaseHandler.get_entry(entry_id, self.window.auth)
                    if entry_id >= 0
                    else self.window.changes[-entry_id - 1][1]
                )
            )

        elif key in ["p", "P"]:
            self.fill_row(json.loads(pyperclip.paste()))
            self.window.add_to_changes([1, json.loads(pyperclip.paste())])

        elif key in ["d", "D"]:
            if self.entry_ids:
                entry_id = self.entry_ids[self.currentRow()]
                if entry_id < 0:
                    self.window.changes[-entry_id - 1] = -1

                    while self.window.changes[-1] == -1:
                        self.window.changes.pop()
                        if not self.window.changes:
                            break

                else:
                    self.window.add_to_changes([0, self.currentRow(), entry_id])

                self.entry_ids.pop(self.currentRow())
                self.removeRow(self.currentRow())

    def fill_row(self, row, index=None):
        """Fills table row with values from the list passed to it"""

        index = index or self.rowCount()
        self.insertRow(index)
        for j in range(2):
            self.setItem(index, j, (QTableWidgetItem(row[j])))

        row = "*" * len(self.window.fernet.decrypt(row[2].encode()))
        self.setItem(index, 2, (QTableWidgetItem(row)))
        self.setCurrentCell(self.rowCount() - 1, self.currentColumn())

    def fill_table(self):
        """Updates data in the table"""

        self.clear()
        self.setColumnCount(3)
        self.setRowCount(0)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(["Website", "Username", "Password"])
        self.data = DatabaseHandler.get_all(self.window.auth)
        logging.debug(self.data)

        for i in range(3):
            self.setColumnWidth(i, 190)

        self.setColumnWidth(3, 30)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SingleSelection)

        for i, row in enumerate(self.data):
            self.fill_row(row, i)

        if self.rowCount():
            self.setCurrentCell(0, 0)

        self.entry_ids = DatabaseHandler.get_entry_ids(self.window.auth)

    def search_next_prev(self, key, items):
        """
        Allows you to navigate search results:
            n -> forward
            N -> backward
        """

        if not items:
            return 0

        if not self.currentItem():
            self.setCurrentItem(items[0])
            self.current_index = 0

        else:
            try:
                self.current_index += 1 if key == "n" else -1
                self.setCurrentItem(items[self.current_index])

            except IndexError:
                if self.current_index > 0:
                    self.current_index = 0

                else:
                    self.current_index = -1

                self.setCurrentItem(items[self.current_index])

        return 0

    def insert_mode(self):
        """Checks if last row in table is entry_input and if it's focused"""

        return (
            isinstance(
                self.cellWidget(self.entry_row_index, 2), NewPasswordInput
            ),
            self.currentRow() == self.entry_row_index,
        )

    def check_entry_input(self):
        """Checks if all values in entry_input are valid"""

        return (
            all(widget.text() for widget in self.entry_input)
            and self.entry_input[2].text() == self.entry_input[2].other_text
        )

    def get_entry_input(self, fernet):
        """Returns values from entry_input"""

        return [
            self.entry_input[0].text(),
            self.entry_input[1].text(),
            fernet.encrypt(self.entry_input[2].text().encode()).decode(),
        ]

    def focus_entry_input(self):
        """Gives focus to first empty field in entry_input"""

        for i, widget in enumerate(self.entry_input):
            if not widget.text():
                self.setCurrentCell(self.entry_row_index, i)
                break
            self.setCurrentCell(self.entry_row_index, 2)
