#!/usr/bin/python

from PyQt5.QtWidgets import QApplication
import sys
from qpassword_manager.mainwindow import MainWindow


def main():
    app = QApplication(['qpassword_manager'])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
