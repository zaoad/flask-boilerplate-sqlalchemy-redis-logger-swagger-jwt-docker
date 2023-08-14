# -*- coding: utf-8 -*-
import logging
import logging.config
import json


def create_logger(app):
    instance_name = app.config["FLASK_ENV"]
    try:
        with open(f"instance/{instance_name}/logging.json", 'r') as json_file:
            loaded_dict = json.load(json_file)
            logging.config.dictConfig(loaded_dict)
    except (FileNotFoundError, PermissionError) as e:
        print("error", e)
        # Skip custom logging silently when read error occurs
        pass

    # Register logging handler
    app.logger = logging.getLogger("custom_logger")
