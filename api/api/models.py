"""SQLAlchemy models for api."""
from api.extensions import db


class User(db.Model):
    """A simple model representation of a user."""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(1000))

    retailers = db.relationship('Retailer', back_populates='user')
    payment_types = db.relationship('PaymentType', back_populates='user')
    categories = db.relationship('Category', back_populates='user')
    transactions = db.relationship('Transaction', back_populates='user')


class Retailer(db.Model):
    """Model representation of a retailer."""

    __tablename__ = 'retailer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(1000), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='retailers')

    transactions_buyer = db.relationship('Transaction', back_populates='buyer')
    transactions_seller = db.relationship('Transaction', back_populates='seller')


class PaymentType(db.Model):
    """Model representation of a payment type."""

    __tablename__ = 'payment_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='payment_types')

    transactions = db.relationship('Transaction', back_populates='payment_type')


class Transaction(db.Model):
    """
    Model representation of a transaction.

    Currency amounts are stored in cents so that we can store them as integers
    an not have to worry about inaccuracies with floating points.
    """

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)

    buyer_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    buyer = db.relationship('Retailer', back_populates='transactions_buyer')

    seller_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    seller = db.relationship('Retailer', back_populates='transactions_seller')

    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'))
    payment_type = db.relationship('PaymentType', back_populates='transactions')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='transactions')

    transaction_categories = db.relationship('TransactionCategory', back_populates='transaction')


class Category(db.Model):
    """Model representation of a category."""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(1000), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='categories')

    transaction_categories = db.relationship('TransactionCategory', back_populates='category')


class TransactionCategory(db.Model):
    """Model representation of an ammount tied to a transaction and category."""

    __tablename__ = 'transaction_category'

    id = db.Column(db.Integer, primary_key=True)

    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))
    transaction = db.relationship('Transaction', back_populates='transaction_categories')

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    Category = db.relationship('Category', back_populates='transaction_categories')
