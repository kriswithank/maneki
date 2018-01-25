import wtforms
from decimal import Decimal
from wtforms import validators
from finances.utils.wtforms import ComboBoxField


class NewTransactionForm(wtforms.Form):
    date = wtforms.fields.DateField(
        label='Date',
        format='%Y-%m-%d',
        validators=[validators.DataRequired()])
    total = wtforms.DecimalField(
        label='Total',
        places=2,
        validators=[
            validators.InputRequired(),
            validators.NumberRange(
                min=Decimal('0.01'),
                message='Must have transaction of at least 1 cent')])
    tax = wtforms.DecimalField(
        label='Tax',
        places=2,
        validators=[
            validators.InputRequired(),
            validators.NumberRange(
                min=0,
                message='Cannot have negative tax')])
    payment_type = ComboBoxField(
        label='Payment Type',
        validators=[validators.DataRequired()])
    retailer = ComboBoxField(
        label='Retailer',
        validators=[validators.DataRequired()])
    #TODO: Add submit button and clear button


class ConfirmTransactionForm(wtforms.Form):
    date = wtforms.HiddenField()
    total = wtforms.HiddenField()
    tax = wtforms.HiddenField()
    payment_type = wtforms.HiddenField()
    retailer = wtforms.HiddenField()
    description = wtforms.TextAreaField(label='Description')
    confirm = wtforms.SubmitField(label='Confirm')
    cancel = wtforms.SubmitField(label='Cancel')
