#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
import sys
import os
from mainwindow import MainWindow

def main():
    try:
        os.chdir(sys.path[0])
    except:
        pass

    app = QApplication(['Qt5PasswordManager'])

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
