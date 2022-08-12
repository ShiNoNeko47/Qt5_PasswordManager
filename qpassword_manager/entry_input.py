"""QLineEdits in entry_input in password_table"""

from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QLineEdit


class NewPasswordInput(QLineEdit):
    """
    QLineEdit for password input
    It has two values that have to match
    You can switch between the value you input with tab
    """

    def __init__(self):
        super().__init__()
        self.setEchoMode(QLineEdit.Password)

        self.other_text = ""

    def switch_values(self):
        """Switches values"""

        text = self.other_text
        self.other_text = self.text()
        self.setText(text)

    def event(self, event):
        """Calls switch_values when tab is pressed"""

        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.switch_values()
            return True
        return QLineEdit.event(self, event)


class NewWebsiteInput(QLineEdit):
    """First QLineEdit in entry_input"""

    def event(self, event):
        """Ignores shift + tab"""

        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Backtab:
            return True
        return QLineEdit.event(self, event)
