#!/usr/bin/python

from PyQt5.QtWidgets import *
import sqlite3
import sys
import os
from setupwindow import SetupWindow
from mainwindow import MainWindow

def main():
    os.chdir(sys.path[0])

    app = QApplication(['Qt5PasswordManager'])

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    try:
        c.execute('create table passwords (id integer, website varchar(50), username varchar(50), password varchar(50))')
        c.close()
        conn.close()

        window = SetupWindow()
        window.show()

    except Exception as e:
        c.execute('select password from passwords where (id = -1)')
        key_hashed = c.fetchone()[0]
        c.close()
        conn.close()

        window = MainWindow(key_hashed)
        window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
