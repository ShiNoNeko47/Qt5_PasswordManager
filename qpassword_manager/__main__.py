#!/usr/bin/python
"""Entry point"""

import sys
import os
import getopt
import logging
from xdg import xdg_data_home
from PyQt5.QtWidgets import QApplication
from qpassword_manager.login_window import LoginWindow


def main() -> None:
    """Argument parsing and app initialization"""

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "l:", ["log="])

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

    os.chdir(os.path.join(xdg_data_home(), "qpassword_manager"))

    window = LoginWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    sys.exit(main())
