from PyQt5.QtWidgets import *

class Edit_btn(QPushButton):
    marked = []
    def __init__(self, rowId, table, edit_btns, sql, window):
        super().__init__()
        self.table = table
        self.edit_btns = edit_btns
        self.clicked.connect(self.edit_row)
        self.rowId = rowId
        self.sql = sql
        self.w = window

    def edit_row(self):
        if self.rowId not in Edit_btn.marked:
            Edit_btn.marked.append(self.rowId)
            self.setText('<')
            for btn in self.edit_btns:
                if btn != self:
                    btn.setDisabled(True)
        else:
            Edit_btn.marked.clear()
            self.setText('')
            for btn in self.edit_btns:
                btn.setDisabled(False)

            if self.w.newWebsite_le.text():
                self.sql.append('update passwords set website=\'{}\' where id={}'.format(self.w.newWebsite_le.text(), self.rowId))
                self.setText('-')
                self.table.setItem(self.edit_btns.index(self), 0, (QTableWidgetItem('+ ' + self.w.newWebsite_le.text())))

            if self.w.newUsername_le.text():
                self.sql.append('update passwords set username=\'{}\' where id={}'.format(self.w.newUsername_le.text(), self.rowId))
                self.setText('-')
                self.table.setItem(self.edit_btns.index(self), 1, (QTableWidgetItem('+ ' + self.w.newUsername_le.text())))

            if all([self.w.newPassword_le.text(),
                self.w.newPassword_le.text() == self.w.reNewPassword_le.text(),]):
                self.sql.append('update passwords set password=\'{}\' where id={}'.format(self.w.f.encrypt(self.w.newPassword_le.text().encode()).decode(), self.rowId))
                self.setText('-')
                self.table.setItem(self.edit_btns.index(self), 2, (QTableWidgetItem('+ ' + '*' * len(self.w.newPassword_le.text()))))
            self.w.resetEntries()
