#!/usr/bin/python
"""Module for reading and updating the config file"""

import os
import logging
import json
from xdg import xdg_data_home


class Config:
    """Class for working with the config file"""

    @staticmethod
    def config():
        """
        Reads and returns configuration from config.json

        Returns:
            dict: configuration in form of a dictionary
        """

        try:
            with open(
                os.path.join(xdg_data_home(), 'qpassword_manager',
                             "config.json"),
                "r",
                encoding="utf8",
            ) as file:
                config = json.loads(file.read())
            return config
        except FileNotFoundError as error:
            with open(
                os.path.join(xdg_data_home(), 'qpassword_manager',
                             "config.json"),
                "w+",
                encoding="utf8",
            ) as file:
                config = """{
                    \"host\": {
                        \"timeout\": 5,
                        \"url\": \"https://qpasswordmanager.ddns.net\"
                    },
                    \"database_online\": false,
                    \"vim_mode\": true
                }"""
                file.write(config)
                return json.loads(config)
            logging.debug(error)

    @staticmethod
    def config_update(config):
        """
        Updates config.json

        Parameters:
            config (dict): configuration in form of a dictionary
        """

        with open(
            os.path.join(xdg_data_home(), 'qpassword_manager',
                         "config.json"),
            "w",
            encoding="utf8",
        ) as file:
            file.write(json.dumps(config))
