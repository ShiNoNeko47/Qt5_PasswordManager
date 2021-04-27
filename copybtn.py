import pyperclip
from PyQt5.QtWidgets import *

class Copy_btn(QPushButton):
    def __init__(self, index, data, f):
        super().__init__()
        self.clicked.connect(lambda: pyperclip.copy(f.decrypt(data[index][2].encode()).decode()))


