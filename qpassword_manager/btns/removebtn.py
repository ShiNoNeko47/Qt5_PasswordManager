"""RemoveBtn class"""

from PyQt5.QtWidgets import QPushButton


class RemoveBtn(QPushButton):
    """
    Button that removes a row from database

    Attributes:
        window: parent window (ManagePasswordsWindow)
        row_id: id of the row in database this button can delete
        actions: list of actions in queue
        action: item to add or remove from queue
    """

    marked = []

    def __init__(self, row_id, window):
        super().__init__()

        self.window = window

        self.row_id = row_id
        self.actions = window.actions
        self.action = [self.row_id, "delete"]

        self.clicked.connect(self.remove_row)

        if self.row_id not in RemoveBtn.marked:
            self.setText("X")
        else:
            self.setText("-")

    def remove_row(self):
        """Controlls button text (X or -) and adds delete action to queue"""

        if self.row_id not in RemoveBtn.marked:
            self.actions.append(self.action)
            self.setText("-")
            RemoveBtn.marked.append(self.row_id)
        else:
            del self.actions[self.actions.index(self.action)]
            self.setText("X")
            del RemoveBtn.marked[RemoveBtn.marked.index(self.row_id)]
        self.window.save_btn.setDisabled(not self.actions)
