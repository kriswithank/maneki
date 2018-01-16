"""SQLAlchemy models for api_finances."""
from api_finances.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property

class Retailer(db.Model):
    """Model representation of a retailer."""

    __tablename__ = 'retailer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))

    transactions = db.relationship('Transaction', back_populates='retailer')


class PaymentType(db.Model):
    """
    Model representation of a payment type.

    Example: TCF Debit, Cash, Gift Card, etc.
    """

    __tablename__ = 'payment_type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    transactions = db.relationship('Transaction', back_populates='payment_type')


class Transaction(db.Model):
    """
    Model representation of a transaction.

    To be added int the future, make either a deposit or a withdrawal.

    Currency amounts are stored in cents so that we can store them as integers
    an not have to worry about inaccuracies with floating points.
    """

    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Integer)
    description = db.Column(db.Text, nullable=False)

    retailer_id = db.Column(db.Integer, db.ForeignKey('retailer.id'))
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'))

    retailer = db.relationship('Retailer', back_populates='transactions')
    payment_type = db.relationship('PaymentType', back_populates='transactions')

    @hybrid_property
    def decimal_total(self) -> float:
        return float(self.total / 100)

    @decimal_total.setter
    def decimal_total(self, decimal_value: float):
        self.total = int(decimal_value * 100)

    @hybrid_property
    def decimal_tax(self) -> float:
        return float(self.tax / 100)

    @decimal_tax.setter
    def decimal_tax(self, decimal_value: float):
        self.tax = int(decimal_value * 100)
