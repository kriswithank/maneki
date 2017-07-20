"""A RESTful api for authorizing users using Jason Web Tokens."""
from datetime import datetime, timedelta
from functools import wraps

import click
import jwt
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from webargs import fields, ValidationError
from webargs.flaskparser import parser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notverysecure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/postgres'
db = SQLAlchemy(app)
api = Api(app)


class JSONError(Exception):
    """Represent errors that have a payload that should be a jsonified response."""

    def __init__(self, payload):
        """Create a new ValidationError with the payload to jsonify."""
        super().__init__()
        self.payload = payload

    def get_response(self):
        """Get the jsonified response of the payload."""
        return jsonify(self.payload)


@app.errorhandler(JSONError)
def handle_jsonerror(error):
    """Return a jsonified response of a ValidationError's payload when it raised and uncaught."""
    return error.get_response()


@parser.error_handler
def handle_error(error):
    """Handle validations errors by just converting them to a JSONError."""
    raise JSONError(error.messages)


def is_token_valid(token):
    """Return True iff the token is valid, otherwise raise a ValidationError."""
    try:
        jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
    except jwt.exceptions.ExpiredSignatureError:
        raise ValidationError('Token is expired')
    except jwt.exceptions.DecodeError:
        raise ValidationError('Token is invalid')

    return True


token_args = {
    'token': fields.Str(required=True, validate=is_token_valid)
}


def token_required(func):
    """Require decorated function to be provided a valid token."""
    @wraps(func)
    def validate_token(*args, **kwargs):
        """Parse the args, validation is done during the parse."""
        parser.parse(token_args, request)
        return func(*args, **kwargs)
    return validate_token


token_parser = reqparse.RequestParser(bundle_errors=True)
token_parser.add_argument('username', required=True)
token_parser.add_argument('password', required=True)


@app.route('/foo-testing', methods=['GET', 'POST'])
def foo_testing():
    """Test out the webargs module."""
    args = parser.parse(token_args, request)
    return "your token was: {}\n".format(args['token'])


@app.route('/temp-testing', methods=['GET', 'POST'])
@token_required
def temp_testing():
    """Test token_required decorator."""
    return 'you should only see this if you have a valid token'


class User(db.Model):
    """A simple model representation of a user."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(1000))


class UserResourse(Resource):
    """A restful resource for users."""

    def put(self):
        """Create a new user."""
        pass

    def post(self):
        """Modify an existing user."""
        pass

    def delete(self):
        """Delete an existing user."""
        pass


class TokenResourse(Resource):
    """A RESTful resource for authorization tokens."""

    def get(self):
        """Get a JWT if the credentials are valid."""
        args = token_parser.parse_args()
        found_user = User.query.filter_by(username=args['username']).first()

        if found_user is None:
            return jsonify({'message': {'username': 'No such user exists'}})

        if found_user.password != args['password']:
            return jsonify({'message': {'password': 'Incorrect password'}})

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


# class UserResource(Resource):
#     """A restful resource for users"""
#     def post(self):
#         """Change a user's password"""
#         # Request must be JSON
#         if not request.is_json:
#             return jsonify({'message': 'Request must be JSON'})

#         try:
#             token = request.get_json()['token']
#             token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')

#             print('got token and token_data')

#             username = token_data['username']
#             new_password = request.get_json()['new_password']

#             print('got username and new password from request')

#             found_user = User.query.filter_by(username=username).first()

#             if found_user is None:
#                 return jsonify({'message': 'Failure, user does not exist'})

#             found_user.password = new_password
#             db.session.add(found_user)
#             db.session.commit(found_user)

#             return jsonify({'message': 'Success, password changed'})
#         except jwt.exceptions.ExpiredSignatureError:
#             return jsonify({'message': 'Token has expired'})
#         except jwt.exceptions.DecodeError:
#             return jsonify({'message': 'Token is invalid'})
#         except KeyError:
#             return jsonify({'message': 'No token provided'})
#         except:
#             pass  # Ignore other exceptions

#         return jsonify({'message': 'A fatal error has occured'})


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


if __name__ == '__main__':
    app.run(debug=True)
