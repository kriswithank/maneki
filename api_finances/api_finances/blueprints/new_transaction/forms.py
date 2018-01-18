import wtforms
from wtforms import validators
from api_finances.utils.wtforms import ComboBoxField


class NewTransactionForm(wtforms.Form):
    date = wtforms.fields.DateField(
        label='Date',
        format='%Y-%m-%d',
        validators=[validators.DataRequired()])
    total = wtforms.DecimalField(
        label='Total',
        places=2,
        validators=[validators.DataRequired()])
    tax = wtforms.DecimalField(
        label='Tax',
        places=2,
        validators=[validators.DataRequired()])
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
