from PyQt5.QtWidgets import QPushButton
import mysql.connector
from conf.connectorconfig import Config


class Edit_btn(QPushButton):
    def __init__(self, rowId, edit_btns, window):
        super().__init__()
        self.rowId = rowId
        self.edit_btns = edit_btns
        self.w = window
        self.clicked.connect(self.edit_row)
        self.f = self.w.f
        self.setText('+')

    def edit_row(self):
        if self.text() == '+':
            for btn in self.edit_btns:
                btn.setText('+')

            self.setText('-')
            conn = mysql.connector.connect(**Config.config())
            c = conn.cursor()
            c.execute("""select Website, Username, Password
                         from Passwords
                         where
                         (ID = \'{}\' and Deleted = 0)"""
                      .format(self.rowId))

            row = c.fetchone()
            c.close()
            conn.close()

            self.w.newWebsite_le.setText(row[0])
            self.w.newUsername_le.setText(row[1])
            self.w.newPassword_le.setText(self.f.decrypt(row[2]).decode())
            self.w.reNewPassword_le.setText(self.f.decrypt(row[2]).decode())

        else:
            self.setText('+')
            self.w.resetEntries()
