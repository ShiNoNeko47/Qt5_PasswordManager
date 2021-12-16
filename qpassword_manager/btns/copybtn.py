import pyperclip
from PyQt5.QtWidgets import QPushButton


class CopyBtn(QPushButton):
    def __init__(self, index, data, f):
        super().__init__()
        self.decrypted = f.decrypt(data[index]["2"].encode()).decode()
        self.clicked.connect(lambda: pyperclip.copy(self.decrypted))
        self.setText("📋")
