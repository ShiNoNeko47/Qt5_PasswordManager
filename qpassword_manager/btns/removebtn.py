from PyQt5.QtWidgets import QPushButton


class RemoveBtn(QPushButton):
    marked = []

    def __init__(self, row_id, remove_btns, window):
        super().__init__()

        self.window = window

        self.row_id = row_id
        self.remove_btns = remove_btns
        self.table = window.table
        self.actions = window.actions
        self.action = [self.row_id, "delete"]

        self.clicked.connect(self.remove_row)

        if self.row_id not in RemoveBtn.marked:
            self.setText("X")
        else:
            self.setText("-")

    def remove_row(self):
        if self.row_id not in RemoveBtn.marked:
            self.actions.append(self.action)
            self.setText("-")
            RemoveBtn.marked.append(self.row_id)
        else:
            del self.actions[self.actions.index(self.action)]
            self.setText("X")
            del RemoveBtn.marked[RemoveBtn.marked.index(self.row_id)]
        self.window.save_btn.setDisabled(not self.actions)
