# -*- coding: utf-8 -*-
import binascii
import copy
import json
import os
import time
from json.decoder import JSONDecodeError
from typing import List, Any

from my_api.security.token_type import TokenType
from my_api.utils import get_sha1_hash, not_empty


class AuthPayload(object):
    def __init__(
        self,
        token_type: TokenType,
        user_identity: str,
        user_roles: List[str],
        user_data: Any = None,
    ):
        self.token_type = token_type
        self.user_identity = user_identity
        self.user_roles = user_roles
        if isinstance(user_data, str):
            try:
                self.user_data = json.loads(user_data)
            except JSONDecodeError:
                self.user_data = dict()
        elif isinstance(user_data, dict):
            self.user_data = user_data
        else:
            self.user_data = dict()
        self.timestamp = int(time.time())
        self.seed = int(binascii.hexlify(os.urandom(8)), 16)
        self.hash_method = get_sha1_hash

    @staticmethod
    def _dict_to_str(data: dict) -> str:
        return json.dumps(data, sort_keys=True)

    @classmethod
    def from_dict(cls, payload: dict):
        return cls(
            TokenType[payload["token_type"]],
            payload["user_identity"],
            payload["user_roles"].split(","),
            payload.get("user_data"),
        )

    def validate(self):
        return (
            isinstance(self.token_type, TokenType)
            and not_empty(self.user_identity)
            and isinstance(self.user_roles, list)
            and not_empty(self.user_roles)
        )

    def to_dict(self):
        return {
            "token_type": str(self.token_type),
            "user_identity": self.user_identity,
            "user_roles": ",".join(self.user_roles),
            "user_data": json.dumps(self.user_data if self.user_data else dict()),
            "timestamp": self.timestamp,
        }

    def get_hash(self) -> str:
        str_data = self._dict_to_str(self.to_dict())
        return self.hash_method(str_data)

    def duplicate_for(self, token_type: TokenType):
        cloned = copy.deepcopy(self)
        cloned.token_type = token_type
        return cloned
