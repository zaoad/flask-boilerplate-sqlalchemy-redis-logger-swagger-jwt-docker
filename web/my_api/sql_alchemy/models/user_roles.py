from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.models.base_model import BaseModel
from my_api.sql_alchemy.models import UUID4_LEN,TABLE_NAME_USER_ROlE,  TABLE_ACCESS_NAME_USER, TABLE_ACCESS_NAME_ROLE



class UserRole(BaseModel):
    __tablename__ = TABLE_NAME_USER_ROlE

    id = sql.Column(sql.Integer, primary_key=True)
    user_id = sql.Column(
        sql.String(UUID4_LEN),
        sql.ForeignKey(f"{TABLE_ACCESS_NAME_USER}.user_id"),
        nullable=False,
        index=True,
    )
    role_id = sql.Column(
        sql.Integer,
        sql.ForeignKey(f"{TABLE_ACCESS_NAME_ROLE}.id"),
        nullable=False,
        index=True,
    )

    __table_args__ = (sql.UniqueConstraint("user_id", "role_id"),) + BaseModel.__table_args__
