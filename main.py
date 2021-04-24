#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
from password import *
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PasswordManager')
        self.w = None
        layout = QGridLayout()

        addPassword_btn = QPushButton('Add password')
        addPassword_btn.clicked.connect(self.newpassword)
        layout.addWidget(addPassword_btn)

        showPasswords_btn = QPushButton('Show my passwords')
        showPasswords_btn.clicked.connect(self.showpasswords)
        layout.addWidget(showPasswords_btn)

        self.setLayout(layout)

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
