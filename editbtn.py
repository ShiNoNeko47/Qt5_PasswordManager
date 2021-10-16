from PyQt5.QtWidgets import *
import sqlite3

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
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute('select * from \"{}\" where id={}'.format(self.w.user, self.rowId))
            row = c.fetchone()
            c.close()
            conn.close()

            self.w.newWebsite_le.setText(row[1])
            self.w.newUsername_le.setText(row[2])
            self.w.newPassword_le.setText(self.f.decrypt(row[3].encode()).decode())
            self.w.reNewPassword_le.setText(self.f.decrypt(row[3].encode()).decode())
        else:
            self.setText('+')
            self.w.resetEntries()
