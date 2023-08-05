from http import HTTPStatus
from flask_restx import Namespace, Resource
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash

from my_api.utils import Response
from my_api.services import user_service, user_role_service, role_service
from my_api.utils import format_update_data

api = Namespace("user", description="user related services")

mandatory_field = ["name", "phone", "password"]


@api.route("register")
class CreateUser(Resource):
    @api.doc(responses={200: "OK", 201: "CREATED"}, params={})
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
            user_result = user_service.create_user(user_info)
            return Response(HTTPStatus.CREATED).success(data=user_result), HTTPStatus.CREATED
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("")
class GetAllUsers(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def get(self):
        try:
            user_list = user_service.get_all_active_users()
            return Response(HTTPStatus.OK).success(data=user_list), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/<string:user_id>")
class UpdateUser(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def get(self, user_id):
        try:
            user_info = user_service.get_user_info(user_id)
            if not user_info:
                return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                            detail=f"User not exist"), HTTPStatus.NOT_FOUND
            return Response(HTTPStatus.OK).success(data=user_info), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(responses={200: "OK"}, params={})
    def put(self, user_id):
        try:
            if not user_service.get_user_info(user_id):
                return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                            detail=f"User not exist"), HTTPStatus.NOT_FOUND
            data = request.get_json()
            user_info = dict()
            user_info["name"] = data.get('name')
            user_info["email"] = data.get('email')
            user_info["phone"] = data.get("phone")

            update_info = format_update_data(user_info)
            user = user_service.update_user(user_id, update_info)
            return Response(HTTPStatus.OK).success(data=user), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(responses={200: "OK"}, params={})
    def delete(self, user_id):
        try:
            if not user_service.get_user_info(user_id):
                return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                            detail=f"User not exist"), HTTPStatus.NOT_FOUND
            user_service.delete_user(user_id)
            return Response(HTTPStatus.OK).success(data={"message": "Deleted Successfully"}), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/<string:user_id>/roles")
class AddRoleAndGetRoles(Resource):
    @api.doc(responses={200: "OK", 201: "CREATED"}, params={})
    def post(self, user_id):
        if not user_service.get_user_info(user_id):
            return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                        detail=f"User not exist"), HTTPStatus.NOT_FOUND

        data = request.get_json()
        role_id = data.get('role_id')
        if not role_service.get_role_info(role_id):
            return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                        detail=f"Role not exist"), HTTPStatus.NOT_FOUND
        if not role_id:
            return Response(HTTPStatus.BAD_REQUEST).error(error=HTTPStatus.BAD_REQUEST,
                                                          detail=f"role_id is required"), HTTPStatus.BAD_REQUEST
        try:
            user_role_service.add_user_role(user_id, role_id)
            return Response(HTTPStatus.CREATED).success(data={"message": "Role added Successfully"}), HTTPStatus.CREATED
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR

    @api.doc(responses={200: "OK"}, params={})
    def get(self, user_id):
        try:
            if not user_service.get_user_info(user_id):
                return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                            detail=f"User not exist"), HTTPStatus.NOT_FOUND
            role_names = user_role_service.get_user_roles_name(user_id)
            return Response(HTTPStatus.OK).success(data=role_names), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/<string:user_id>/roles/<string:role_id")
class DeleteUserRole(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def delete(self, user_id, role_id):
        try:
            if not user_role_service.get_user_role_info(user_id, role_id):
                return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                            detail=f"User Role not exist"), HTTPStatus.NOT_FOUND
            user_role_service.delete_user_role(user_id, role_id)
            return Response(HTTPStatus.OK).success(data={"message": "Deleted Successfully"}), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR
