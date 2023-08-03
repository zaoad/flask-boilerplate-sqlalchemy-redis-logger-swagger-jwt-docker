import os
import click
from flask.cli import FlaskGroup

from my_api.app import create_app
from my_api.sql_alchemy import client as sql_client

cli = FlaskGroup(create_app=lambda: create_app("my_api"))


@cli.command("env")
def env():
    """Check env variables for the app."""
    env_vars = ["FLASK_ENV", "FLASK_SECRET", "LOGGING_ROOT", "LOGGING_CONFIG"]
    for var in env_vars:
        click.echo(f"${var}={os.getenv(var)}")


@cli.command("create_db")
def create_db():
    click.echo("hello")

@cli.command("create_db")
def create_db():
    create_app("my_api")
    sql_client.sql.drop_all()
    sql_client.sql.create_all()
    sql_client.sql.session.commit()

@cli.command("seed_db")
def seed_db():
    pass


if __name__ == "__main__":
    cli()
