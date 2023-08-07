# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# import binascii
# import os
# from datetime import timedelta
# from functools import wraps
#
from flask import g, request
# from flask_jwt_extended import (
#     verify_jwt_in_request,
#     get_jwt_identity,
#     create_access_token,
# )
from flask_jwt_extended.exceptions import WrongTokenError, RevokedTokenError, InvalidHeaderError, NoAuthorizationError
# from jwt import InvalidTokenError
#
# from boing import APPNAME
# from boing.core.redis_services import check_device_blocked
# from boing.extensions.sqlalchemy.enums import RoleType
# from boing.models.redis_models import JWTBlacklist, RoomMetadata
from .auth_payload import AuthPayload
# from boing.security.hash_store import HashStore
# from boing.security.token_type import TokenType
# from flask import request, current_app as app
#
# authorizations = {
#     "Access Token": {
#         "type": "apiKey",
#         "in": "header",
#         "name": "Authorization",
#         "description": "Format: Bearer <jwt_token>",
#     },
#     "Refresh Token": {
#         "type": "apiKey",
#         "in": "header",
#         "name": "Authorization",
#         "description": "Format: Bearer <jwt_token>",
#     },
#     "Basic Auth": {
#         "type": "basic",
#         "in": "header",
#         "name": "Authorization",
#     },
# }
#
#
# def is_identity_blacklisted(identity: str, auth_payload: AuthPayload, skip_client_check: bool = False) -> bool:
#     jwt_blacklist_model = JWTBlacklist(identity)
#     if jwt_blacklist_model.get():
#         return True
#     if not skip_client_check:
#         client_identity = ":".join(
#             [auth_payload.user_identity, auth_payload.device_identity, auth_payload.app_identity]
#         )
#         jwt_blacklist_model = JWTBlacklist(client_identity)
#         if jwt_blacklist_model.get():
#             return True
#     return False
#
#
# def access_required(*token_types: TokenType, optional: bool = False):
#     def decorator(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             if optional:
#                 verify_jwt_in_request_optional()
#             else:
#                 verify_jwt_in_request()
#             identity = get_jwt_identity()
#             app.logger.info(f"Got jwt identity: {identity}, token type: {token_types}")
#             if optional and identity is None:
#                 g.auth_payload = dict()
#                 g.auth_hash = None
#             else:
#                 if not isinstance(identity, str):
#                     app.logger.warning(f"Invalid token identity, token is not string, token type: {token_types}")
#                     raise InvalidTokenError("Invalid token identity")
#                 hash_store = HashStore(identity)
#                 auth_payload = hash_store.load_auth_hash()
#                 if auth_payload is None:
#                     app.logger.warning(f"Invalid token identity, auth payload is None, token type: {token_types}")
#                     raise InvalidTokenError("Invalid token identity")
#                 if TokenType.ANY not in token_types:
#                     if auth_payload.token_type not in token_types:
#                         app.logger.warning(f"Wrong token type, token type: {token_types}")
#                         raise WrongTokenError("Wrong token type")
#                 if check_device_blocked(auth_payload.device_identity):
#                     app.logger.warning(f"Device blocked for device id: {auth_payload.device_identity}")
#                     raise NoAuthorizationError("Device has been blocked")
#                 if is_identity_blacklisted(identity, auth_payload, auth_payload.token_type == TokenType.OTP_TOKEN):
#                     app.logger.warning(f"Token has been revoked, token type: {token_types}")
#                     raise RevokedTokenError("Token has been revoked")
#                 g.auth_payload = auth_payload
#                 g.auth_hash = identity
#             return fn(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
#
#
# def passwd_required(fn):
#     @wraps(fn)
#     def decorator(*args, **kwargs):
#         auth = request.authorization
#         try:
#             room_name_parts = auth.username.strip().split("#")
#             room_name = room_name_parts[0].strip()
#             room_user = room_name_parts[1].strip()
#             comm_user = room_name_parts[2].strip() if len(room_name_parts) > 2 else None
#             room_password = auth.password.strip()
#             if len(room_name) == 0 or len(room_user) == 0 or len(room_password) == 0:
#                 raise ValueError
#         except (AttributeError, IndexError, ValueError):
#             raise InvalidHeaderError("Invalid authorization header")
#         room_metadata_model = RoomMetadata(room_name)
#         ex_room_metadata = room_metadata_model.hgetall()
#         if ex_room_metadata is None or ex_room_metadata.get("web_password") != room_password:
#             raise NoAuthorizationError("Unauthorized")
#         g.auth_payload = AuthPayload(
#             token_type=TokenType.PASSWD_TOKEN,
#             user_identity=room_user,
#             device_identity=f"{room_name}#{int(binascii.hexlify(os.urandom(8)), 16)}",
#             app_identity=APPNAME,
#             user_roles=[RoleType.COMM_USER.name if comm_user else RoleType.WEB_USER.name],
#             user_data={"room_name": room_name, "comm_user": comm_user},
#         )
#         return fn(*args, **kwargs)
#
#     return decorator
#

def get_session_data() -> AuthPayload:
    if hasattr(g, "auth_payload"):
        return g.auth_payload
    raise InvalidHeaderError

#
# def get_request_ip() -> str:
#     return request.environ.get("HTTP_X_FORWARDED_FOR", request.environ["REMOTE_ADDR"])
#
#
# def create_jwt_token(auth_payload: AuthPayload, ttl: int) -> str:
#     app.logger.info(f"Create JWT token request from user: {auth_payload.user_identity}, TTL: {ttl}")
#     if not auth_payload.validate():
#         app.logger.warning(f"Auth payload validation failed in create jwt token for user: {auth_payload.user_identity}")
#         raise AttributeError("Invalid auth payload")
#     hash_store = HashStore(auth_payload.get_hash())
#     hash_store.store_auth_hash(payload=auth_payload, ttl=ttl)
#     return create_access_token(identity=hash_store.auth_hash, expires_delta=timedelta(seconds=ttl))
#
#
# def delete_token_data():
#     if hasattr(g, "auth_hash"):
#         hash_store = HashStore(g.auth_hash)
#         hash_store.delete_auth_hash()
#
#
# def role_required(*role_types: RoleType):
#     def decorator(fn):
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             auth_data = get_session_data()
#             roles = auth_data.user_roles
#             valid_roles = list(set([rt.name for rt in role_types]).intersection(roles))
#             if not valid_roles:
#                 raise NoAuthorizationError("Unauthorized")
#             return fn(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
