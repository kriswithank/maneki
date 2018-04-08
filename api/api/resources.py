"""RESTful resources for api."""
from datetime import datetime, timedelta

import jwt
from flask import current_app
from flask.json import jsonify
from flask_restful import Resource
from marshmallow import (Schema, ValidationError, fields, validates,
                         validates_schema)
from webargs.flaskparser import use_args

from api import models


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
        target_user = models.User.query.filter_by(username=value).first()
        if target_user is None:
            raise ValidationError('No such user exists.')

    @validates_schema(skip_on_field_errors=True)
    def password_is_correct(self, data):
        """
        Check that the password is correct for the given user.

        Since this is only run if all field validations pass, we know that target_user
        is not None.
        """
        target_user = models.User.query.filter_by(username=data['username']).first()
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
    def post(self, args):
        """Get a JWT if the credentials are valid."""
        expiration = datetime.utcnow() + timedelta(seconds=60)
        content = {
            'exp': expiration,
            'username': args['username'],
        }

        # Recall that encode returns a bytes object, so we will have to encode it
        # to be able to jsonify the token.
        token_bytes = jwt.encode(content, current_app.config['SECRET_KEY'], algorithm='HS256')
        token = token_bytes.decode('UTF-8')

        return jsonify({
            'message': 'Success',
            'token': token})


class TransactionResource(Resource):
    """A RESTful resource for transactions belonging to a user."""

    def get(self, user_id):
        """Return all transactions belonging to the given user."""
        transactions = models.Transaction.query.filter_by(user_id=user_id).all()
        return jsonify({
            'message': 'Success',
            'transactions': [{
                'id': t.id,
                'date': t.date,
                'description': t.description,
                'buyer_id': t.buyer.id,
                'seller_id': t.seller.id,
                'payment_type_id': t.payment_type.id,
                'transaction_categories': [{
                    'id': c.id,
                    'ammount': c.ammount,
                    'category_id': c.category.id,
                } for c in t.transaction_categories],
            } for t in transactions],
        })


def register_resources(api):
    """Register Flask-RESTful resources to the given api."""
    api.add_resource(UserResourse, '/user')
    api.add_resource(TokenResourse, '/token')
    api.add_resource(TransactionResource, '/transaction/<int:user_id>')
