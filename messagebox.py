from PyQt5.QtWidgets import *
from removebtn import Remove_btn

class MessageBox(QWidget):
    def __init__(self, managePasswordsWindow, mode = 'yes/no', title = 'Save changes?'):
        super().__init__()
        self.managePasswordsWindow = managePasswordsWindow

        self.setWindowTitle(title)
        self.layout = QGridLayout()

        self.label = QLabel()
        self.label.setText(title)
        self.layout.addWidget(self.label, 0, 0, 1, 2)

        self.ok_btn = QPushButton()
        self.ok_btn.setText('Ok')
        self.ok_btn.clicked.connect(self.ok)

        self.yes_btn = QPushButton()
        self.yes_btn.setText('Yes')
        self.yes_btn.clicked.connect(self.save)

        self.no_btn = QPushButton()
        self.no_btn.setText('No')
        self.no_btn.clicked.connect(self.not_save)

        if mode == 'yes/no':
            self.layout.addWidget(self.yes_btn, 1, 1)
            self.layout.addWidget(self.no_btn, 1, 0)
        elif mode == 'ok':
            self.layout.addWidget(self.ok_btn, 1, 0)

        self.setLayout(self.layout)

    def ok(self):
        self.close()

    def save(self):
        self.managePasswordsWindow.commitChanges()
        self.close()
        self.managePasswordsWindow.close()

    def not_save(self):
        self.managePasswordsWindow.sql.clear()
        Remove_btn.marked.clear()
        self.managePasswordsWindow.save_btn.setDisabled(True)
        self.close()
        self.managePasswordsWindow.close()
