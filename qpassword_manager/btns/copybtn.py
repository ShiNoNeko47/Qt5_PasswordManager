'''CopyBtn class'''

import pyperclip
from PyQt5.QtWidgets import QPushButton


class CopyBtn(QPushButton):
    '''
    Button that copies a decrypted password to clipboard

    Attributes:
        decrypted: decrypted password
    '''

    def __init__(self, index, data, fernet):
        super().__init__()
        self.decrypted = fernet.decrypt(data[index]["2"].encode()).decode()
        self.clicked.connect(lambda: pyperclip.copy(self.decrypted))
        self.setText("📋")
