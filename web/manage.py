from flask.cli import FlaskGroup

from my_api.app import create_app


cli = FlaskGroup(create_app=lambda : create_app("my_api"))


if __name__ == "__main__":
    cli()