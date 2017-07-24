"""A RESTful api for authorizing users using Jason Web Tokens."""
from datetime import datetime, timedelta

import jwt
from flask import Flask
from flask.json import jsonify
from flask_restful import Resource
from marshmallow import (Schema, ValidationError, fields, validates,
                         validates_schema)
from webargs.flaskparser import parser, use_args

from api_auth.commands import configure_app_cli
from api_auth.extensions import api, db
from api_auth.models import User
from api_auth.utils import JSONError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notverysecure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/postgres'


@app.errorhandler(JSONError)
def handle_jsonerror(error):
    """Return a jsonified response of a ValidationError's payload when it raised and uncaught."""
    return error.get_response()


@parser.error_handler
def handle_error(error):
    """Handle validations errors by just converting them to a JSONError."""
    raise JSONError(error.messages)


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
            jwt.decode(value, app.config['SECRET_KEY'], algorithm='HS256')
        except jwt.exceptions.ExpiredSignatureError:
            raise ValidationError('Token is expired.')
        except jwt.exceptions.DecodeError:
            raise ValidationError('Token is invalid.')


class CredentialSchema(Schema):
    """Marhmallow Schema for validating user credentials."""

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
        """Check that the password is correct for the given user.

        Since this is only run if all field validations pass, we know that target_user
        is not None.
        """
        target_user = User.query.filter_by(username=data['username']).first()
        if data['password'] != target_user.password:
            raise ValidationError('Password is incorrect.', ['password'])


@app.route('/foo-route')
@use_args(ValidTokenSchema())
def foo_route(data):  # pylint: disable=unused-argument
    """Test 'token-required' decorator."""
    return "you should only see this if you have a valid token."


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
        token_bytes = jwt.encode(content, app.config['SECRET_KEY'], algorithm='HS256')
        token = token_bytes.decode('UTF-8')

        return jsonify({
            'message': 'Success',
            'token': token})


api.add_resource(UserResourse, '/user')
api.add_resource(TokenResourse, '/token')

db.init_app(app)
api.init_app(app)

configure_app_cli(app)


if __name__ == '__main__':
    app.run(debug=True)
