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


class ValidTokenSchema(Schema):
    """Marshmallow schema for validating tokens."""

    class Meta:
        """Enforce required and validated fields by enabling strict evaluation."""

        strict = True

    token = fields.Str(required=True)

    @validates('token')
    def token_is_valid(self, value: str) -> None:
        """Return True iff the token is valid, otherwise raise a ValidationError."""
        try:
            jwt.decode(value, current_app.config['SECRET_KEY'], algorithm='HS256')
        except jwt.exceptions.ExpiredSignatureError:
            raise ValidationError('Token is expired.')
        except jwt.exceptions.DecodeError:
            raise ValidationError('Token is invalid.')


def token_required(func):
    """Decorate functions requiring a valid token with this."""
    @wraps(func)
    def test_for_valid_token(*args, **kwargs):
        """Use ValidTokenSchema to validate token and discard generated args."""
        parser.parse(ValidTokenSchema(), request)
        return func(*args, **kwargs)
    return test_for_valid_token


def create_sqla_db(app, db) -> None:
    """Create a database if it does not exist."""
    if not database_exists(current_app.config['SQLALCHEMY_DATABASE_URI']):
        create_database(current_app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()  # create the tables
