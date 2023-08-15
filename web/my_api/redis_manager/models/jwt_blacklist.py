# -*- coding: utf-8 -*-
from .base import Base, KeyType


class JWTBlacklist(Base):
    """Redis model for holding blacklisted identities.

    Key format: <prefix>:jwt_blacklist:<identity>
    Value type: String
    """

    __keyname__ = "jwt_blacklist"
    __keytype__ = KeyType.STRING

    def __init__(self, identity):
        super().__init__(self.__keyname__, self.__keytype__, identity)

    def set(self, value: str):
        raise RuntimeError("Method 'set' is not allowed.")
