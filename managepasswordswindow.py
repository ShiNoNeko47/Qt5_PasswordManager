from PyQt5.QtWidgets import *
import mysql.connector
from cryptography.fernet import Fernet
from removebtn import Remove_btn
from editbtn import Edit_btn
from PyQt5.QtCore import QSettings, QPoint
from messagebox import MessageBox

class ManagePasswordsWindow(QWidget):
    def __init__(self, displayPasswordsWindow, btn, config):
        super().__init__()
        self.btn = btn
        self.config = config
        self.setWindowTitle('Manage Passwords')
        self.layout = QGridLayout()

        self.newWebsite_le = QLineEdit()
        self.newWebsite_le.textChanged.connect(self.validInputCheck)
        self.newWebsite_le.setPlaceholderText('Website:')
        self.layout.addWidget(self.newWebsite_le, 0, 0, 2, 1)

        self.newUsername_le = QLineEdit()
        self.newUsername_le.setPlaceholderText('Username:')
        self.newUsername_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.newUsername_le, 0, 1, 2, 1)

        self.newPassword_le = QLineEdit()
        self.newPassword_le.setPlaceholderText('Password:')
        self.newPassword_le.setEchoMode(QLineEdit.Password)
        self.newPassword_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.newPassword_le, 0, 2)

        self.reNewPassword_le = QLineEdit()
        self.reNewPassword_le.setPlaceholderText('Confirm Password:')
        self.reNewPassword_le.setEchoMode(QLineEdit.Password)
        self.reNewPassword_le.textChanged.connect(self.validInputCheck)
        self.layout.addWidget(self.reNewPassword_le, 1, 2)

        self.add_btn = QPushButton('Add')
        self.add_btn.clicked.connect(self.addPassword)
        self.add_btn.setDisabled(True)
        self.layout.addWidget(self.add_btn, 0, 3, 2, 1)

        self.save_btn = QPushButton('Save')
        self.save_btn.setDisabled(True)
        self.save_btn.clicked.connect(self.commitChanges)
        self.layout.addWidget(self.save_btn, 3, 3)

        self.setLayout(self.layout)
        self.setFixedWidth(640)

        self.displayPasswordsWindow = displayPasswordsWindow

        self.messageBox = MessageBox(self)

    def setKey(self, key):
        self.f = Fernet(key)

    def createTable(self):
        self.sql = []

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Password', '', ''])

        conn = mysql.connector.connect(**self.config)
        c = conn.cursor()
        print(self.user)
        c.execute('select website, username, password from {}_ where (id <> -1)'.format(self.user))
        self.data = c.fetchall()
        c.execute('select id from {}_ where (id <> -1)'.format(self.user))
        self.rowIds = c.fetchall()
        #print(self.rowIds)
        c.close()
        conn.close()

        for i in range(3):
            self.table.setColumnWidth(i, 180)
        self.table.setColumnWidth(3, 30)
        self.table.setColumnWidth(4, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for row, i in zip(self.data, range(len(self.data))):
            self.table.insertRow(i)
            for data, j in zip(row, range(3)):
                self.table.setItem(i, j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(self.f.decrypt(data.encode())))))

        self.number_or_ids = len(self.rowIds)

        self.createBtns()

        self.table.setFixedWidth(620)

        self.layout.addWidget(self.table, 2, 0, 1, 4)

    def createBtns(self):
        self.remove_btns = []
        self.edit_btns = []

        for i in range(self.table.rowCount()):
            try:
                self.remove_btns.append(Remove_btn(self.rowIds[i][0], self.table, self.remove_btns, self.sql, self))
                self.edit_btns.append(Edit_btn(self.rowIds[i][0], self.edit_btns, self))
            except Exception:
                self.remove_btns.append(Remove_btn(-1, self.table, self.remove_btns, self.sql, self))
                self.edit_btns.append(Edit_btn(-1, self.edit_btns, self))
                print(-1)
            if i < self.number_or_ids:
                self.table.setCellWidget(i, 3, self.edit_btns[i])
            self.table.setCellWidget(i, 4, self.remove_btns[i])

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
            self.sql.append('insert into {}_ values ({}, \"{}\",\"{}\",\"{}\")'.format(self.user,
                n,
                self.newWebsite_le.text(),
                self.newUsername_le.text(),
                self.f.encrypt(self.newPassword_le.text().encode()).decode()
            ))

            self.save_btn.setDisabled(not self.sql)

            self.table.insertRow(i)
            self.table.setItem(i, 0, (QTableWidgetItem('+ ' + self.newWebsite_le.text())))
            self.table.setItem(i, 1, (QTableWidgetItem('+ ' + self.newUsername_le.text())))
            self.table.setItem(i, 2, (QTableWidgetItem('+ ' + '*' * len(self.newPassword_le.text()))))

            self.newWebsite_le.setText('')
            self.newUsername_le.setText('')
            self.newPassword_le.setText('')
            self.reNewPassword_le.setText('')

            #print(self.sql)
            self.createBtns()

    def commitChanges(self):
        conn = mysql.connector.connect(**self.config)
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
        self.save_btn.setDisabled(True)
        self.sql.clear()

    def resetEntries(self):
        self.newWebsite_le.setText('')
        self.newUsername_le.setText('')
        self.newPassword_le.setText('')
        self.reNewPassword_le.setText('')

    def closeEvent(self, event):
        if not self.sql:
            self.btn.setDisabled(False)
            self.resetEntries()
            event.accept()
        else:
            event.ignore()
            self.messageBox.close()
            self.messageBox.show()

