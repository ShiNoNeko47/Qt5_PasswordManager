"""Settings window"""

from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QGridLayout
from PyQt5.Qt import Qt
from qpassword_manager.conf.connectorconfig import Config


class Settings(QWidget):
    """
    Settings window

    Attributes:
        config: configuration in json format
    """

    def __init__(self):
        super().__init__()
        self.config = Config.config()

        self.layout = QGridLayout()
        self.setWindowTitle("Settings")

        self.host_le = QLineEdit()
        self.host_le.setText(self.config["host"])
        self.host_le.textChanged.connect(self.check_ip)
        self.host_le.setPlaceholderText("Host")
        self.layout.addWidget(self.host_le, 0, 0, 1, 3)
        self.setMinimumWidth(320)

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.clicked.connect(self.config_update)
        self.layout.addWidget(self.ok_btn, 1, 1)

        self.setLayout(self.layout)

    def check_ip(self):
        """Checks if line edit is empty and enables or disables the button"""

        if self.host_le.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def config_update(self):
        """Updates configuration using Config.config_update method"""

        self.config["host"] = self.host_le.text()
        Config.config_update(self.config)
        self.close()

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Clicks ok button when you press enter"""

        if event.key() == Qt.Key_Return:
            self.ok_btn.click()
