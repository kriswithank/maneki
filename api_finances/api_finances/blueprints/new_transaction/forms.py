import wtforms
from api_finances.utils.wtforms import ComboBoxField


class NewTransactionForm(wtforms.Form):
    date = wtforms.fields.DateField('Date', format='%Y-%m-%d')
    total = wtforms.IntegerField('Total')
    tax = wtforms.IntegerField('Tax')
    payment_type = ComboBoxField('Payment Type')
    retailer = ComboBoxField('Retailer')
    description = wtforms.TextAreaField('Description')
    #TODO: Add submit button and clear button


class ConfirmTransactionForm(wtforms.Form):
    confirm = wtforms.SubmitField('Confirm')
    cancel = wtforms.SubmitField('Cancel')
