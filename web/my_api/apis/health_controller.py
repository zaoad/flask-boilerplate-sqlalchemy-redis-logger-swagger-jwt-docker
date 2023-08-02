from flask_restx import Api, Resource, fields, Namespace
from my_api import VERSION
api = Namespace("health", description="auth related services")


@api.route("/status")
class HealthStatus(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def get(self):
        return {
            "status": "running",
            "api-version": f"{VERSION}",
        }, 200
