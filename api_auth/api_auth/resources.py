"""RESTful resources for api_auth."""
from datetime import datetime, timedelta

import jwt
from flask.json import jsonify
from flask_restful import Resource
from marshmallow import (Schema, ValidationError, fields, validates,
                         validates_schema)
from webargs.flaskparser import use_args

from api_auth import const
from api_auth.models import User


class CredentialSchema(Schema):
    """Schema for validating user credentials."""

    class Meta:
        """Enforce required and validated fields by enabling strict evaluation."""

        strict = True

    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates('username')
    def user_exists(self, value: str) -> None:
        """Query the database to see if a user with the given username exists."""
        target_user = User.query.filter_by(username=value).first()
        if target_user is None:
            raise ValidationError('No such user exists.')

    @validates_schema(skip_on_field_errors=True)
    def password_is_correct(self, data):
        """
        Check that the password is correct for the given user.

        Since this is only run if all field validations pass, we know that target_user
        is not None.
        """
        target_user = User.query.filter_by(username=data['username']).first()
        if data['password'] != target_user.password:
            raise ValidationError('Password is incorrect.', ['password'])


class UserResourse(Resource):
    """A restful resource for users."""

    def put(self):
        """Create a new user."""
        pass

    def post(self):
        """Change an existing user's password."""
        pass

    def delete(self):
        """Delete an existing user."""
        pass


class TokenResourse(Resource):
    """A RESTful resource for authorization tokens."""

    @use_args(CredentialSchema())
    def get(self, args):
        """Get a JWT if the credentials are valid."""
        expiration = datetime.utcnow() + timedelta(seconds=60)
        content = {
            'exp': expiration,
            'username': args['username'],
        }

        # Recall that encode returns a bytes object, so we will have to encode it
        # to be able to jsonify the token.
        token_bytes = jwt.encode(content, const.SECRET_KEY, algorithm='HS256')
        token = token_bytes.decode('UTF-8')

        return jsonify({
            'message': 'Success',
            'token': token})


def register_resources(api):
    """Register Flask-RESTful resources to the given api."""
    api.add_resource(UserResourse, '/user')
    api.add_resource(TokenResourse, '/token')
