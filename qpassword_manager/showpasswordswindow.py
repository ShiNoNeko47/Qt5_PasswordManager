from PyQt5.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
)
import requests
from cryptography.fernet import Fernet
from qpassword_manager.btns.copybtn import Copy_btn
from conf.connectorconfig import Config


class ShowPasswordsWindow(QWidget):
    def __init__(self, btn):
        super().__init__()

        self.btn = btn
        self.setWindowTitle("Passwords")
        self.layout = QGridLayout()

        self.setFixedWidth(640)
        self.setLayout(self.layout)

    def set_key(self, key):
        self.f = Fernet(key)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.verticalHeader().setVisible(False)
        self.table.setHorizontalHeaderLabels(
            ["Website", "Username", "Password", ""]
        )
        self.r = requests.post(
            Config.config()["host"], {"action": "create_table"}, auth=self.auth
        )
        print(self.r.json())
        self.data = self.r.json()

        for i in range(3):
            self.table.setColumnWidth(i, 190)
        self.table.setColumnWidth(3, 30)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        copy_btns = []
        for row, i in zip(self.data, range(len(self.data))):
            self.table.insertRow(i)
            for j in range(2):
                self.table.setItem(i, j, (QTableWidgetItem(row[str(j)])))
            data = "*" * len(self.f.decrypt(row["2"].encode()))
            self.table.setItem(i, 2, (QTableWidgetItem(data)))
            copy_btns.append(Copy_btn(i, self.data, self.f))
            self.table.setCellWidget(i, 3, copy_btns[i])

        self.table.setFixedWidth(619)

        self.layout.addWidget(self.table, 0, 0)

    def closeEvent(self, event):
        self.btn.setDisabled(False)
