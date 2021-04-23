#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
from password import *
import sys
from main_window import MainWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PasswordManager')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
