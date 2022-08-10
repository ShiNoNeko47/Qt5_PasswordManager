import logging
from PyQt5.QtWidgets import QTableWidget, QLineEdit
from PyQt5.Qt import Qt
from qpassword_manager.entry_input import NewPasswordInput, NewWebsiteInput
from pynput.keyboard import Key, Controller



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
            'h': [Key.left],
            'j': [Key.down],
            'k': [Key.up],
            'l': [Key.right],
            'g': [Key.ctrl, Key.home],
            'G': [Key.ctrl, Key.end],
            '0': [Key.home],
            '$': [Key.end],
        }
        self.keyboard = Controller()
        self.current_index = 0
        self.setTabKeyNavigation(False)

    def insert_mode(self):
        return (type(self.cellWidget(0, 2)) == NewPasswordInput, self.currentRow() == 0)

    def focus_entry_input(self):
        for i, widget in enumerate(self.entry_input):
            if not widget.text():
                self.setCurrentCell(0, i)
                break
            self.setCurrentCell(0, 2)

    def keyboardSearch(self, key):  # pylint: disable=invalid-name
        """Handles keys based on keybinds"""

        logging.debug(key)
        if key in self.keybinds:
            for keybind in self.keybinds[key]:
                self.keyboard.press(keybind)

            for keybind in self.keybinds[key]:
                self.keyboard.release(keybind)

        elif key == '/':
            self.window.search_input.clear()
            self.window.search_input.show()
            self.window.search_input.setFocus()
            if self.window.table.selectedItems():
                self.window.selected = self.window.table.selectedItems()[0]

            self.window.select()

        elif key in ['n', 'N']:
            self.window.search_next_prev(key, self.window.search())

        elif key == ':':
            self.window.cmd_input.setText(":")
            self.window.cmd_input.show()
            self.window.cmd_input.setFocus()

        elif key in ['o', 'O']:
            if not self.insert_mode()[0]:
                self.insertRow(0)

                self.entry_input = [
                    NewWebsiteInput(),
                    QLineEdit(),
                    NewPasswordInput()
                ]

                for i in range(3):
                    self.setCellWidget(0, i, self.entry_input[i])
            self.focus_entry_input()

        # elif key in ['y', 'Y']:
        # elif key in ['p', 'P']:
        # elif key == 'u':
