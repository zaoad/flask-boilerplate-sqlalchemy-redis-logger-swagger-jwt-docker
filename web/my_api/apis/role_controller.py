from http import HTTPStatus
from flask_restx import Namespace, Resource, fields
from flask import request

from my_api.security.helpers import access_required, role_required
from my_api.security.token_type import TokenType
from my_api.sql_alchemy.enums import RoleType
from my_api.utils import Response
from my_api.services import role_service
from my_api.utils import format_update_data

api = Namespace("role", description="role related services")

add_role_model = api.model(
    "role_data", {
        "name": fields.String(description="role id")
    }
)


@api.route("")
class CreateAndGetAllRole(Resource):
    @access_required(TokenType.ACCESS_TOKEN)
    @role_required(RoleType.ADMIN)
    @api.expect(add_role_model)
    @api.doc(responses={200: "OK", 201: "CREATED"}, params={}, security="Access Token")
    def post(self):
        data = request.get_json()
        role_info = dict()
        role_info["name"] = data.get('name')
        if not role_info["name"]:
            return Response(HTTPStatus.BAD_REQUEST).error(error=HTTPStatus.BAD_REQUEST,
                                                          detail="name is required"), HTTPStatus.BAD_REQUEST
        try:
            role = role_service.create_role(role_info)
            return Response(HTTPStatus.CREATED).success(data=role), HTTPStatus.CREATED
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR

    @access_required(TokenType.ACCESS_TOKEN)
    @role_required(RoleType.ADMIN)
    @api.doc(responses={200: "OK"}, params={}, security="Access Token")
    def get(self):
        try:
            role_list = role_service.get_all_active_roles()
            return Response(HTTPStatus.OK).success(data=role_list), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR


@api.route("/<string:role_id>")
class UpdateRole(Resource):
    @access_required(TokenType.ACCESS_TOKEN)
    @role_required(RoleType.ADMIN)
    @api.expect(add_role_model)
    @api.doc(responses={200: "OK"}, params={}, security="Access Token")
    def put(self, role_id):
        if not role_service.get_role_info(role_id):
            return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                        detail=f"Role not exist"), HTTPStatus.NOT_FOUND
        data = request.get_json()
        role_info = dict()
        role_info["name"] = data.get('name')
        try:
            update_info = format_update_data(role_info)
            role = role_service.update_role(role_id, update_info)
            return Response(HTTPStatus.OK).success(data=role), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR

    @access_required(TokenType.ACCESS_TOKEN)
    @role_required(RoleType.ADMIN)
    @api.doc(responses={200: "OK"}, params={}, security="Access Token")
    def delete(self, role_id):
        try:
            if not role_service.get_role_info(role_id):
                return Response(HTTPStatus.NOT_FOUND).error(error=HTTPStatus.NOT_FOUND,
                                                            detail=f"Role not exist"), HTTPStatus.NOT_FOUND
            role_service.delete_role(role_id)
            return Response(HTTPStatus.OK).success(data={"message": "Deleted Successfully"}), HTTPStatus.OK
        except Exception as e:
            return Response(HTTPStatus.INTERNAL_SERVER_ERROR).error(error=HTTPStatus.INTERNAL_SERVER_ERROR,
                                                                    detail=str(e)), HTTPStatus.INTERNAL_SERVER_ERROR
