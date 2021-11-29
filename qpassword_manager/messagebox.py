from PyQt5.QtWidgets import (QWidget,
                             QLabel,
                             QPushButton,
                             QGridLayout)
from PyQt5.Qt import Qt
from qpassword_manager.btns.removebtn import Remove_btn


class MessageBox(QWidget):
    def __init__(self, parentWindow, title):
        super().__init__()
        self.parentWindow = parentWindow

        self.setWindowTitle(title)
        self.layout = QGridLayout()

        self.label = QLabel()
        self.label.setText(title)
        self.layout.addWidget(self.label, 0, 0, 1, 3)

        self.ok_btn = QPushButton()
        self.ok_btn.setText('Ok')
        self.ok_btn.clicked.connect(self.ok)

        self.yes_btn = QPushButton()
        self.yes_btn.setText('Yes')
        self.yes_btn.clicked.connect(self.yes)

        self.no_btn = QPushButton()
        self.no_btn.setText('No')
        self.no_btn.clicked.connect(self.no)

        if title[-1] == '?':
            self.layout.addWidget(self.yes_btn, 1, 2)
            self.layout.addWidget(self.no_btn, 1, 0)
            self.default = self.yes_btn
        else:
            self.layout.addWidget(self.ok_btn, 1, 1)
            self.default = self.ok_btn
        self.setLayout(self.layout)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return:
            self.default.click()

    def ok(self):
        self.close()

    def yes(self):
        self.parentWindow.commit_changes()
        self.close()
        self.parentWindow.close()

    def no(self):
        self.parentWindow.sql.clear()
        Remove_btn.marked.clear()
        self.parentWindow.save_btn.setDisabled(True)
        self.close()
        self.parentWindow.close()
