import os

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

from my_api.sql_alchemy import client as sql_client
from my_api.apis import api_blueprint

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
    sql_client.sql.init_app(app)
    CORS(app)
    app.register_blueprint(api_blueprint)
    return app
