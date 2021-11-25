from PyQt5.QtWidgets import QPushButton


class Remove_btn(QPushButton):
    marked = []

    def __init__(self, rowId, table, remove_btns, sql, window):
        super().__init__()
        # print(Remove_btn.marked)
        self.table = table
        self.remove_btns = remove_btns
        self.clicked.connect(self.remove_row)
        self.rowId = rowId
        self.sql = sql
        self.w = window
        if self.rowId not in Remove_btn.marked:
            self.setText('X')
        else:
            self.setText('-')

    def remove_row(self):
        if self.rowId not in Remove_btn.marked:
            self.statement = """update Passwords
                                set
                                Deleted = 1
                                where
                                (ID = {})""".format(self.rowId)
            self.sql.append(self.statement)
            self.setText('-')
            Remove_btn.marked.append(self.rowId)
        else:
            del self.sql[self.sql.index(self.statement)]
            self.setText('X')
            del Remove_btn.marked[Remove_btn.marked.index(self.rowId)]
        self.w.save_btn.setDisabled(not self.sql)
        # print(self.sql)
