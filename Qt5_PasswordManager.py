#!/usr/bin/python

from PyQt5.QtWidgets import QApplication
import sys
from mainwindow import MainWindow


def main():
    app = QApplication(['Qt5PasswordManager'])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
