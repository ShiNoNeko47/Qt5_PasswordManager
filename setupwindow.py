from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import mysql.connector
from Crypto.Hash import SHA256
from config import Config
from messagebox import MessageBox

class SetupWindow(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow
        self.layout = QGridLayout()
        self.setWindowTitle('New user')
        self.setFixedHeight(150)
        self.setFixedWidth(600)

        self.username_setup_le = QLineEdit()
        self.username_setup_le.setPlaceholderText('New username')
        self.layout.addWidget(self.username_setup_le, 0, 0)

        self.key_setup_le = QLineEdit()
        self.key_setup_le.setEchoMode(QLineEdit.Password)
        self.key_setup_le.textChanged.connect(self.checkPassword)
        self.key_setup_le.setPlaceholderText('Master key')
        self.layout.addWidget(self.key_setup_le, 1, 0)

        self.key_reenter_le = QLineEdit()
        self.key_reenter_le.setEchoMode(QLineEdit.Password)
        self.key_reenter_le.textChanged.connect(self.checkPassword)
        self.key_reenter_le.setPlaceholderText('Confirm master key')
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

    def ok(self):
        try:
            conn = mysql.connector.connect(**Config.config())
            c = conn.cursor()
            c.execute('create table {}_ (id integer, website varchar(50), username varchar(50), password varchar(150))'.format(self.username_setup_le.text()))
            c.execute("insert into {}_ values (-1, \"Master\", \"Key\", \"{}\")".format(self.username_setup_le.text(), SHA256.new(str.encode(self.key_setup_le.text())).hexdigest()))
            c.execute('select password from {}_ where (id = -1)'.format(self.username_setup_le.text()))
            print(c.fetchall())
            conn.commit()
            c.close()
            conn.close()

            self.close()

            self.mainWindow.key_input.setText(self.key_setup_le.text())
            self.mainWindow.name_input.setText(self.username_setup_le.text())
        except mysql.connector.Error as x:
            if x.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                self.messagebox = MessageBox(self, 'ok', 'User already exists!')
            else:
                self.messagebox = MessageBox(self, 'ok', x.msg)

            self.messagebox.show()

    def resetEntries(self):
        self.username_setup_le.setText('')
        self.key_setup_le.setText('')
        self.key_reenter_le.setText('')

    def closeEvent(self, event):
        try:
            self.messagebox.close()
        except:
            pass
        self.resetEntries()
        event.accept()

