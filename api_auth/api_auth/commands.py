"""Adding commannds to the flask cli."""
import click

from api_auth.extensions import db


def register_commands(app):
    """Add comands to the flask app."""
    # pylint: disable=unused-variable

    @app.cli.command()
    def initdb():
        """
        Create all SQLAlchemy tables.

        Run from terminal using 'flask initdb'.
        """
        db.create_all()
        click.echo('Created all tables')

    @app.cli.command()
    def dropdb():
        """
        Drop all tables in database.

        Run from terminal using 'flask dropdb'.
        """
        db.drop_all()
        click.echo('Dropped all tables')
