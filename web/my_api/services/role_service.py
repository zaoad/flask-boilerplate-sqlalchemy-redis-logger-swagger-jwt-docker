import json

from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.managers import role_manager


def create_role(data: dict):
    try:
        role_manager.add(sql.session, **data)
        sql.session.commit()
    except Exception as e:
        sql.session.rollback()
        raise e


def update_role(role_id: str, update_data: str):
    role_update_dict = {
        "filter_args_dict": {"id": role_id},
        "update_args_dict": update_data
    }
    try:
        role_manager.update(sql.session, **role_update_dict)
        sql.session.commit()
    except Exception as e:
        sql.session.rollback()
        raise e


def delete_role(role_id: str):
    try:
        role_manager.delete(sql.session, id=role_id)
        sql.session.commit()
    except Exception as e:
        raise e


def get_all_active_roles():
    try:
        role_list_obj, e = role_manager.get_all_by_id(sql.session)
        role_list = []
        for role in role_list_obj:
            role_list.append(role.name)
        return role_list
    except Exception as e:
        raise e
