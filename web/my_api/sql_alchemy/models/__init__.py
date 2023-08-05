from my_api import config
SCHEMA_NAME = None
try:
    SCHEMA_NAME = config.SQLALCHEMY_SCHEMA
    if SCHEMA_NAME is None:
        raise Exception("Must provide SQLALCHEMY_SCHEMA")
except Exception as e:
    raise e

UUID4_LEN = 40
ENUM_LEN = 16
TABLE_NAME_USER = "user"
TABLE_NAME_ROLE = "role"
TABLE_ACCESS_NAME_USER_ROlE = "user_role"
