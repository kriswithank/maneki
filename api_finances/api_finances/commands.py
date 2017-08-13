"""Cli commands for api_finances."""
import click

from flask import current_app

from api_finances import models, utils  # models required import to create all tables
from api_finances.extensions import db


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
        utils.create_sqla_db(current_app, db)
        click.echo('Created all tables')

    @app.cli.command()
    def dropdb():
        """Drop all tables in database."""
        db.drop_all()
        click.echo('Dropped all tables')
