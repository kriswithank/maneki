"""
A restful api for authorizing users using Jason Web Tokens
"""
from datetime import datetime, timedelta

import click
import jwt
from flask import Flask, request
from flask.json import jsonify
from flask_restful import Api, Resource
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


class UserResource(Resource):
    """A restful resource for users"""
    def post(self):
        """Change a user's password"""
        # Request must be JSON
        if not request.is_json:
            return jsonify({'message': 'Request must be JSON'})

        try:
            token = request.get_json()['token']
            token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithm='HS256')

            print('got token and token_data')

            username = token_data['username']
            new_password = request.get_json()['new_password']

            print('got username and new password from request')

            found_user = User.query.filter_by(username=username).first()

            if found_user is None:
                return jsonify({'message': 'Failure, user does not exist'})

            found_user.password = new_password
            db.session.add(found_user)
            db.session.commit(found_user)

            return jsonify({'message': 'Success, password changed'})
        except jwt.exceptions.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'})
        except jwt.exceptions.DecodeError:
            return jsonify({'message': 'Token is invalid'})
        except KeyError:
            return jsonify({'message': 'No token provided'})
        except:
            pass  # Ignore other exceptions

        return jsonify({'message': 'A fatal error has occured'})


api.add_resource(UserResource, '/user')


@app.route('/test-post', methods=['POST'])
def test_post_endpoint():
    """A temporary endpoint to test how passing data works in flask"""
    json_stuff = request.get_json()
    print(str(json_stuff))
    foo_data = json_stuff['foo']
    bar_data = request.form.get('bar')
    return 'The passed data was foo:{0} bar:{1}'.format(foo_data, bar_data)


# Once we get tests up, this should be the only route left
@app.route('/get-token', methods=['GET'])
def get_token():
    """
    Returns a JSON repsonse with JWT token for validation in other apis.

    Expects a GET response with 'Content-Type: application/json' header and
    data of the form {"username": "someuser", "password": "someuserspassword"}.

    Returns a JSON response of the form
        {"message": "someresponse", "token": "sometoken"}
    The token key is only present in the event of a successful authorization.

    Token expires after 24 hours.
    """
    # Request must be JSON
    if not request.is_json:
        return jsonify({'message': 'Request must be JSON'})

    try:
        req_username = request.get_json()['username']
    except:
        return jsonify({'message': 'No username provided'})

    try:
        req_password = request.get_json()['password']
    except:
        return jsonify({'message': 'No password provided'})

    found_user = User.query.filter_by(username=req_username).first()

    if found_user is None:
        return jsonify({'message': 'No such user exists'})

    if found_user.password != req_password:
        return jsonify({'message': 'Incorrect password'})

    expiration = datetime.utcnow() + timedelta(hours=24)

    content = {
        'exp': expiration,
        'username': req_username,
    }

    # Recall that encode returns a bytes object, so we will have to encode it
    # to be able to jsonify the token.
    token_bytes = jwt.encode(content, app.config['SECRET_KEY'], algorithm='HS256')
    token = token_bytes.decode('UTF-8')

    return jsonify({
        'message': 'Success',
        'token': token})


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
