from my_api.sql_alchemy.managers import BaseManager
from my_api.sql_alchemy.models import Role


class RoleManager(BaseManager):
    pass


role_manager = RoleManager(Role)
