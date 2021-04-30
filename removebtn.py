from PyQt5.QtWidgets import *
from editbtn import Edit_btn

class Remove_btn(QPushButton):
    marked = []
    def __init__(self, rowId, table, remove_btns, sql, window):
        super().__init__()
        self.w = window
        self.table = table
        self.remove_btns = remove_btns
        self.clicked.connect(self.remove_row)
        self.rowId = rowId
        self.sql = sql
        if self.rowId not in Remove_btn.marked:
            self.setText('X')
        else:
            self.setText('-')

    def remove_row(self):
        if self.rowId not in Edit_btn.marked:
            if self.rowId not in Remove_btn.marked:
                if self.rowId >= 0:
                    self.sql.append('delete from passwords where id={}'.format(self.rowId))
                    self.setText('-')
                    Remove_btn.marked.append(self.rowId)
            else:
                del self.sql[self.sql.index('delete from passwords where id={}'.format(self.rowId))]
                self.setText('X')
                del Remove_btn.marked[Remove_btn.marked.index(self.rowId)]
        else:
            i = 0
            while i < len(self.sql):
                if 'where id={}'.format(self.rowId) in self.sql[i]:
                    del self.sql[i]
                    print(self.sql)
                else:
                    i += 1
            self.w.edit_btns[self.remove_btns.index(self)].setText('')
            self.w.update_row(self.remove_btns.index(self))
            del Edit_btn.marked[Edit_btn.marked.index(self.rowId)]
            print(self.remove_btns.index(self))
            for btn in self.w.edit_btns:
                btn.setDisabled(False)
        print(self.sql)
        self.w.save_btn.setDisabled(not self.sql)

