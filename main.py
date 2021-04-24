#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
from password import *
import sys
import pyperclip

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
        self.layout = QGridLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Password', ''])

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('select * from passwords')
        self.data = c.fetchall()
        c.close()
        conn.close()

        for i in range(3):
            self.table.setColumnWidth(i, 190)
        self.table.setColumnWidth(3, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        copy_btns = []
        for row, i in zip(self.data, range(len(self.data))):
            self.table.insertRow(i)
            for data, j in zip(row, range(3)):
                self.table.setItem(self.data.index(row), j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(data))))

            copy_btns.append(copy_btn(i, self.data))
            self.table.setCellWidget(i, 3, copy_btns[i])

        self.setFixedWidth(640)
        self.table.setFixedWidth(604)

        self.layout.addWidget(self.table, 0, 0)
        self.setLayout(self.layout)

class copy_btn(QPushButton):
    def __init__(self, index, data):
        super().__init__()
        self.clicked.connect(lambda: pyperclip.copy(data[index][2]))

def main():

    argv = sys.argv
    argv[0] = 'Qt5PasswordManager'

    app = QApplication(argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
