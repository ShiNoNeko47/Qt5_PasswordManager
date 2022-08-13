"""MessageBox class"""
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.Qt import Qt


class MessageBox(QWidget):
    """
    MessageBox class

    Attributes:
        window_parent: parent window
    """

    def __init__(self, window_parent, title):
        super().__init__()
        self.window_parent = window_parent

        self.setWindowTitle(title)
        self.layout = QGridLayout()

        self.label = QLabel()
        self.label.setText(title)
        self.label.setWordWrap(True)
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
            self.default = None
        else:
            self.layout.addWidget(self.ok_btn, 1, 1)
            self.default = self.ok_btn

        self.setLayout(self.layout)

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Clicks \"yes\" if you press enter"""

        if event.key() == Qt.Key_Return:
            if self.default:
                self.default.click()

        elif event.key() == Qt.Key_Y:
            self.choice_yes()

        elif event.key() == Qt.Key_N:
            self.choice_no()

    def choice_ok(self):
        """Closes MessageBox"""

        self.close()

    def choice_yes(self):
        """Closes MessageBox and sends 1 to messagebox handler"""

        self.window_parent.messagebox_handler(1)
        self.close()

    def choice_no(self):
        """Closes MessageBox and sends 0 to messagebox handler"""

        self.window_parent.messagebox_handler(0)
        self.close()
