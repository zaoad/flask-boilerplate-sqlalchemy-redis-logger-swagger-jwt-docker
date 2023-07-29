import os

from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_app(app_name: str):
    """Creates a Flask app"""
    instance_name = os.getenv("FLASK_ENV", "development")
    instance_path = os.path.join(os.getcwd(), "instance")
    app = Flask(
        app_name,
        instance_path=instance_path,
        instance_relative_config=True,
    )
    print(instance_name, instance_path)
    # app.config.from_object("web.my_api.config")  # TODO this for running app using flask run
    app.config.from_object("my_api.config")
    app.config.from_pyfile(f"{instance_name}/application.cfg", silent=True)

    @app.route("/")
    def hello_world():
        return jsonify(hello="world")

    return app
