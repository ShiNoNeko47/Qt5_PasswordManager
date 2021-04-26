#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
from password import *
import sys
import pyperclip
import os
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2

class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setWindowTitle('Setup')
        self.setFixedHeight(100)
        self.setFixedWidth(600)

        self.key_setup_le = QLineEdit()
        self.key_setup_le.setEchoMode(QLineEdit.Password)
        self.key_setup_le.textChanged.connect(self.check)
        self.layout.addWidget(self.key_setup_le, 0, 0)

        self.key_reenter_le = QLineEdit()
        self.key_reenter_le.setEchoMode(QLineEdit.Password)
        self.key_reenter_le.textChanged.connect(self.check)
        self.layout.addWidget(self.key_reenter_le, 1, 0)

        self.ok_btn = QPushButton('Ok')
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.ok)
        self.layout.addWidget(self.ok_btn, 1, 1)

        self.setLayout(self.layout)

    def check(self):
        self.ok_btn.setEnabled(False)
        if all([self.key_setup_le.text() == self.key_reenter_le.text(), len(self.key_setup_le.text()) > 3]):
            self.ok_btn.setEnabled(True)

    def ok(self):
        self.close()

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute("insert into passwords values (-1, \'Master\', \'Key\', \'{}\')".format(SHA256.new(str.encode(self.key_setup_le.text())).hexdigest()))
        conn.commit()
        c.close()
        conn.close()

        self.window = MainWindow(SHA256.new(str.encode(self.key_setup_le.text())).hexdigest())
        self.window.show()

class MainWindow(QWidget):
    def __init__(self, key_hashed):
        super().__init__()
        self.key_hashed = key_hashed
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
        if SHA256.new(str.encode(self.key_input.text())).hexdigest() == self.key_hashed:
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

        self.setFixedWidth(640)
        self.setLayout(self.layout)

    def createTable(self):
        self.sql = []

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Password', ''])

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('select website, username, password from passwords where (id <> -1)')
        self.data = c.fetchall()
        c.execute('select id from passwords where (id <> -1)')
        self.rowIds = c.fetchall()
        #print(self.rowIds)
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

        self.table.setFixedWidth(619)

        self.layout.addWidget(self.table, 1, 0, 1, 4)

    def createRemoveBtns(self):
        self.remove_btns = []

        n = 0
        for i in range(self.table.rowCount()):
            try:
                self.remove_btns.append(remove_btn(self.rowIds[i + n][0], self.table, self.remove_btns, self.sql))
            except Exception:
                self.remove_btns.append(remove_btn(-1, self.table, self.remove_btns, self.sql))
            self.table.setCellWidget(i, 3, self.remove_btns[i])

    def addPassword(self):
        if all([self.newWebsite_le.text() != '', self.newUsername_le.text() != '', self.newPassword_le.text() != '']):
            n = self.table.rowCount()
            i = n
            while (n,) in self.rowIds:
                n += 1
                #print(n)
            self.rowIds.append((n,))
            self.sql.append('insert into passwords values ({}, \'{}\',\'{}\',\'{}\')'.format(n, self.newWebsite_le.text(), self.newUsername_le.text(), self.newPassword_le.text()))
            self.table.insertRow(i)
            self.table.setItem(i, 0, (QTableWidgetItem('* ' + self.newWebsite_le.text())))
            self.table.setItem(i, 1, (QTableWidgetItem('* ' + self.newUsername_le.text())))
            self.table.setItem(i, 2, (QTableWidgetItem('* ' + '*' * len(self.newPassword_le.text()))))

            self.newWebsite_le.setText('')
            self.newUsername_le.setText('')
            self.newPassword_le.setText('')

            #print(self.sql)
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
        c.execute('select website, username, password from passwords where (id <> -1)')
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
                self.table.setItem(i, j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(data))))

            copy_btns.append(copy_btn(i, self.data))
            self.table.setCellWidget(i, 3, copy_btns[i])

        self.table.setFixedWidth(619)

        self.layout.addWidget(self.table, 0, 0)

class copy_btn(QPushButton):
    def __init__(self, index, data):
        super().__init__()
        self.clicked.connect(lambda: pyperclip.copy(data[index][2]))

class remove_btn(QPushButton):
    def __init__(self, rowId, table, remove_btns, sql):
        super().__init__()
        self.setText('X')
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
        #print(self.sql)

def main():
    os.chdir(sys.path[0])

    app = QApplication(['Qt5PasswordManager'])

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    try:
        c.execute('create table passwords (id integer, website varchar(50), username varchar(50), password varchar(50))')
        c.close()
        conn.close()

        window = SetupWindow()
        window.show()

    except Exception as e:
        c.execute('select password from passwords where (id = -1)')
        key_hashed = c.fetchone()[0]
        c.close()
        conn.close()

        window = MainWindow(key_hashed)
        window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
