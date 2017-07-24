"""
General extensions to the flask app.

Most of these extensions will have to be registered with the app seperately.
"""
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
api = Api()


def register_extensions(app):
    """Register extensions to the given app."""
    db.init_app(app)
    api.init_app(app)
