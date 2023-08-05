from uuid import uuid4

from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.models.base_model import BaseModel
from my_api.sql_alchemy.models import UUID4_LEN, TABLE_NAME_USER, TABLE_ACCESS_NAME_USER_ROlE, TABLE_NAME_ROLE


USER_FULLNAME_LEN = 128
USER_PHONE_LEN = 20
USER_EMAIL_LEN = 320
USER_PASSWORD_LEN = 200


class User(BaseModel):
    __tablename__ = TABLE_NAME_USER
    user_id = sql.Column(sql.String(UUID4_LEN), primary_key=True)
    name = sql.Column(sql.String(USER_FULLNAME_LEN), nullable=False, default="")
    phone = sql.Column(sql.String(USER_PHONE_LEN), nullable=True)
    email = sql.Column(sql.String(USER_EMAIL_LEN), nullable=True)
    # password = sql.Column(sql.String(USER_PASSWORD_LEN), nullable=True, default="")
    # roles = sql.relationship(
    #     TABLE_NAME_ROLE,
    #     secondary=TABLE_ACCESS_NAME_USER_ROlE,
    #     back_populates=TABLE_NAME_USER,
    #     lazy="select",  # list is not small, will give a query object
    # )

    def __init__(self, name, phone, email):
        self.user_id = str(uuid4())
        self.name = name
        self.phone = phone
        self.email = email

