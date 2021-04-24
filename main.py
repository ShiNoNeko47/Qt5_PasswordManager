#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
from password import *
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PasswordManager')
        self.setFixedHeight(150)
        self.setFixedWidth(600)
        self.w = None
        access = False
        self.layout = QGridLayout()

        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.textChanged.connect(self.check_key)
        self.layout.addWidget(self.key_input)

        self.addPassword_btn = QPushButton('Add password')
        self.addPassword_btn.setEnabled(False)
        self.addPassword_btn.clicked.connect(self.newpassword)
        self.layout.addWidget(self.addPassword_btn)

        self.showPasswords_btn = QPushButton('Show my passwords')
        self.showPasswords_btn.setEnabled(False)
        self.showPasswords_btn.clicked.connect(self.showpasswords)
        self.layout.addWidget(self.showPasswords_btn)

        self.setLayout(self.layout)

    def check_key(self):
        self.addPassword_btn.setEnabled(False)
        self.showPasswords_btn.setEnabled(False)
        if self.key_input.text() == 'abc':
            self.addPassword_btn.setEnabled(True)
            self.showPasswords_btn.setEnabled(True)

    def newpassword(self):
        if self.w == None:
            self.w = NewPasswordWindow()
        self.w.show()

    def showpasswords(self):
        if self.w == None:
            self.w = NewPasswordWindow()
        self.w.show()

class NewPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Password')

class ShowPasswords(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Passwords')
        layout = QGridLayout()


        layout.addWidget()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
