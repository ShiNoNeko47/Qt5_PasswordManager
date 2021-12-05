from PyQt5.QtWidgets import (QWidget,
                             QGridLayout,
                             QLineEdit,
                             QPushButton,
                             QTableWidget,
                             QTableWidgetItem,
                             QAbstractItemView)
import requests
from cryptography.fernet import Fernet
from qpassword_manager.messagebox import MessageBox
from qpassword_manager.btns.removebtn import Remove_btn
from qpassword_manager.btns.editbtn import Edit_btn
from conf.connectorconfig import Config


class ManagePasswordsWindow(QWidget):
    def __init__(self, displayPasswordsWindow, btn):
        super().__init__()
        self.btn = btn
        self.setWindowTitle('Manage Passwords')
        self.layout = QGridLayout()

        self.newWebsite_le = QLineEdit()
        self.newWebsite_le.textChanged.connect(self.valid_input_check)
        self.newWebsite_le.setPlaceholderText('Website')
        self.layout.addWidget(self.newWebsite_le, 0, 0, 2, 1)

        self.newUsername_le = QLineEdit()
        self.newUsername_le.setPlaceholderText('Username')
        self.newUsername_le.textChanged.connect(self.valid_input_check)
        self.layout.addWidget(self.newUsername_le, 0, 1, 2, 1)

        self.newPassword_le = QLineEdit()
        self.newPassword_le.setPlaceholderText('Password')
        self.newPassword_le.setEchoMode(QLineEdit.Password)
        self.newPassword_le.textChanged.connect(self.valid_input_check)
        self.layout.addWidget(self.newPassword_le, 0, 2)

        self.reNewPassword_le = QLineEdit()
        self.reNewPassword_le.setPlaceholderText('Confirm Password')
        self.reNewPassword_le.setEchoMode(QLineEdit.Password)
        self.reNewPassword_le.textChanged.connect(self.valid_input_check)
        self.layout.addWidget(self.reNewPassword_le, 1, 2)

        self.add_btn = QPushButton('Add')
        self.add_btn.clicked.connect(self.add_password)
        self.add_btn.setDisabled(True)
        self.layout.addWidget(self.add_btn, 0, 3, 2, 1)

        self.save_btn = QPushButton('Save')
        self.save_btn.setDisabled(True)
        self.save_btn.clicked.connect(self.commit_changes)
        self.layout.addWidget(self.save_btn, 3, 3)

        self.setLayout(self.layout)
        self.setFixedWidth(640)

        self.displayPasswordsWindow = displayPasswordsWindow

        self.messagebox = MessageBox(self, 'Save changes?')

    def messagebox_handler(self, choice):
        if choice == 1:
            self.commit_changes()
            self.close()
        else:
            self.actions.clear()
            Remove_btn.marked.clear()
            self.save_btn.setDisabled(True)
            self.close()

    def set_key(self, key):
        self.f = Fernet(key)

    def create_table(self):
        self.actions = []

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(['Website',
                                              'Username',
                                              'Password',
                                              '',
                                              ''])
        self.r = requests.post(Config.config()['host'],
                               {'action': 'create_table'},
                               auth=self.auth)
        print(self.r.json())
        self.data = self.r.json()

        self.r = requests.post(Config.config()['host'],
                               {'action': 'get_pass_ids'},
                               auth=self.auth)
        print(self.r.json())
        self.rowIds = self.r.json()

        for i in range(3):
            self.table.setColumnWidth(i, 180)
        self.table.setColumnWidth(3, 30)
        self.table.setColumnWidth(4, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        for row, i in zip(self.data, range(len(self.data))):
            self.table.insertRow(i)
            for j in range(2):
                data = row[str(j)]
                print(data)
                self.table.setItem(i, j, (QTableWidgetItem(data)))
            data = '*' * len(self.f.decrypt(row['2'].encode()))
            self.table.setItem(i, 2, (QTableWidgetItem(data)))
        self.create_btns()

        self.table.setFixedWidth(620)

        self.layout.addWidget(self.table, 2, 0, 1, 4)

    def create_btns(self):
        self.remove_btns = []
        self.edit_btns = []

        for i in range(len(self.rowIds)):
            self.edit_btns.append(Edit_btn(self.rowIds[i],
                                           self.edit_btns,
                                           self))
            self.table.setCellWidget(i, 3, self.edit_btns[i])
            self.remove_btns.append(Remove_btn(self.rowIds[i],
                                               self.table,
                                               self.remove_btns,
                                               self.actions,
                                               self))
            self.table.setCellWidget(i, 4, self.remove_btns[i])

    def valid_input_check(self):
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
        self.req_notMet = list(map(lambda x: x[1:],
                                   filter(lambda x: not check[int(x[0])],
                                   ['0Don\'t leave empty fields!',
                                    '1Passwords don\'t match!'])))
        tooltip = ''
        for i, j in zip(self.req_notMet, ['', '\n']):
            tooltip = tooltip + j + i
        self.add_btn.setToolTip(tooltip)

    def add_password(self):
        if self.valid_input_check():
            self.actions.append([self.newWebsite_le.text(),
                                 self.newUsername_le.text(),
                                 self.f.encrypt(self.newPassword_le.text()
                                                .encode()).decode(),
                                 'add'])

            self.save_btn.setDisabled(not self.actions)

            n = self.table.rowCount()
            self.table.insertRow(n)

            website = self.newWebsite_le.text()
            self.table.setItem(n, 0, (QTableWidgetItem('+ ' + website)))

            username = self.newUsername_le.text()
            self.table.setItem(n, 1, (QTableWidgetItem('+ ' + username)))

            password = '*' * len(self.newPassword_le.text())
            self.table.setItem(n, 2, (QTableWidgetItem('+ ' + password)))

            self.newWebsite_le.setText('')
            self.newUsername_le.setText('')
            self.newPassword_le.setText('')
            self.reNewPassword_le.setText('')

            self.create_btns()

    def commit_changes(self):
        for action in self.actions:
            if action.pop() == 'add':
                self.r = requests.post(Config.config()['host'],
                                       {'action': 'add',
                                        'password': action[2],
                                        'username': action[1],
                                        'website': action[0]},
                                       auth=self.auth)
            else:
                self.r = requests.post(Config.config()['host'],
                                       {'action': 'delete',
                                        'id': action},
                                       auth=self.auth)
            print(self.r.text)

        Remove_btn.marked.clear()
        self.actions.clear()

        self.create_table()
        self.displayPasswordsWindow.create_table()
        self.save_btn.setDisabled(True)

    def reset_entries(self):
        self.newWebsite_le.setText('')
        self.newUsername_le.setText('')
        self.newPassword_le.setText('')
        self.reNewPassword_le.setText('')

    def closeEvent(self, event):
        if not self.actions:
            self.btn.setDisabled(False)
            self.reset_entries()
            event.accept()
        else:
            event.ignore()
            self.messagebox.close()
            self.messagebox.show()
