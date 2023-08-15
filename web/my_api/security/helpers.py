#!/usr/bin/env python
# -*- coding: utf-8 -*-
import binascii
import os
from datetime import timedelta
from functools import wraps

from flask import g, request
from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt_identity,
    create_access_token,
)
from flask_jwt_extended.exceptions import WrongTokenError, RevokedTokenError, InvalidHeaderError, NoAuthorizationError
from jwt import InvalidTokenError

from my_api.sql_alchemy.enums import RoleType
from my_api.redis_manager.models.jwt_blacklist import JWTBlacklist
from .auth_payload import AuthPayload
from my_api.security.hash_store import HashStore
from my_api.security.token_type import TokenType
from flask import request, current_app as app


authorizations = {
    "Access Token": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Format: Bearer <jwt_token>",
    },
    "Refresh Token": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Format: Bearer <jwt_token>",
    },
    "Basic Auth": {
        "type": "basic",
        "in": "header",
        "name": "Authorization",
    },
}


def is_identity_blacklisted(identity: str) -> bool:
    jwt_blacklist_model = JWTBlacklist(identity)
    if jwt_blacklist_model.get():
        return True
    return False


def access_required(*token_types: TokenType):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            identity = get_jwt_identity()
            app.logger.info(f"Got jwt identity: {identity}, token type: {token_types}")

            if not isinstance(identity, str):
                app.logger.warning(f"Invalid token identity, token is not string, token type: {token_types}")
                raise InvalidTokenError("Invalid token identity")
            hash_store = HashStore(identity)
            auth_payload = hash_store.load_auth_hash()
            if auth_payload is None:
                app.logger.warning(f"Invalid token identity, auth payload is None, token type: {token_types}")
                raise InvalidTokenError("Invalid token identity")
            if TokenType.ANY not in token_types:
                if auth_payload.token_type not in token_types:
                    app.logger.warning(f"Wrong token type, token type: {token_types}")
                    raise WrongTokenError("Wrong token type")
            if is_identity_blacklisted(identity):
                app.logger.warning(f"Token has been revoked, token type: {token_types}")
                raise RevokedTokenError("Token has been revoked")
            g.auth_payload = auth_payload
            g.auth_hash = identity
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def get_session_data() -> AuthPayload:
    if hasattr(g, "auth_payload"):
        return g.auth_payload
    raise InvalidHeaderError


def get_request_ip() -> str:
    return request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])


def create_jwt_token(auth_payload: AuthPayload, ttl: int) -> str:
    app.logger.info(f"Create JWT token request from user: {auth_payload.user_identity}, TTL: {ttl}")
    if not auth_payload.validate():
        app.logger.warning(f"Auth payload validation failed in create jwt token for user: {auth_payload.user_identity}")
        raise AttributeError("Invalid auth payload")
    hash_store = HashStore(auth_payload.get_hash())
    hash_store.store_auth_hash(payload=auth_payload, ttl=ttl)
    return create_access_token(identity=hash_store.auth_hash, expires_delta=timedelta(seconds=ttl))


def delete_token_data():
    if hasattr(g, "auth_hash"):
        hash_store = HashStore(g.auth_hash)
        hash_store.delete_auth_hash()


def role_required(*role_types: RoleType):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            auth_data = get_session_data()
            roles = auth_data.user_roles
            valid_roles = list(set([rt.name for rt in role_types]).intersection(roles))
            if not valid_roles:
                raise NoAuthorizationError("Unauthorized")
            return fn(*args, **kwargs)

        return wrapper

    return decorator
