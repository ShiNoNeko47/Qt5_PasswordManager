import logging
import requests
from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
from cryptography.fernet import Fernet
from qpassword_manager.btns.copybtn import CopyBtn
from qpassword_manager.conf.connectorconfig import Config


class DisplayPasswordsWindow(QWidget):
    def __init__(self, btn):
        super().__init__()

        self.fernet = None
        self.btn = btn

        self.setWindowTitle("Passwords")
        self.layout = QGridLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table, 0, 0)

        self.setFixedWidth(640)
        self.setLayout(self.layout)

    def set_key(self, key):
        self.fernet = Fernet(key)

    def create_table(self):
        self.table.clear()
        self.table.setColumnCount(4)
        self.table.setRowCount(0)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(
            ["Website", "Username", "Password", ""]
        )
        data = requests.post(
            Config.config()["host"], {"action": "create_table"}, auth=self.auth
        ).json()
        logging.debug(data)

        for i in range(3):
            self.table.setColumnWidth(i, 190)
        self.table.setColumnWidth(3, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        copy_btns = []
        for i, row in enumerate(data):
            self.table.insertRow(i)
            for j in range(2):
                self.table.setItem(i, j, (QTableWidgetItem(row[str(j)])))
            row = "*" * len(self.fernet.decrypt(row["2"].encode()))
            self.table.setItem(i, 2, (QTableWidgetItem(row)))
            copy_btns.append(CopyBtn(i, data, self.fernet))
            self.table.setCellWidget(i, 3, copy_btns[i])

        self.table.setFixedWidth(619)

    def closeEvent(self, event):  # pylint: disable=invalid-name
        self.btn.setDisabled(False)
        logging.debug(event)
