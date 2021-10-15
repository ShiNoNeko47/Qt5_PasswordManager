import sqlite3
from Crypto.Hash import SHA256
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPoint
from PyQt5.Qt import Qt
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from managepasswordswindow import ManagePasswordsWindow
from showpasswordswindow import ShowPasswordsWindow
from setupwindow import SetupWindow

class MainWindow(QWidget):
    def __init__(self, key = ''):
        super().__init__()
        self.move(QPoint(350, 200))

        self.key_hashed = 'a'
        self.setWindowTitle('PasswordManager')
        self.setFixedHeight(250)
        self.setFixedWidth(600)

        self.layout = QGridLayout()

        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.check_input)
        self.layout.addWidget(self.name_input, 0, 0, 1, 3)

        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.textChanged.connect(self.check_input)
        self.layout.addWidget(self.key_input, 1, 0, 1, 3)

        self.displayPasswords_btn = QPushButton('Display passwords')
        self.displayPasswords_btn.setEnabled(False)
        self.displayPasswords_btn.clicked.connect(self.displaypasswords)
        self.layout.addWidget(self.displayPasswords_btn, 2, 0, 1, 3)

        self.managePasswords_btn = QPushButton('Manage passwords')
        self.managePasswords_btn.setEnabled(False)
        self.managePasswords_btn.clicked.connect(self.managepasswords)
        self.layout.addWidget(self.managePasswords_btn, 3, 0, 1, 3)

        self.newUser_btn = QPushButton('New user')
        self.newUser_btn.clicked.connect(self.newuser)
        self.layout.addWidget(self.newUser_btn, 4, 1)

        self.setLayout(self.layout)

        self.key_input.setText(key)

        self.w3 = SetupWindow(self)
        self.w2 = ShowPasswordsWindow(self.displayPasswords_btn)
        self.w1 = ManagePasswordsWindow(self.w2, self.managePasswords_btn)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.displayPasswords_btn.click()

    def check_input(self):
        self.managePasswords_btn.setEnabled(False)
        self.displayPasswords_btn.setEnabled(False)
        if len(self.key_input.text()) >= 4 and len(self.name_input.text())>0:
            self.managePasswords_btn.setEnabled(True)
            self.displayPasswords_btn.setEnabled(True)

    def check_key(self):
        try:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute('select password from {} where (id = -1)'.format(self.name_input.text()))
            key_hashed = c.fetchone()[0]
            c.close()
            conn.close()
            print(key_hashed)
            print(SHA256.new(str.encode(self.key_input.text())).hexdigest())
            if SHA256.new(str.encode(self.key_input.text())).hexdigest() == key_hashed:
                self.key = self.getKey()
                print(self.key)
                return True
            return False
        except:
            pass

    def managepasswords(self):
        if self.check_key():
            self.w1.user = self.name_input.text()
            self.w1.setKey(self.key)
            self.w2.user = self.name_input.text()
            self.w2.setKey(self.key)
            self.w1.createTable()
            self.w1.show()

            self.managePasswords_btn.setDisabled(True)

    def displaypasswords(self):
        if self.check_key():
            self.w2.user = self.name_input.text()
            self.w2.setKey(self.key)
            self.w2.createTable()
            self.w2.show()

            self.displayPasswords_btn.setDisabled(True)

    def newuser(self):
        self.w3.show()

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

