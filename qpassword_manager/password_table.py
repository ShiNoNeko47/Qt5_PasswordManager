import logging
from PyQt5.QtWidgets import QTableWidget
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

    def keyboardSearch(self, key):  # pylint: disable=invalid-name
        """Handles keys based on keybinds"""

        logging.debug(key)
        if key in self.keybinds:
            for keybind in self.keybinds[key]:
                self.keyboard.press(keybind)

            for keybind in self.keybinds[key]:
                self.keyboard.release(keybind)

        elif key == '/':
            self.window.search_input.show()
            self.window.search_input.setFocus()
            if self.window.table.selectedItems():
                self.window.selected = self.window.table.selectedItems()[0]

            self.window.select()

        elif key in ['n', 'N']:
            self.window.search_next_prev(key, self.window.search())
