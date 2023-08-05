from my_api.sql_alchemy.managers import BaseManager
from my_api.sql_alchemy.models.user import User
from my_api.sql_alchemy.enums import StatusType


class UserManager(BaseManager):
   pass


user_manager = UserManager(User)
