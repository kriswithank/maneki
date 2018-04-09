from api.resources import (
    auth, transaction, user)


def register_resources(api):
    """Register Flask-RESTful resources to the given api."""
    api.add_resource(auth.TokenResourse, '/token')
    api.add_resource(transaction.TransactionResource, '/transaction/<int:transaction_id>')
    api.add_resource(transaction.TransactionListResource, '/transaction')
    api.add_resource(user.UserResourse, '/user')
