#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .base import Base, KeyType


class AuthHash(Base):
    """Redis model for holding auth token hashes

    Key format: <prefix>:auth_hash:<hash>
    Value type: Hash <field, value>
    """

    __keyname__ = "auth_hash"
    __keytype__ = KeyType.HASH

    def __init__(self, identity):
        super().__init__(self.__keyname__, self.__keytype__, identity)
