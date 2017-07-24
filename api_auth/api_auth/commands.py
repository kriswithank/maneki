"""Cli commands for api_auth."""
import click

from api_auth.extensions import db


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
        """Create all SQLAlchemy tables."""
        db.create_all()
        click.echo('Created all tables')

    @app.cli.command()
    def dropdb():
        """Drop all tables in database."""
        db.drop_all()
        click.echo('Dropped all tables')
