from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.models.base_model import BaseModel
from my_api.sql_alchemy.models import TABLE_NAME_USER, TABLE_NAME_ROLE, TABLE_ACCESS_NAME_USER_ROlE


class Role(BaseModel):
    __tablename__ = TABLE_NAME_ROLE
    id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String, unique=True)
    # users = sql.relationship(TABLE_NAME_USER, secondary=TABLE_ACCESS_NAME_USER_ROlE, back_populates=TABLE_NAME_ROLE)