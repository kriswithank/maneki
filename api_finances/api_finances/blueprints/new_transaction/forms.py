import wtforms
from api_finances.utils.wtforms import ComboBoxField


class NewTransactionForm(wtforms.Form):
    date = wtforms.fields.DateField(label='Date', format='%Y-%m-%d')
    total = wtforms.IntegerField(label='Total')
    tax = wtforms.IntegerField(label='Tax')
    payment_type = ComboBoxField(label='Payment Type')
    retailer = ComboBoxField(label='Retailer')
    description = wtforms.TextAreaField(label='Description')
    #TODO: Add submit button and clear button


class ConfirmTransactionForm(wtforms.Form):
    confirm = wtforms.SubmitField(label='Confirm')
    cancel = wtforms.SubmitField(label='Cancel')
