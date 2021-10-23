from PyQt5.QtWidgets import *
import mysql.connector
from cryptography.fernet import Fernet
from copybtn import Copy_btn

class ShowPasswordsWindow(QWidget):
    def __init__(self, btn, config):
        super().__init__()
        self.config = config

        self.btn = btn
        self.setWindowTitle('Passwords')
        self.layout = QGridLayout()

        self.setFixedWidth(640)
        self.setLayout(self.layout)

    def setKey(self, key):
        self.f = Fernet(key)

    def createTable(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website', 'Username', 'Password', ''])

        conn = mysql.connector.connect(**self.config)
        c = conn.cursor()
        c.execute('select website, username, password from {}_ where (id <> -1)'.format(self.user))
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
                self.table.setItem(i, j, (QTableWidgetItem(data) if j != 2 else QTableWidgetItem('*'*len(self.f.decrypt(data.encode())))))

            copy_btns.append(Copy_btn(i, self.data, self.f))
            self.table.setCellWidget(i, 3, copy_btns[i])

        self.table.setFixedWidth(619)

        self.layout.addWidget(self.table, 0, 0)

    def closeEvent(self, event):
        self.btn.setDisabled(False)
