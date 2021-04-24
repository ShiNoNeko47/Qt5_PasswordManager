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

        self.w1 = None
        self.w2 = None

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
        if self.key_input.text() == '123':
            self.addPassword_btn.setEnabled(True)
            self.showPasswords_btn.setEnabled(True)

    def newpassword(self):
        if self.w1 == None:
            self.w1 = NewPasswordWindow()
        self.w1.show()

    def showpasswords(self):
        if self.w2 == None:
            self.w2 = ShowPasswords()
        self.w2.show()

class NewPasswordWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('New Password')

class ShowPasswords(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Passwords')
        layout = QGridLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(3)

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('select * from passwords')
        self.data = c.fetchall()
        c.close()
        conn.close()

        for row in self.data:
            self.table.insertRow(self.data.index(row))
            print(row)
            for data in row:
                print(data + str(self.data.index(row)) + str(row.index(data)))
                self.table.setItem(self.data.index(row), row.index(data), QTableWidgetItem(data))

        layout.addWidget(self.table, 0, 0)
        self.setLayout(layout)

def main():

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('select * from passwords')
    print(c.fetchall())
    c.close()
    conn.close()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
