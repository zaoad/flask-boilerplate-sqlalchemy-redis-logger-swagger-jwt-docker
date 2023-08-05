from datetime import datetime

from my_api.sql_alchemy.models import SCHEMA_NAME, UUID4_LEN, ENUM_LEN
from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.enums import StatusType


class BaseModel(sql.Model):
    __abstract__ = True
    __table_args__ = ({"schema": SCHEMA_NAME},)

    create_time = sql.Column(sql.DateTime, nullable=False, default=datetime.utcnow)
    update_time = sql.Column(sql.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = sql.Column(sql.String(UUID4_LEN), nullable=True)
    updated_by = sql.Column(sql.String(UUID4_LEN), nullable=True)
    status = sql.Column(sql.String(ENUM_LEN), nullable=False, default=StatusType.ACTIVE.name.lower())
    version = sql.Column(sql.Integer, nullable=False, default=1)

    __mapper_args__ = {"version_id_col": version}
