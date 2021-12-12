#!/usr/bin/python

import json
from cryptography.fernet import Fernet


class Config:
    key = b"LdGzkYcr8D4rOuKAyf_9spqqDGC-2Qf8duZM6x30ElQ="
    f = Fernet(key)

    def config():
        with open("qpassword_manager/conf/config.json", "rb") as file:
            configEnc = file.read()
        config = json.loads(Config.f.decrypt(configEnc).decode())
        return config

    def config_update(config):
        with open("qpassword_manager/conf/config.json", "wb") as file:
            file.write(Config.f.encrypt(json.dumps(config).encode()))


def main():
    config = Config.config()
    for parameter in config:
        print(type(config[parameter]))
        if parameter != "connection_timeout":
            newParameter = input(parameter + ": ")
        else:
            try:
                newParameter = int(input(parameter + ": "))
            except ValueError:
                newParameter = ""

        if newParameter != "":
            config[parameter] = newParameter
    # print(config)

    Config.config_update(config)


if __name__ == "__main__":
    main()
