# -*- coding: utf-8 -*-
from datetime import timedelta

from my_api.redis_manager.models.auth_hash import AuthHash
from .auth_payload import AuthPayload


class HashStore(object):
    def __init__(self, auth_hash):
        self.auth_hash = auth_hash
        self.auth_hash_model = AuthHash(auth_hash)

    def store_auth_hash(self, payload: AuthPayload, ttl: int):
        self.auth_hash_model.hmset(payload.to_dict())
        self.auth_hash_model.hsetex(timedelta(seconds=ttl))

    def load_auth_hash(self):
        auth_hash_dict = self.auth_hash_model.hgetall()
        try:
            return AuthPayload.from_dict(auth_hash_dict)
        except (KeyError, TypeError):
            return None

    def delete_auth_hash(self):
        self.auth_hash_model.delete()
