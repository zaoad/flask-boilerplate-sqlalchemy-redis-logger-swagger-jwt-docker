import json
import uuid

from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.managers import user_manager, user_role_manager


def user_dict(user):
    user_info = dict()
    user_info["user_id"] = user.user_id
    user_info["name"] = user.name
    user_info["phone"] = user.phone
    user_info["email"] = user.email
    return user_info


def create_user(data: dict):
    try:
        data["user_id"] = str(uuid.uuid4())
        user, e = user_manager.add(sql.session, **data)
        sql.session.commit()
        user_info = user_dict(user)
        return user_info
    except Exception as e:
        sql.session.rollback()
        raise e


def get_user_info(user_id):
    try:
        user, e = user_manager.get_by_id(sql.session, user_id=user_id)
        if not user:
            return None
        user_info = user_dict(user)
        return user_info
    except Exception as e:
        raise e


def update_user(user_id: str, update_data: str):
    user_update_dict = {
        "filter_args_dict": {"user_id": user_id},
        "update_args_dict": update_data
    }
    try:
        user = user_manager.update(sql.session, **user_update_dict)
        user_info = user_dict(user)
        sql.session.commit()
        return user_info
    except Exception as e:
        sql.session.rollback()
        raise e


def delete_user(user_id: str):
    try:
        user_manager.delete(sql.session, user_id=user_id)
        sql.session.commit()
    except Exception as e:
        raise e


def get_all_active_users():
    try:
        user_list_obj, e = user_manager.get_all_by_id(sql.session)
        user_list = list()
        if user_list_obj:
            for user in user_list_obj:
                user_info = user_dict(user)
                user_list.append(user_info)
        return user_list
    except Exception as e:
        raise e
