#!/usr/bin/python
"""Module for reading and updating encrypted config file"""

import os
import json
from cryptography.fernet import Fernet


class Config:
    """Class for working with encrypted config file"""

    key = b"LdGzkYcr8D4rOuKAyf_9spqqDGC-2Qf8duZM6x30ElQ="
    f = Fernet(key)

    @staticmethod
    def config():
        """
        Reads and returns configuration from config.json

        Returns:
            dict: configuration in form of a dictionary
        """

        with open(
            os.path.join(os.path.dirname(__file__), "config.json"), "rb"
        ) as file:
            config_enc = file.read()
        config = json.loads(Config.f.decrypt(config_enc).decode())
        return config

    @staticmethod
    def config_update(config):
        """
        Updates config.json

        Parameters:
            config (dict): configuration in form of a dictionary
        """

        with open(
            os.path.join(os.path.dirname(__file__), "config.json"), "wb"
        ) as file:
            file.write(Config.f.encrypt(json.dumps(config).encode()))


def main():
    """main function"""

    config = Config.config()
    # config["timeout"] = 5
    config["verify"] = False
    config_new = {}
    for parameter in config:
        print(type(config[parameter]))
        parameter_new = input(parameter + ": ")

        if parameter_new != " ":
            if parameter_new != "":
                config_new[parameter] = parameter_new
            else:
                config_new[parameter] = config[parameter]

    print(config_new)

    Config.config_update(config_new)


if __name__ == "__main__":
    main()
