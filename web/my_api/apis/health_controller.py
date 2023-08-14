from flask_restx import Resource, Namespace
from my_api import VERSION
from flask import current_app as app
api = Namespace("health", description="auth related services")


@api.route("/status")
class HealthStatus(Resource):
    @api.doc(responses={200: "OK"}, params={})
    def get(self):
        app.logger.info("Check server status")
        return {
            "status": "running",
            "api-version": f"{VERSION}",
        }, 200
