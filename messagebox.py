from PyQt5.QtWidgets import *

class MessageBox(QWidget):
    def __init__(self, managePasswordsWindow):
        super().__init__()
        self.managePasswordsWindow = managePasswordsWindow

        self.setWindowTitle('Commit changes?')
        self.layout = QGridLayout()

        self.label = QLabel()
        self.label.setText('Commit changes?')
        self.layout.addWidget(self.label, 0, 0, 1, 2)

        self.yes_btn = QPushButton()
        self.yes_btn.setText('Yes')
        self.yes_btn.clicked.connect(self.save)
        self.layout.addWidget(self.yes_btn, 1, 1)

        self.no_btn = QPushButton()
        self.no_btn.setText('No')
        self.no_btn.clicked.connect(self.not_save)
        self.layout.addWidget(self.no_btn, 1, 0)

        self.setLayout(self.layout)

    def save(self):
        self.managePasswordsWindow.commitChanges()
        self.close()
        self.managePasswordsWindow.close()

    def not_save(self):
        self.managePasswordsWindow.sql.clear()
        self.close()
        self.managePasswordsWindow.close()
