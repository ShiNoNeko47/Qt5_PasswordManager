from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.Qt import Qt


class MessageBox(QWidget):
    def __init__(self, window_parent, title):
        super().__init__()
        self.window_parent = window_parent

        self.setWindowTitle(title)
        self.layout = QGridLayout()

        self.label = QLabel()
        self.label.setText(title)
        self.layout.addWidget(self.label, 0, 0, 1, 3)

        self.ok_btn = QPushButton()
        self.ok_btn.setText("Ok")
        self.ok_btn.clicked.connect(self.choice_ok)

        self.yes_btn = QPushButton()
        self.yes_btn.setText("Yes")
        self.yes_btn.clicked.connect(self.choice_yes)

        self.no_btn = QPushButton()
        self.no_btn.setText("No")
        self.no_btn.clicked.connect(self.choice_no)

        if title[-1] == "?":
            self.layout.addWidget(self.yes_btn, 1, 2)
            self.layout.addWidget(self.no_btn, 1, 0)
            self.default = self.yes_btn
        else:
            self.layout.addWidget(self.ok_btn, 1, 1)
            self.default = self.ok_btn
        self.setLayout(self.layout)

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        if event.key() == Qt.Key_Return:
            self.default.click()

    def choice_ok(self):
        self.close()

    def choice_yes(self):
        self.window_parent.messagebox_handler(1)
        self.close()

    def choice_no(self):
        self.window_parent.messagebox_handler(0)
        self.close()
