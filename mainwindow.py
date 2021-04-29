from Crypto.Hash import SHA256
from PyQt5.QtWidgets import *
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from managepasswordswindow import ManagePasswordsWindow
from showpasswordswindow import ShowPasswordsWindow

class MainWindow(QWidget):
    def __init__(self, key_hashed, key = ''):
        super().__init__()
        self.key_hashed = key_hashed
        self.setWindowTitle('PasswordManager')
        self.setFixedHeight(150)
        self.setFixedWidth(600)

        self.layout = QGridLayout()

        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.textChanged.connect(self.check_key)
        self.layout.addWidget(self.key_input)

        self.managePasswords_btn = QPushButton('Manage passwords')
        self.managePasswords_btn.setEnabled(False)
        self.managePasswords_btn.clicked.connect(self.managepasswords)
        self.layout.addWidget(self.managePasswords_btn)

        self.displayPasswords_btn = QPushButton('Display passwords')
        self.displayPasswords_btn.setEnabled(False)
        self.displayPasswords_btn.clicked.connect(self.displaypasswords)
        self.layout.addWidget(self.displayPasswords_btn)

        self.setLayout(self.layout)

        self.key_input.setText(key)

        self.w2 = ShowPasswordsWindow(self.displayPasswords_btn)
        self.w1 = ManagePasswordsWindow(self.w2, self.managePasswords_btn)

    def check_key(self):
        self.managePasswords_btn.setEnabled(False)
        self.displayPasswords_btn.setEnabled(False)
        if SHA256.new(str.encode(self.key_input.text())).hexdigest() == self.key_hashed:
            self.managePasswords_btn.setEnabled(True)
            self.displayPasswords_btn.setEnabled(True)
            self.key = self.getKey()
            #print(self.key)

    def managepasswords(self):
        self.w1.setKey(self.key)
        self.w2.setKey(self.key)
        self.w1.createTable()
        self.w1.show()

        self.managePasswords_btn.setDisabled(True)

    def displaypasswords(self):
        self.w2.setKey(self.key)
        self.w2.createTable()
        self.w2.show()

        self.displayPasswords_btn.setDisabled(True)

    def getKey(self):
        password = self.key_input.text().encode()
        salt = b'sw\xea\x01\x9d\x109\x0eF\xef/\n\xb0mWK'
        kdf = PBKDF2HMAC(
                algorithm = hashes.SHA256,
                length = 32,
                salt = salt,
                iterations=10000,
                backend = default_backend()
                )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def closeEvent(self, event):
        if all([self.w1.isHidden(), self.w2.isHidden()]):
            event.accept()
        else:
            event.ignore()

