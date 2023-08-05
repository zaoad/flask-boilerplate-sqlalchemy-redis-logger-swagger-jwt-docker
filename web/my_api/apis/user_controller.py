from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from my_api.utils import Response
from my_api.services import user_service

api = Namespace("user", description="user related services")

mandatory_field = ["name", "phone", "password"]


@api.route("register")
class CreateUser(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def post(self):
        data = request.get_json()
        user_info = dict()
        user_info["name"] = data.get('name')
        user_info["email"] = data.get('email')
        user_info["phone"] = data.get("phone")
        user_info["password"] = generate_password_hash(data.get("password"))
        for field in mandatory_field:
            return Response(HTTPStatus.BAD_REQUEST).error(error=HTTPStatus.BAD_REQUEST,
                                                          detail=f"{field} is required"), HTTPStatus.BAD_REQUEST
        try:
            user_info = user_service.create_user(user_info)
            return Response(HTTPStatus.CREATED).success(data=user_info), HTTPStatus.CREATED
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR

