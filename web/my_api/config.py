# -*- coding: utf-8 -*-
import os

"""SECRET_KEY: Secret key used for signing cookies and tokens.

Application will fail to start if $FLASK_SECRET is not set.
"""
try:
    SECRET_KEY = os.getenv("FLASK_SECRET").encode("utf-8")
except AttributeError:  # pragma: no cover
    raise RuntimeError("Environment variable $FLASK_SECRET was not set")

FLASK_ENV = os.getenv("FLASK_ENV", "development")
LOGGING_ROOT = os.getenv("LOGGING_ROOT", "logs")
LOGGING_CONFIG = os.getenv("LOGGING_CONFIG", f"instance/{FLASK_ENV}/logging.yaml")


# Sql database

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:admin@db:5432/flask_db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
BOING_SQLALCHEMY_SCHEMA = os.getenv("BOING_SQLALCHEMY_SCHEMA", "dev")

