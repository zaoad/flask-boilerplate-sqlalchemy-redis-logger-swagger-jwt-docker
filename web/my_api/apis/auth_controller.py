import traceback
from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
from flask import request, current_app as app

from my_api.services import user_service, user_role_service
from my_api.services.redis_services import redis_clear_blacklisted_client
from my_api.utils import Response
from my_api.security.auth_payload import AuthPayload
from my_api.security.token_type import TokenType
from my_api.security.helpers import (
    access_required,
    get_session_data,
    create_jwt_token,
    authorizations,
    delete_token_data,
    get_request_ip,
)

api = Namespace("auth", description="auth related services")

login_model = api.model(
    "login_data", {
        "phone": fields.String(description="phone number"),
        "password": fields.String(description="password"),
    }
)


@api.route("/login")
class login(Resource):
    def post(self):
        data = request.get_json()
        phone = data.get("phone")
        password = data.get("password")
        try:
            user_info = user_service.check_phone_password(phone, password)
            app.logger.error(
                f"Login requested from IP: {get_request_ip()}, Phone: {phone},"
            )
            if not user_info:
                return Response(HTTPStatus.BAD_REQUEST).error(error=HTTPStatus.BAD_REQUEST,
                                                              detail=f"phone or password is invalid"), HTTPStatus.BAD_REQUEST
            user_id = user_info["user_id"]
            role_names = user_role_service.get_user_roles_name(user_id)
            auth_payload = AuthPayload(
                token_type=TokenType.ACCESS_TOKEN,
                user_identity=user_id,
                user_roles=role_names,
                user_data={"phone": phone},
            )
            refresh_payload = auth_payload.duplicate_for(TokenType.REFRESH_TOKEN)
            data = {
                "access_token": create_jwt_token(auth_payload, ttl=app.config["JWT_ACCESS_TOKEN_EXPIRES"]),
                "refresh_token": create_jwt_token(refresh_payload, ttl=app.config["JWT_REFRESH_TOKEN_EXPIRES"]),
                "user_id": user_id
            }
            redis_clear_blacklisted_client(user_id=user_id)
            delete_token_data()
            app.logger.info("Successfully login")
            return Response(HTTPStatus.OK).success(data=data), HTTPStatus.OK
        except Exception as e:
            app.logger.error("Exception occurred: " + str(e) + "\n" + traceback.format_exc(limit=-20, chain=True))
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/refresh")
class Refresh(Resource):
    @access_required(TokenType.REFRESH_TOKEN)
    @api.doc(security="Refresh Token")
    def post(self):
        auth_data = get_session_data()
        app.logger.info(f"Refresh token requested from {auth_data.user_identity}")
        try:
            auth_payload = AuthPayload(
                token_type=TokenType.ACCESS_TOKEN,
                user_identity=auth_data.user_identity,
                user_roles=auth_data.user_roles,
                user_data=auth_data.user_data,
            )
            data = {
                "access_token": create_jwt_token(auth_payload, ttl=app.config["JWT_ACCESS_TOKEN_EXPIRES"]),
                "user_id": auth_data.user_identity,
            }
            if app.config["EXTEND_REFRESH_TOKEN"]:
                refresh_payload = auth_payload.duplicate_for(TokenType.REFRESH_TOKEN)
                data["refresh_token"] = create_jwt_token(
                    refresh_payload, ttl=app.config["JWT_REFRESH_TOKEN_EXPIRES"]
                )
            return data, 200

        except Exception as e:
            app.logger.error("Exception occurred: " + str(e) + "\n" + traceback.format_exc(limit=-20, chain=True))
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/verify-token")
class VerifyToken(Resource):
    @access_required(TokenType.ACCESS_TOKEN)
    @api.doc(security="Access Token")
    def post(self):
        auth_data = get_session_data()
        user_id = auth_data.user_identity
        app.logger.info(f"Authentication request for access token from {user_id}")
        return Response(HTTPStatus.OK).success(data={"message": "token verified"}), HTTPStatus.OK


@api.route("/logout")
class Logout(Resource):
    @access_required(TokenType.ANY)
    @api.doc(security=["Access Token", "Refresh Token", "OTP Token", "Web Token"])
    def post(self):
        auth_data = get_session_data()
        app.logger.info(f"Revoking token from {auth_data.user_identity}")
        delete_token_data()
        app.logger.info(f"Revoked {auth_data.token_type}")
        return {"message": "Token revoked"}, 200
