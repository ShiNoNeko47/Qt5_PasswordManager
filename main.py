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

        self.displayPasswords_btn = QPushButton('Display passwords')
        self.displayPasswords_btn.setEnabled(False)
        self.displayPasswords_btn.clicked.connect(self.displaypasswords)
        self.layout.addWidget(self.displayPasswords_btn)

        self.managePasswords_btn = QPushButton('Manage passwords')
        self.managePasswords_btn.setEnabled(False)
        self.managePasswords_btn.clicked.connect(self.managepasswords)
        self.layout.addWidget(self.managePasswords_btn)

        self.setLayout(self.layout)

    def check_key(self):
        self.managePasswords_btn.setEnabled(False)
        self.displayPasswords_btn.setEnabled(False)
        if self.key_input.text() == '123':
            self.managePasswords_btn.setEnabled(True)
            self.displayPasswords_btn.setEnabled(True)

    def managepasswords(self):
        if self.w1 == None:
            self.w1 = ManagePasswordsWindow()
        self.w1.show()

    def displaypasswords(self):
        if self.w2 == None:
            self.w2 = ShowPasswords()
        self.w2.show()

class ManagePasswordsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Manage Passwords')
        self.layout = QGridLayout()

        self.newWebsite_le = QLineEdit()
        self.layout.addWidget(self.newWebsite_le, 0, 0)

        self.newUsername_le = QLineEdit()
        self.layout.addWidget(self.newUsername_le, 0, 1)

        self.newPassword_le = QLineEdit()
        self.newPassword_le.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.newPassword_le, 0, 2)

        self.add_btn = QPushButton('Add')
        self.layout.addWidget(self.add_btn, 0, 3)

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

        self.remove_btns = []
        for row, i in zip(self.data, range(len(self.data))):
            self.table.insertRow(i)
            for data, j in zip(row, range(3)):
                self.table.setItem(self.data.index(row), j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(data))))

            self.remove_btns.append(remove_btn(self.table, self.remove_btns))
            self.table.setCellWidget(i, 3, self.remove_btns[i])

        self.layout.addWidget(self.table, 1, 0, 1, 4)

        self.setLayout(self.layout)

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

class remove_btn(QPushButton):
    def __init__(self, table, remove_btns):
        super().__init__()
        self.table = table
        self.remove_btns = remove_btns
        self.clicked.connect(self.remove_row)

    def remove_row(self):
        self.table.removeRow(self.remove_btns.index(self))
        del self.remove_btns[self.remove_btns.index(self)]

def main():

    argv = sys.argv
    argv[0] = 'Qt5PasswordManager'

    app = QApplication(argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
