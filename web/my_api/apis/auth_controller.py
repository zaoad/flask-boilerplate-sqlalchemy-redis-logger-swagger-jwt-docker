from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask import request

from my_api.utils import Response
from my_api.sql_alchemy.client import sql
from my_api.sql_alchemy.models.user import User

api = Namespace("auth", description="auth related services")

@api.route("/register")
class Register(Resource):
    def post(self):
        pass
        # data = request.get_json()
        # name = data.get('name')
        # email = data.get('email')
        # phone = data.get("phone")
        # password = data.get('password')
        #
        # hashed_password = generate_password_hash(password)
        #
        # with Session() as session:
        #     user = User(username=username, password=hashed_password)
        #     session.add(user)
        #     session.commit()
        #
        # return jsonify({"message": "User registered successfully."}), 201