"""The flask app and app configuration for api_auth."""
from flask import Flask
from webargs.flaskparser import parser, use_args

from api_auth.commands import register_commands
from api_auth.extensions import api, register_extensions
from api_auth.resources import CredentialSchema, register_resources
from api_auth.utils import JSONError, token_required


app = Flask(__name__)
app.config['SECRET_KEY'] = 'notverysecure'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/auth'


@app.errorhandler(JSONError)
def handle_jsonerror(error):
    """Return a jsonified response of a ValidationError's payload when it raised and uncaught."""
    return error.get_response()


@parser.error_handler
def handle_error(error):
    """
    Handle webargs ValidationErrors by converting them to a JSONError.

    This will jsonify the payload.
    """
    raise JSONError(error.messages)


@app.route('/foo-route')
@token_required
@use_args(CredentialSchema())
def foo_route(data):
    """Test 'token-required' decorator."""
    return str(data)


register_resources(api)
register_extensions(app)
register_commands(app)


if __name__ == '__main__':
    app.run(debug=True)
