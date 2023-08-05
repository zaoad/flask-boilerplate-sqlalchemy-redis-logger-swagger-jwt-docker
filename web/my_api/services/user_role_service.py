import json

from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.managers import user_role_manager
from my_api.sql_alchemy.models.roles import Role
from my_api.sql_alchemy.enums import StatusType


def add_user_role(user_id, role_id):
    try:
        user_role = dict()
        user_role[user_id] = user_id
        user_role[role_id] = role_id
        user_role, e = user_role_manager.add(sql.session, **user_role)
        return user_role
    except Exception as e:
        raise e


def get_user_roles_name(user_id):
    try:
        user_role_list, e = user_role_manager.filter_by({"user_id": user_id, "status": StatusType.ACTIVE.name.lower()})
        role_list = [user_role.role_id for user_role in user_role_list]
        role_list = Role.filter(Role.id.in_(role_list)).all()
        role_names = [role.name for role in role_list]
        return role_names
    except Exception as e:
        raise e


def delete_user_role(user_id, role_id):
    try:
        user_role_manager.delete(sql.session, user_id=user_id, role_id=role_id)
        sql.session.commit()
    except Exception as e:
        raise e
