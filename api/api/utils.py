"""Assorted general utilities."""
from functools import wraps

import jwt
from flask import jsonify, request, current_app
from marshmallow import Schema, ValidationError, fields, validates
from webargs.flaskparser import parser

from sqlalchemy_utils import create_database, database_exists


class JSONError(Exception):
    """Represent errors that have a payload that should be a jsonified response."""

    def __init__(self, payload):
        """Create a new ValidationError with the payload to jsonify."""
        super().__init__()
        self.payload = payload

    def get_response(self):
        """Get the jsonified response of the payload."""
        return jsonify(self.payload)


def create_sqla_db(app, db) -> None:
    """Create a database if it does not exist."""
    if not database_exists(current_app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(current_app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()  # create the tables
