"""RESTful resources for api involving users."""
from datetime import datetime, timedelta

import jwt
from flask import current_app, request
from flask.json import jsonify
from flask_restful import Resource
from functools import wraps
from marshmallow import (Schema, ValidationError, fields, validates,
                         validates_schema)
from webargs.flaskparser import use_args

from api import models
from api.resources.auth import authenticate

class UserResourse(Resource):
    """A restful resource for users."""

    def post(self):
        """Create a new user."""
        pass

    def put(self):
        """Change an existing user's password."""
        pass

    def delete(self):
        """Delete an existing user."""
        pass
