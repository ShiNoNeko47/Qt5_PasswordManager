"""Database setup window"""

import sys
import sqlite3
from PyQt5.QtWidgets import (
    QGridLayout,
    QPushButton,
    QLineEdit,
    QWidget,
    QApplication,
)
from PyQt5.Qt import Qt
from Crypto.Hash import SHA256


class SetupWindow(QWidget):
    """
    The window for setting up an offline database
    """

    def __init__(self):
        super().__init__()
        self.layout = QGridLayout()
        self.setWindowTitle("Database Setup")
        self.setFixedHeight(100)
        self.setFixedWidth(600)

        self.key_setup_le = QLineEdit()
        self.key_setup_le.setEchoMode(QLineEdit.Password)
        self.key_setup_le.textChanged.connect(self.check)
        self.layout.addWidget(self.key_setup_le, 0, 0)

        self.key_reenter_le = QLineEdit()
        self.key_reenter_le.setEchoMode(QLineEdit.Password)
        self.key_reenter_le.textChanged.connect(self.check)
        self.layout.addWidget(self.key_reenter_le, 1, 0)

        self.ok_btn = QPushButton("Ok")
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.create)
        self.layout.addWidget(self.ok_btn, 1, 1)

        self.setLayout(self.layout)

    def keyPressEvent(self, event):  # pylint: disable=invalid-name
        """Clicks ok button when you press enter"""

        if event.key() == Qt.Key_Return:
            self.ok_btn.click()

    def check(self):
        """Checks if inputs are valid"""

        self.ok_btn.setEnabled(False)
        if all(
            [
                self.key_setup_le.text() == self.key_reenter_le.text(),
                len(self.key_setup_le.text()) > 3,
            ]
        ):
            self.ok_btn.setEnabled(True)

    def create(self):
        """Creates new database"""

        conn = sqlite3.connect("passwords.db")
        cursor = conn.cursor()
        cursor.execute(
            """create table passwords
               (id integer,
               website varchar(50),
               username varchar(50),
               password varchar(50))"""
        )
        key = str.encode(self.key_setup_le.text())
        cursor.execute(
            f"""insert into passwords values
                (-1,
                \"Master\",
                \"Key\",
                \"{SHA256.new(key).hexdigest()}\")"""
        )
        conn.commit()
        cursor.close()
        conn.close()

        self.close()


def main():
    """Main function"""

    app = QApplication([])
    window = SetupWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    sys.exit(main())
