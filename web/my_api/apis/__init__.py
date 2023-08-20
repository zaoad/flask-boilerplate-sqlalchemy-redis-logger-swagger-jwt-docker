from flask import Blueprint
from flask_restx import Api

from my_api import APPNAME, VERSION

from my_api.apis.health_controller import api as health_ns
from my_api.apis.task_controller import api as task_ns
from my_api.apis.user_controller import api as user_ns
from my_api.apis.auth_controller import api as auth_ns
from my_api.apis.role_controller import api as role_ns
from flask_jwt_extended.exceptions import NoAuthorizationError, CSRFError, InvalidHeaderError, JWTDecodeError, \
    WrongTokenError, RevokedTokenError, FreshTokenRequired

api_blueprint = Blueprint("api", APPNAME, url_prefix="/my-api")

api = Api(
    api_blueprint,
    title=APPNAME,
    version=VERSION,
    description="Restful API for communicator"
)


@api.errorhandler(NoAuthorizationError)
def handle_auth_error(e):
    return {"message": str(e)}, 401


@api.errorhandler(CSRFError)
def handle_auth_error(e):
    return {"message": str(e)}, 401


@api.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    return {"message": str(e)}, 422


@api.errorhandler(JWTDecodeError)
def handle_jwt_decode_error(e):
    return {"message": str(e)}, 422


@api.errorhandler(WrongTokenError)
def handle_wrong_token_error(e):
    return {"message": str(e)}, 422


@api.errorhandler(RevokedTokenError)
def handle_revoked_token_error(e):
    return {"message": str(e)}, 401


@api.errorhandler(FreshTokenRequired)
def handle_fresh_token_required(e):
    return {"message": str(e)}, 401


api.add_namespace(task_ns, path="/tasks")
api.add_namespace(health_ns, path="/health")
api.add_namespace(user_ns, path="/users")
api.add_namespace(auth_ns, path="/auth")
api.add_namespace(role_ns, path="/roles")

__all__ = ["api_blueprint"]
