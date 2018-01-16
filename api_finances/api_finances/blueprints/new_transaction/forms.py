import wtforms
from api_finances.utils.wtforms import ComboBoxField


class NewTransactionForm(wtforms.Form):
    date = wtforms.fields.DateField(label='Date', format='%Y-%m-%d')
    total = wtforms.IntegerField(label='Total')
    tax = wtforms.IntegerField(label='Tax')
    payment_type = ComboBoxField(label='Payment Type')
    retailer = ComboBoxField(label='Retailer')
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
