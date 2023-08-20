# -*- coding: utf-8 -*-
from datetime import timedelta


from my_api.redis_manager import JWTBlacklist


def redis_store_blacklisted_client(user_id, ttl=0):
    jwt_blacklist = JWTBlacklist(user_id)
    jwt_blacklist.setex(timedelta(seconds=ttl))


def redis_clear_blacklisted_client(user_id):
    jwt_blacklist = JWTBlacklist(":".join([user_id]))
    jwt_blacklist.delete()
