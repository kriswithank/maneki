"""A RESTful api for authorizing users using Jason Web Tokens."""
from flask import Flask
from webargs.flaskparser import parser, use_args

from api_auth.commands import configure_app_cli
from api_auth.extensions import api, db
from api_auth.utils import JSONError, token_required
from api_auth.resources import UserResourse, TokenResourse, CredentialSchema


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


@app.route('/foo-route')
@token_required
@use_args(CredentialSchema())
def foo_route(data):
    """Test 'token-required' decorator."""
    return str(data)


api.add_resource(UserResourse, '/user')
api.add_resource(TokenResourse, '/token')

db.init_app(app)
api.init_app(app)

configure_app_cli(app)


if __name__ == '__main__':
    app.run(debug=True)
