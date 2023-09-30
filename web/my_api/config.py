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
LOGGING_CONFIG = os.getenv("LOGGING_CONFIG", f"instance/{FLASK_ENV}/logging.json")


# jwt
JWT_ACCESS_TOKEN_EXPIRES = 10080
JWT_REFRESH_TOKEN_EXPIRES = 1296200
JWT_OTP_TOKEN_EXPIRES = 300
JWT_VOIP_PASSWORD_TOKEN_EXPIRES = 86400
EXTEND_REFRESH_TOKEN = True

# Sql database

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/flask_db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_SCHEMA = os.getenv("SQLALCHEMY_SCHEMA", "my_schema")

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_PREFIX = os.getenv("REDIS_PREFIX", "my-api")
REDIS_FAIL_ATTEMPTS_MAX = 5

AUTHOR="Zaoad"