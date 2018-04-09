"""The api flask app factory."""
from os import environ

from flask import Flask
from webargs.flaskparser import parser, use_args

from api import const
from api.commands import register_commands
from api.extensions import api, register_extensions
from api.resources.register import register_resources
from api.utils import JSONError


def create_app(config_override_file=None):
    """
    Create a flask app for api.

    Reads in two optional environment variables, FLASK_CONFIG_BASE AND FLASK_CONFIG_OVERRIDE.
    FLASK_BASE_CONFIG specifies the base configuration to use, if nothing is given then it
    defaults to api/config/base.cfg.
    FLASK_CONFIG_OVERRIDE provides overrides for the base config.
    Note that you will probably have to provide one of these files since the SECRET_KEY must
    be set and currently there is no secret key being set in the base config (this to ensure
    that production does not use an insecure SECRET_KEY).
    """
    # pylint: disable=redefined-outer-name,unused-variable
    app = Flask(__name__)

    # Read in the base config (will read from '../cofnig/base.cfg' if FLASK_BASE_CONFIG isn't set
    environ.setdefault('FLASK_BASE_CONFIG', const.CONFIG_DEFAULT_BASE)
    app.config.from_envvar('FLASK_BASE_CONFIG')

    # Load in additional configuration overrides if provided
    if config_override_file is not None:
        app.config.from_pyfile(config_override_file)

    @app.errorhandler(JSONError)
    def handle_jsonerror(error):
        """Return a jsonified response of an uncaught ValidationError's payload."""
        return error.get_response()

    @parser.error_handler
    def handle_error(error):
        """
        Handle webargs ValidationErrors by converting them to a JSONError.

        This will jsonify the payload.
        """
        raise JSONError(error.messages)

    register_resources(api)
    register_extensions(app)
    register_commands(app)

    return app
