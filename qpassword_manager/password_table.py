"""QTableWidget in main_window"""

import json
import logging

import pyperclip
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QTableWidget,
    QLineEdit,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QApplication,
)
from qpassword_manager.entry_input import NewPasswordInput, NewWebsiteInput


class PasswordTable(QTableWidget):
    """
    Reimplementation of QTableWidget class

    Attributes:
        keybinds: dictionary for keybind translations
        keyboard: controller that sends keys
    """

    def __init__(self, window) -> None:
        super().__init__()
        self.window = window

        self.keybinds = {
            Qt.Key_H: Qt.Key_Left,
            Qt.Key_J: Qt.Key_Down,
            Qt.Key_K: Qt.Key_Up,
            Qt.Key_L: Qt.Key_Right,
            Qt.Key_0: Qt.Key_Home,
            Qt.Key_Dollar: Qt.Key_End,
        }

        self.current_index = 0
        self.setTabKeyNavigation(False)

        self.entry_ids = []
        self.entry_row_index = 0
        self.entry_input = None
        self.entry_input_mode = 0
        self.data = None

    def event(self, event) -> bool:
        """Handles keys for navigation"""

        if event.type() == QEvent.KeyPress and event.key() in self.keybinds:
            event = QKeyEvent(
                QEvent.KeyPress,
                self.keybinds[event.key()],
                Qt.NoModifier,
                "",
            )
            QApplication.sendEvent(self, event)
            return True

        return QTableWidget.event(self, event)

    def keyboardSearch(  # pylint: disable=invalid-name, too-many-branches
        self, key
    ) -> None:
        """Handles keys based on keybinds"""

        if key == "/":
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
            self.add_row(self.rowCount())
            self.entry_input_mode = 1

        elif key in ["c", "C"]:
            row = self.currentRow()
            current_entry = self.window.database_handler.get_entry(
                self.entry_ids[row], self.window.auth
            )

            if current_entry is not None:
                self.removeRow(row)
                self.add_row(row)

                for i in range(2):
                    self.entry_input[i].setText(current_entry[i])

                self.entry_input[2].setText(
                    self.window.fernet.decrypt(
                        current_entry[2].encode()
                    ).decode()
                )
                self.entry_input_mode = 2

        elif key in ["y", "Y"]:
            entry_id = self.entry_ids[self.currentRow()]
            pyperclip.copy(
                json.dumps(
                    self.window.database_handler.get_entry(
                        entry_id, self.window.auth
                    )
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

    def stop_change(self) -> None:
        """Stops editting and resets values in current row to the ones in database"""

        row_index = self.currentRow()
        column_index = self.currentColumn()
        self.removeRow(row_index)
        row = self.window.database_handler.get_entry(
            self.entry_ids[row_index], self.window.auth
        )
        self.fill_row(row, row_index)
        self.setCurrentCell(row_index, column_index)

    def add_row(self, row) -> None:
        """Adds a row with input entries"""

        if not self.insert_mode()[0]:
            self.entry_row_index = row
            self.insertRow(row)

            self.entry_input = [
                NewWebsiteInput(),
                QLineEdit(),
                NewPasswordInput(),
            ]

            for i in range(3):
                self.setCellWidget(row, i, self.entry_input[i])
        self.focus_entry_input()

    def fill_row(self, row, index=None) -> None:
        """Fills table row with values from the list passed to it"""

        if index is None:
            index = self.rowCount()
        self.insertRow(index)
        for j in range(2):
            self.setItem(index, j, (QTableWidgetItem(row[j])))

        row = "*" * len(self.window.fernet.decrypt(row[2].encode()))
        self.setItem(index, 2, (QTableWidgetItem(row)))
        self.setCurrentCell(index, self.currentColumn())

    def fill_table(self) -> None:
        """Updates data in the table"""

        self.clear()
        self.setColumnCount(3)
        self.setRowCount(0)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(["Website", "Username", "Password"])
        self.data = self.window.database_handler.get_all(self.window.auth)
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

        self.entry_ids = self.window.database_handler.get_entry_ids(
            self.window.auth
        )

    def search_next_prev(self, key, items) -> None:
        """
        Allows you to navigate search results:
            n -> forward
            N -> backward
        """

        if not items:
            return

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

        return

    def insert_mode(self) -> (bool, bool):
        """Checks if last row in table is entry_input and if it's focused"""

        return (
            isinstance(
                self.cellWidget(self.entry_row_index, 2), NewPasswordInput
            ),
            self.currentRow() == self.entry_row_index,
        )

    def check_entry_input(self) -> bool:
        """Checks if all values in entry_input are valid"""

        return (
            all(widget.text() for widget in self.entry_input)
            and self.entry_input[2].text() == self.entry_input[2].other_text
        )

    def get_entry_input(self, fernet) -> [str, str, str]:
        """Returns values from entry_input"""

        return [
            self.entry_input[0].text(),
            self.entry_input[1].text(),
            fernet.encrypt(self.entry_input[2].text().encode()).decode(),
        ]

    def focus_entry_input(self) -> None:
        """Gives focus to first empty field in entry_input"""

        for i, widget in enumerate(self.entry_input):
            if not widget.text():
                self.setCurrentCell(self.entry_row_index, i)
                break
            self.setCurrentCell(self.entry_row_index, 2)
