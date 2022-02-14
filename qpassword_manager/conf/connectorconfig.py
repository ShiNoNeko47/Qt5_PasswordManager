#!/usr/bin/python
"""Module for reading and updating the config file"""

import os
import json


class Config:
    """Class for working with the config file"""

    @staticmethod
    def config():
        """
        Reads and returns configuration from config.json

        Returns:
            dict: configuration in form of a dictionary
        """

        with open(
            os.path.join(os.path.dirname(__file__), "config.json"),
            "r",
            encoding="utf8",
        ) as file:
            config = json.loads(file.read())
        return config

    @staticmethod
    def config_update(config):
        """
        Updates config.json

        Parameters:
            config (dict): configuration in form of a dictionary
        """

        with open(
            os.path.join(os.path.dirname(__file__), "config.json"),
            "w",
            encoding="utf8",
        ) as file:
            file.write(json.dumps(config))
