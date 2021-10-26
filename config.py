#!/usr/bin/python

import json
from cryptography.fernet import Fernet

class Config:
    key = b'LdGzkYcr8D4rOuKAyf_9spqqDGC-2Qf8duZM6x30ElQ='
    f = Fernet(key)

    def config():
        with open('config.json', 'rb') as file:
            configEnc = file.read()
        config = json.loads(Config.f.decrypt(configEnc).decode())
        return(config)

    def config_update(config):
        with open('config.json', 'wb') as file:
            file.write(Config.f.encrypt(json.dumps(config).encode()))
