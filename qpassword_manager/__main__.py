#!/usr/bin/python

from PyQt5.QtWidgets import QApplication
import sys
from qpassword_manager.mainwindow import MainWindow


def main():
    app = QApplication(["qpassword_manager"])

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    sys.exit(main())
