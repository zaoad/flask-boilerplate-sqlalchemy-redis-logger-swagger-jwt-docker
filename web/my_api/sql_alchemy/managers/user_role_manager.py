from my_api.sql_alchemy.managers import BaseManager
from my_api.sql_alchemy.models import UserRole


class UserRoleManager(BaseManager):
    pass


user_role_manager = UserRoleManager(UserRole)
