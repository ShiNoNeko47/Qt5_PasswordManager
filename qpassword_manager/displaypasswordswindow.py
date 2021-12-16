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
from qpassword_manager.btns.copybtn import Copy_btn
from qpassword_manager.conf.connectorconfig import Config


class DisplayPasswordsWindow(QWidget):
    def __init__(self, btn):
        super().__init__()

        self.f = None
        self.btn = btn

        self.setWindowTitle("Passwords")
        self.layout = QGridLayout()

        self.table = QTableWidget()
        self.layout.addWidget(self.table, 0, 0)

        self.setFixedWidth(640)
        self.setLayout(self.layout)

    def set_key(self, key):
        self.f = Fernet(key)

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
        for row, i in zip(data, range(len(data))):
            self.table.insertRow(i)
            for j in range(2):
                self.table.setItem(i, j, (QTableWidgetItem(row[str(j)])))
            row = "*" * len(self.f.decrypt(row["2"].encode()))
            self.table.setItem(i, 2, (QTableWidgetItem(row)))
            copy_btns.append(Copy_btn(i, data, self.f))
            self.table.setCellWidget(i, 3, copy_btns[i])

        self.table.setFixedWidth(619)

    def closeEvent(self, event):
        self.btn.setDisabled(False)
        logging.debug(event)
