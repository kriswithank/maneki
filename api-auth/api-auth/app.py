"""
A RESTful api for authorizing users using Jason Web Tokens
"""
from datetime import datetime, timedelta

import click
import jwt
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'notverysecure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/postgres'
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    """A simple model representation of a user"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(1000))


class UserResourse(Resource):
    """A restful resource for users"""
    def put(self):
        """Create a new user"""
        pass

    def post(self):
        """Modify an existing user"""
        pass

    def delete(self):
        """Delete an existing user"""
        pass


token_parser = reqparse.RequestParser(bundle_errors=True)
token_parser.add_argument('username', required=True)
token_parser.add_argument('password', required=True)


class TokenResourse(Resource):
    """A RESTful resource for authorization tokens"""

    def get(self):
        """Get a JWT if the credentials are valid"""

        args = token_parser.parse_args()
        found_user = User.query.filter_by(username=args['username']).first()

        if found_user is None:
            return jsonify({'message': {'username': 'No such user exists'}})

        if found_user.password != args['password']:
            return jsonify({'message': {'password': 'Incorrect password'}})

        expiration = datetime.utcnow() + timedelta(hours=24)
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


api.add_resource(UserResourse, '/user')
api.add_resource(TokenResourse, '/token')


@app.route('/is-valid', methods=['GET'])
def is_valid():
    """
    A simple validation route for demo purposes, should be taken out (or maybe
    moved to the readme/wiki after we get some more infrastructure up
    """
    # Request must be JSON
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'})

    try:
        token = request.get_json()['token']
        print(str(token))
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'message': 'Success', 'data': data})
    except jwt.exceptions.ExpiredSignatureError:
        return jsonify({'message': 'Token has expired'})
    except jwt.exceptions.DecodeError:
        return jsonify({'message': 'Token is invalid'})
    except KeyError:
        return jsonify({'message': 'No token provided'})
    except:
        pass  # Ignore other exceptions

    return jsonify({'message': 'A fatal error has occured'})


@app.cli.command()
def initdb():
    """
    Create all SQLAlchemy tables

    Run from terminal using 'flask initdb'.
    """
    db.create_all()
    click.echo('Created all tables')


@app.cli.command()
def dropdb():
    """
    Drop all tables in database

    Run from terminal using 'flask dropdb'
    """
    db.drop_all()
    click.echo('Dropped all tables')


if __name__ == '__main__':
    app.run(debug=True)
