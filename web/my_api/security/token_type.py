# -*- coding: utf-8 -*-
import enum


class TokenType(enum.Enum):
    ACCESS_TOKEN = 1
    REFRESH_TOKEN = 2
    ANY = 5

    def __str__(self):
        return self.name
