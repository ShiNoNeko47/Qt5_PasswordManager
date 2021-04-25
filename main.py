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

        self.w1 = ManagePasswordsWindow()
        self.w2 = ShowPasswords()

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

    def check_key(self):
        self.managePasswords_btn.setEnabled(False)
        self.displayPasswords_btn.setEnabled(False)
        if self.key_input.text() == '123':
            self.managePasswords_btn.setEnabled(True)
            self.displayPasswords_btn.setEnabled(True)

    def managepasswords(self):
        self.w1.createTable()
        self.w1.show()

    def displaypasswords(self):
        self.w2.createTable()
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
        self.add_btn.clicked.connect(self.addPassword)
        self.layout.addWidget(self.add_btn, 0, 3)

        self.commit_btn = QPushButton('Commit')
        self.commit_btn.clicked.connect(self.commitChanges)
        self.layout.addWidget(self.commit_btn, 2, 3)

        self.setLayout(self.layout)

    def createTable(self):
        self.sql = []

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Password', ''])

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('select website, username, password from passwords')
        self.data = c.fetchall()
        c.execute('select id from passwords')
        self.rowIds = c.fetchall()
        print(self.rowIds)
        c.close()
        conn.close()

        for i in range(3):
            self.table.setColumnWidth(i, 190)
        self.table.setColumnWidth(3, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for row, i in zip(self.data, range(len(self.data))):
            self.table.insertRow(i)
            for data, j in zip(row, range(3)):
                self.table.setItem(i, j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(data))))

        self.createRemoveBtns()

        self.layout.addWidget(self.table, 1, 0, 1, 4)

    def createRemoveBtns(self):
        self.remove_btns = []

        for i in range(self.table.rowCount()):
            try:
                self.remove_btns.append(remove_btn(self.rowIds[i][0], self.table, self.remove_btns, self.sql))
            except Exception:
                self.remove_btns.append(remove_btn(-1, self.table, self.remove_btns, self.sql))
            self.table.setCellWidget(i, 3, self.remove_btns[i])

    def addPassword(self):
        if all([self.newWebsite_le.text() != '', self.newUsername_le.text() != '', self.newPassword_le.text() != '']):
            n = self.table.rowCount()
            self.sql.append('insert into passwords values ({}, \'{}\',\'{}\',\'{}\')'.format(n, self.newWebsite_le.text(), self.newUsername_le.text(), self.newPassword_le.text()))
            self.table.insertRow(n)
            self.table.setItem(n, 0, (QTableWidgetItem('* ' + self.newWebsite_le.text())))
            self.table.setItem(n, 1, (QTableWidgetItem('* ' + self.newUsername_le.text())))
            self.table.setItem(n, 2, (QTableWidgetItem('* ' + '*' * len(self.newPassword_le.text()))))

            self.newWebsite_le.setText('')
            self.newUsername_le.setText('')
            self.newPassword_le.setText('')

            print(self.sql)
            self.createRemoveBtns()

    def commitChanges(self):
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        for statement in self.sql:
            c.execute(statement)
        conn.commit()
        c.close()
        conn.close()
        self.createTable()

class ShowPasswords(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Passwords')
        self.layout = QGridLayout()

        self.setFixedWidth(640)
        self.setLayout(self.layout)

    def createTable(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Password', ''])

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('select website, username, password from passwords')
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

        self.table.setFixedWidth(604)

        self.layout.addWidget(self.table, 0, 0)

class copy_btn(QPushButton):
    def __init__(self, index, data):
        super().__init__()
        self.clicked.connect(lambda: pyperclip.copy(data[index][2]))

class remove_btn(QPushButton):
    def __init__(self, rowId, table, remove_btns, sql):
        super().__init__()
        self.table = table
        self.remove_btns = remove_btns
        self.clicked.connect(self.remove_row)
        self.rowId = rowId
        self.sql = sql

    def remove_row(self):
        self.table.removeRow(self.remove_btns.index(self))
        del self.remove_btns[self.remove_btns.index(self)]
        if self.rowId >= 0:
            self.sql.append('delete from passwords where id = {}'.format(self.rowId))
        print(self.sql)

def main():

    argv = sys.argv
    argv[0] = 'Qt5PasswordManager'

    app = QApplication(argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
