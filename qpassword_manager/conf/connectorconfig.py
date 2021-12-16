#!/usr/bin/python

import os
import json
from cryptography.fernet import Fernet


class Config:
    key = b"LdGzkYcr8D4rOuKAyf_9spqqDGC-2Qf8duZM6x30ElQ="
    f = Fernet(key)

    @staticmethod
    def config():
        with open(
            os.path.join(os.path.dirname(__file__), "config.json"), "rb"
        ) as file:
            config_enc = file.read()
        config = json.loads(Config.f.decrypt(config_enc).decode())
        return config

    @staticmethod
    def config_update(config):
        with open(
            os.path.join(os.path.dirname(__file__), "config.json"), "wb"
        ) as file:
            file.write(Config.f.encrypt(json.dumps(config).encode()))


def main():
    config = Config.config()
    for parameter in config:
        print(type(config[parameter]))
        if parameter != "connection_timeout":
            parameter_new = input(parameter + ": ")
        else:
            try:
                parameter_new = int(input(parameter + ": "))
            except ValueError:
                parameter_new = ""

        if parameter_new != "":
            config[parameter] = parameter_new
    # print(config)

    Config.config_update(config)


if __name__ == "__main__":
    main()
