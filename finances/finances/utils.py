"""Assorted general utilities."""
from flask import current_app

from sqlalchemy_utils import create_database, database_exists


def create_sqla_db(app, db) -> None:
    """Create a database if it does not exist."""
    if not database_exists(current_app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(current_app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()  # create the tables
