"""Settings window"""

from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QLineEdit,
    QFormLayout,
    QVBoxLayout,
    QRadioButton,
)
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
        self.setWindowTitle("Settings")

        self.layout_vbox = QVBoxLayout()

        self.radiobutton_offline = QRadioButton("Offline database")
        self.layout_vbox.addWidget(self.radiobutton_offline)
        self.radiobutton_online = QRadioButton("Online database")
        self.layout_vbox.addWidget(self.radiobutton_online)

        if self.config["database_online"]:
            self.radiobutton_online.setChecked(True)
        else:
            self.radiobutton_offline.setChecked(True)

        self.layout_form = QFormLayout()
        self.layout_vbox.addLayout(self.layout_form)

        self.url_le = QLineEdit()
        self.url_le.setText(self.config["url"])
        self.url_le.textChanged.connect(self.check_ip)
        self.layout_form.addRow("url: ", self.url_le)

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.clicked.connect(self.config_update)
        self.layout_vbox.addWidget(self.ok_btn)

        self.setLayout(self.layout_vbox)

    def check_ip(self):
        """Checks if line edit is empty and enables or disables the button"""

        if self.url_le.text() != "":
            self.ok_btn.setEnabled(True)
        else:
            self.ok_btn.setEnabled(False)

    def config_update(self):
        """Updates configuration using Config.config_update method"""

        self.config["url"] = self.url_le.text()
        self.config["database_online"] = self.radiobutton_online.isChecked()
        Config.config_update(self.config)
        self.close()

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Clicks ok button when you press enter"""

        if event.key() == Qt.Key_Return:
            self.ok_btn.click()
