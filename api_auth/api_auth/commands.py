"""Cli commands for api_auth."""
import click
from sqlalchemy_utils import create_database, database_exists

from api_auth.extensions import db
from flask import current_app


def register_commands(app):
    """
    Register commands to the given app.

    Example:
        @app.cli.command()
        def somecommand():
            ...
            do some stuff
            ...

    This registers a command that you can then run with
        flask somecommand
    """
    # pylint: disable=unused-variable

    @app.cli.command()
    def initdb():
        """Create the database and all SQLAlchemy tables if they do not exist."""
        if not database_exists(current_app.config['SQLALCHEMY_DATABASE_URI']):
            create_database(current_app.config['SQLALCHEMY_DATABASE_URI'])
        db.create_all()  # create the tables
        click.echo('Created all tables')

    @app.cli.command()
    def dropdb():
        """Drop all tables in database."""
        db.drop_all()
        click.echo('Dropped all tables')
