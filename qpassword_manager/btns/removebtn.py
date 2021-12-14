import logging
from PyQt5.QtWidgets import QPushButton


class Remove_btn(QPushButton):
    marked = []

    def __init__(self, rowId, table, remove_btns, actions, window):
        super().__init__()
        # logging.debug(Remove_btn.marked)
        self.table = table
        self.remove_btns = remove_btns
        self.clicked.connect(self.remove_row)
        self.rowId = rowId
        self.actions = actions
        self.w = window
        if self.rowId not in Remove_btn.marked:
            self.setText("X")
        else:
            self.setText("-")

    def remove_row(self):
        if self.rowId not in Remove_btn.marked:
            self.action = [self.rowId, "delete"]
            self.actions.append(self.action)
            self.setText("-")
            Remove_btn.marked.append(self.rowId)
        else:
            del self.actions[self.actions.index(self.action)]
            self.setText("X")
            del Remove_btn.marked[Remove_btn.marked.index(self.rowId)]
        self.w.save_btn.setDisabled(not self.actions)
