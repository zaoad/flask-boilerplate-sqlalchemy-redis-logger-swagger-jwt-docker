from sqlalchemy.orm import registry

# Define your model classes here

from my_api import config

SCHEMA_NAME = None
try:
    SCHEMA_NAME = config.SQLALCHEMY_SCHEMA
    if SCHEMA_NAME is None:
        raise Exception("Must provide SQLALCHEMY_SCHEMA")
except Exception as e:
    raise e
SCHEMA_PREFIX = f"{SCHEMA_NAME}."
UUID4_LEN = 40
ENUM_LEN = 16
TABLE_NAME_USER = "user"
TABLE_NAME_ROLE = "role"
TABLE_NAME_USER_ROlE = "user_role"
TABLE_ACCESS_NAME_USER = SCHEMA_PREFIX + TABLE_NAME_USER
TABLE_ACCESS_NAME_ROLE = SCHEMA_PREFIX + TABLE_NAME_ROLE
TABLE_ACCESS_NAME_USER_ROlE = SCHEMA_PREFIX + TABLE_NAME_USER_ROlE
# print("aashce 1")
from .user_roles import UserRole
from .user import User
from .roles import Role

