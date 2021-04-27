from PyQt5.QtWidgets import *
import sqlite3
from cryptography.fernet import Fernet
from removebtn import Remove_btn

class ManagePasswordsWindow(QWidget):
    def __init__(self, displayPasswordsWindow):
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

        self.displayPasswordsWindow = displayPasswordsWindow

    def setKey(self, key):
        self.f = Fernet(key)

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
                self.table.setItem(i, j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(self.f.decrypt(data.encode())))))

        self.createRemoveBtns()

        self.table.setFixedWidth(619)

        self.layout.addWidget(self.table, 1, 0, 1, 4)

    def createRemoveBtns(self):
        self.remove_btns = []

        for i in range(self.table.rowCount()):
            try:
                self.remove_btns.append(Remove_btn(self.rowIds[i][0], self.table, self.remove_btns, self.sql))
            except Exception:
                self.remove_btns.append(Remove_btn(-1, self.table, self.remove_btns, self.sql))
            self.table.setCellWidget(i, 3, self.remove_btns[i])

    def addPassword(self):
        if all([self.newWebsite_le.text() != '', self.newUsername_le.text() != '', self.newPassword_le.text() != '']):
            n = self.table.rowCount()
            i = n
            while (n,) in self.rowIds:
                n += 1
            self.rowIds.append((n,))
            self.sql.append('insert into passwords values ({}, \"{}\",\"{}\",\"{}\")'.format(n, self.newWebsite_le.text(), self.newUsername_le.text(), self.f.encrypt(self.newPassword_le.text().encode()).decode()))
            self.table.insertRow(i)
            self.table.setItem(i, 0, (QTableWidgetItem('+ ' + self.newWebsite_le.text())))
            self.table.setItem(i, 1, (QTableWidgetItem('+ ' + self.newUsername_le.text())))
            self.table.setItem(i, 2, (QTableWidgetItem('+ ' + '*' * len(self.newPassword_le.text()))))

            self.newWebsite_le.setText('')
            self.newUsername_le.setText('')
            self.newPassword_le.setText('')

            #print(self.sql)
            self.createRemoveBtns()

    def commitChanges(self):
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        for statement in self.sql:
            #print(statement)
            c.execute(statement)
        conn.commit()
        c.close()
        conn.close()
        self.createTable()
        self.displayPasswordsWindow.createTable()
        Remove_btn.marked.clear()

