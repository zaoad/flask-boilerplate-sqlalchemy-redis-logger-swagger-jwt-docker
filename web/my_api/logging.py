# -*- coding: utf-8 -*-
import logging
import logging.config
import os
import re
import json


def create_logger(app):
    try:
        with open('data.json', 'r') as json_file:
            loaded_dict = json.load(json_file)
            logging.config.dictConfig(loaded_dict)
    except (FileNotFoundError, PermissionError):
            # Skip custom logging silently when read error occurs
            pass

    # Register logging handler
    appname, instance = app.import_name, app.config["FLASK_ENV"]
    app.logger = logging.getLogger(f"{appname}_{instance}")