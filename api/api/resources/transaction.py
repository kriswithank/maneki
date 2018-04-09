"""RESTful resources for api involving transactions."""
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


class TransactionResource(Resource):
    """A RESTful resource for a single transaction."""

    @authenticate  # Provides user_id
    def get(self, user_id, transaction_id):
        """Return the transaction id given if the user has access to it."""
        pass

    @authenticate  # Provides user_id
    def put(self, user_id, transaction_id):
        """Return the transaction id given if the user has access to it."""
        pass



class TransactionListResource(Resource):
    """A RESTful resource for many transactions belonging to a user."""

    @authenticate  # Provides user_id
    def get(self, user_id):
        """Return all transactions belonging to the authenticated user."""
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

    @authenticate  # Provides user_id
    # @use_args(TransactionSchema())
    def post(self, user_id):
        """Add a new transaction for the authenticated user."""
        pass


