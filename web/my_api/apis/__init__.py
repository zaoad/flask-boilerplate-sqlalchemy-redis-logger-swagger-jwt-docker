from flask import Blueprint
from flask_restx import Api

from my_api import APPNAME, VERSION

from my_api.apis.health_controller import api as health_ns
from my_api.apis.task_controller import api as task_ns
from my_api.apis.user_controller import api as user_ns
api_blueprint = Blueprint("api", APPNAME, url_prefix="/my-api")

api = Api(
    api_blueprint,
    title=APPNAME,
    version=VERSION,
    description="Restful API for communicator"
)

api.add_namespace(task_ns, path="/tasks")
api.add_namespace(health_ns, path="/health")
api.add_namespace(user_ns, path="/users")

__all__ = ["api_blueprint"]