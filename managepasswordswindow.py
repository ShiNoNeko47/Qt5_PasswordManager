from PyQt5.QtWidgets import *
import sqlite3
from cryptography.fernet import Fernet
from removebtn import Remove_btn

class ManagePasswordsWindow(QWidget):
    def __init__(self, displayPasswordsWindow, btn):
        super().__init__()
        self.btn = btn
        self.setWindowTitle('Manage Passwords')
        self.layout = QGridLayout()

        self.newWebsite_le = QLineEdit()
        self.newWebsite_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.newWebsite_le, 0, 0, 2, 1)

        self.newUsername_le = QLineEdit()
        self.newUsername_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.newUsername_le, 0, 1, 2, 1)

        self.newPassword_le = QLineEdit()
        self.newPassword_le.setEchoMode(QLineEdit.Password)
        self.newPassword_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.newPassword_le, 0, 2)

        self.reNewPassword_le = QLineEdit()
        self.reNewPassword_le.setEchoMode(QLineEdit.Password)
        self.reNewPassword_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.reNewPassword_le, 1, 2)

        self.add_btn = QPushButton('Add')
        self.add_btn.clicked.connect(self.addPassword)
        self.add_btn.setDisabled(True)
        self.layout.addWidget(self.add_btn, 0, 3, 2, 1)

        self.save_btn = QPushButton('Save')
        self.save_btn.clicked.connect(self.commitChanges)
        self.layout.addWidget(self.save_btn, 3, 3)

        self.setLayout(self.layout)
        self.setFixedWidth(640)

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

        self.layout.addWidget(self.table, 2, 0, 1, 4)

    def createRemoveBtns(self):
        self.remove_btns = []

        for i in range(self.table.rowCount()):
            try:
                self.remove_btns.append(Remove_btn(self.rowIds[i][0], self.table, self.remove_btns, self.sql))
            except Exception:
                self.remove_btns.append(Remove_btn(-1, self.table, self.remove_btns, self.sql))
            self.table.setCellWidget(i, 3, self.remove_btns[i])

    def validInputCheck(self):
        check = [all([self.newWebsite_le.text() != '',
            self.newUsername_le.text() != '',
            self.newPassword_le.text() != '',
            self.reNewPassword_le.text() != '']),
            self.newPassword_le.text() == self.reNewPassword_le.text()]
        if all(check):
            self.add_btn.setDisabled(False)
            self.add_btn.setToolTip('')
            return True
        self.add_btn.setDisabled(True)
        self.req_notMet = list(map(lambda x: x[1:], filter(lambda x: not check[int(x[0])], [
            '0Don\'t leave empty fields!',
            '1Passwords don\'t match!'])))
        tooltip = ''
        for i, j in zip(self.req_notMet, ['', '\n']):
            tooltip = tooltip + j + i
        self.add_btn.setToolTip(tooltip)

    def addPassword(self):
        if self.validInputCheck():
            n = self.table.rowCount()
            i = n
            while (n,) in self.rowIds:
                n += 1
            self.rowIds.append((n,))
            self.sql.append('insert into passwords values ({}, \"{}\",\"{}\",\"{}\")'.format(n,
                self.newWebsite_le.text(),
                self.newUsername_le.text(),
                self.f.encrypt(self.newPassword_le.text().encode()).decode()
            ))

            self.table.insertRow(i)
            self.table.setItem(i, 0, (QTableWidgetItem('+ ' + self.newWebsite_le.text())))
            self.table.setItem(i, 1, (QTableWidgetItem('+ ' + self.newUsername_le.text())))
            self.table.setItem(i, 2, (QTableWidgetItem('+ ' + '*' * len(self.newPassword_le.text()))))

            self.newWebsite_le.setText('')
            self.newUsername_le.setText('')
            self.newPassword_le.setText('')
            self.reNewPassword_le.setText('')

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
    def closeEvent(self, event):
        self.btn.setDisabled(False)
        self.newWebsite_le.setText('')
        self.newUsername_le.setText('')
        self.newPassword_le.setText('')
        self.reNewPassword_le.setText('')

