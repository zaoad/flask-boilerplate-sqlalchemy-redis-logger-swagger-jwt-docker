import json

from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.managers import user_role_manager
from my_api.sql_alchemy.models import Role
from my_api.sql_alchemy.enums import StatusType


def add_user_role(user_id, role_id):
    try:
        user_role = dict()
        user_role["user_id"] = user_id
        user_role["role_id"] = int(role_id)
        user_role, e = user_role_manager.add(sql.session, **user_role)
        sql.session.commit()
        return user_role
    except Exception as e:
        raise e


def get_user_role_info(user_id, role_id):
    try:
        role, e = user_role_manager.get_by_id(sql.session, user_id=user_id, role_id=role_id)
        if not role:
            return None
        role_info = {"user_id": role.user_id, "role_id": role.role_id}
        return role_info
    except Exception as e:
        raise e


def get_user_roles_name(user_id):
    try:
        user_role_list , e  = user_role_manager.get_all_by_id(session=sql.session, user_id=user_id, status=StatusType.ACTIVE.name.lower())
        if user_role_list:
            role_list = [user_role.role_id for user_role in user_role_list]
            role_list = Role.query.filter(Role.id.in_(role_list)).all()
            role_names = [role.name for role in role_list]
            return role_names
        return []
    except Exception as e:
        raise e


def delete_user_role(user_id, role_id):
    try:
        user_role_manager.delete(sql.session, user_id=user_id, role_id=role_id)
        sql.session.commit()
    except Exception as e:
        raise e
