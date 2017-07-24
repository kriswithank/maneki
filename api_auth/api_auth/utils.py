"""Assorted general utilities."""
from flask import jsonify, current_app
from marshmallow import Schema, ValidationError, fields, validates
import jwt


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
