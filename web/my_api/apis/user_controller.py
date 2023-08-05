from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask import request

from my_api.utils.http_response import Response
from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.models.user import User

api = Namespace("user", description="user related services")


@api.route("")
class HealthStatus(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def post(self):
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        phone = data.get("phone")

        if not name or not email:
            return Response(HTTPStatus.BAD_REQUEST).error(error=HTTPStatus.BAD_REQUEST,
                                                          detail="Bad Request"), HTTPStatus.BAD_REQUEST

        new_user = User(name=name, phone=phone, email=email)
        sql.session.add(new_user)
        sql.session.commit()

        return Response(HTTPStatus.CREATED).success(data={"msg": "created"}), HTTPStatus.CREATED
