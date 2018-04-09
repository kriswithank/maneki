"""RESTful resources for api involving auth."""

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

class AuthenticationSchema(Schema):
    """Marshmallow schema for validating user credentials."""

    class Meta:
        """Enforce required and validated fields by enabling strict evaluation."""

        strict = True
        additional = ('user_id',)

    username = fields.Str(required=True)
    password = fields.Str(required=True)

    @validates_schema(skip_on_field_errors=True)
    def validate_user(self, data):
        """Check that user exists and password is correct."""
        target_user = models.User.query.filter_by(username=data['username']).first()
        if target_user is None:
            raise ValidationError('No such user exists.', ['username'])
        if data['password'] != target_user.password:
            raise ValidationError('Password is incorrect.', ['password'])
        data['user_id'] = target_user.id


class TokenResourse(Resource):
    """A RESTful resource for authorization tokens."""

    @use_args(AuthenticationSchema())
    def post(self, args):
        """Get a JWT if the credentials are valid."""
        expiration = datetime.utcnow() + timedelta(minutes=15)
        payload = {
            'exp': expiration,
            'user_id': args['user_id'],
        }

        current_app.logger.warn('token args: ' + str(args))

        # Recall that encode returns a bytes object, so we will have to encode it
        # to be able to jsonify the token.
        token_bytes = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
        token = token_bytes.decode('UTF-8')

        return jsonify({
            'message': 'Success',
            'token': token})


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Recall that the http Authorization header has the form
        # Authorization: <type> <credentials/token>
        auth_header = request.headers.get('Authorization', None)

        if auth_header is None:
            return jsonify({
                'result': 'Error',
                'message': 'Must provide Authorization header'})

        auth_type = auth_header.split(' ')[0]
        token = auth_header.split(' ')[1]

        if auth_type != 'Bearer':
            return jsonify({
                'result': 'Error',
                'message': 'Must use Authorization type Bearer'})

        payload = None
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithm='HS256')
        except jwt.ExpiredSignatureError:
            return jsonify({
                'result': 'Error',
                'message': 'Token expired'})
        except Exception as e:
            return jsonify({
                'result': 'Error',
                'message': 'Could not decode jwt'})

        if 'user_id' not in payload:
            return jsonify({
                'result': 'Error',
                'message': 'JWT payload does not contain user id'})

        return func(*args, user_id=payload['user_id'], **kwargs)
    return wrapper

