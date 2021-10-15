from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import sqlite3
from Crypto.Hash import SHA256

class SetupWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        try:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE type='table'")
            self.userList = c.fetchall()[0]
            #c.execute('drop table passwords;')
            #conn.commit()
            c.close()
            conn.close()
        except:
            self.userList = ()

        self.layout = QGridLayout()
        self.setWindowTitle('New user')
        self.setFixedHeight(150)
        self.setFixedWidth(600)

        self.username_setup_le = QLineEdit()
        self.username_setup_le.textChanged.connect(self.checkName)
        self.layout.addWidget(self.username_setup_le, 0, 0)

        self.key_setup_le = QLineEdit()
        self.key_setup_le.setEchoMode(QLineEdit.Password)
        self.key_setup_le.textChanged.connect(self.checkPassword)
        self.layout.addWidget(self.key_setup_le, 1, 0)

        self.key_reenter_le = QLineEdit()
        self.key_reenter_le.setEchoMode(QLineEdit.Password)
        self.key_reenter_le.textChanged.connect(self.checkPassword)
        self.layout.addWidget(self.key_reenter_le, 2, 0)

        self.ok_btn = QPushButton('Ok')
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.ok)
        self.layout.addWidget(self.ok_btn, 2, 1)

        self.setLayout(self.layout)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.ok_btn.click()

    def checkPassword(self):
        self.ok_btn.setEnabled(False)
        if all([self.key_setup_le.text() == self.key_reenter_le.text(), len(self.key_setup_le.text()) > 3]):
            self.ok_btn.setEnabled(True)

    def checkName(self):
        #self.ok_btn.setEnabled(False)
        pass

    def ok(self):
        self.close()

        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('create table {} (id integer, website varchar(50), username varchar(50), password varchar(50))'.format(self.username_setup_le.text()))
        c.execute("insert into {} values (-1, \"Master\", \"Key\", \"{}\")".format(self.username_setup_le.text(), SHA256.new(str.encode(self.key_setup_le.text())).hexdigest()))
        c.execute('select password from {} where (id = -1)'.format(self.username_setup_le.text()))
        print(c.fetchall())
        conn.commit()
        c.close()
        conn.close()

        self.mainWindow.key_input.setText(self.key_setup_le.text())
        self.mainWindow.name_input.setText(self.username_setup_le.text())

