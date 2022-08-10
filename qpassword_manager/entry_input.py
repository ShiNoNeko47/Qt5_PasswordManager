from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QLineEdit


class NewPasswordInput(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setEchoMode(QLineEdit.Password)

        self.other_text = ""

    def switch_values(self):
        text = self.other_text
        self.other_text = self.text()
        self.setText(text)

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.switch_values()
            return True
        return QLineEdit.event(self, event)


class NewWebsiteInput(QLineEdit):
    def __init__(self):
        super().__init__()

    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Backtab:
            return True
        return QLineEdit.event(self, event)
