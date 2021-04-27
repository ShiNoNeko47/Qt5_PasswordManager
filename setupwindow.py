from PyQt5.QtWidgets import *
import sqlite3
from Crypto.Hash import SHA256
from mainwindow import MainWindow

class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('drop table passwords')
        conn.commit()
        c.close()
        conn.close()

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
        c.execute('create table passwords (id integer, website varchar(50), username varchar(50), password varchar(50))')
        c.execute("insert into passwords values (-1, \"Master\", \"Key\", \"{}\")".format(SHA256.new(str.encode(self.key_setup_le.text())).hexdigest()))
        conn.commit()
        c.close()
        conn.close()

        self.window = MainWindow(SHA256.new(str.encode(self.key_setup_le.text())).hexdigest(), self.key_setup_le.text())
        self.window.show()

