#!/usr/bin/python

from PyQt5.QtWidgets import QApplication
import sys
import getopt
import logging
from qpassword_manager.mainwindow import MainWindow


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "l:", ["log="])

        for option, argument in opts:
            if option in ("-h", "--help"):
                pass

            elif option in ("-l", "--log"):
                level = getattr(logging, argument.upper(), None)
                if not isinstance(level, int):
                    raise ValueError(f"Invalid log level: {argument}")
                logging.basicConfig(level=level)

    except getopt.GetoptError as err:
        print(str(err))

    app = QApplication(["qpassword_manager"])

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    sys.exit(main())
