from flask import (Blueprint, render_template, request, session, redirect,
                   url_for)
from werkzeug.datastructures import MultiDict
from api_finances import models
from api_finances.blueprints.new_transaction import forms


new_transaction = Blueprint(
    'new_transaction',
    __name__,
    template_folder='templates')


@new_transaction.route('/', methods=['GET', 'POST'])
def init():
    form = forms.NewTransactionForm(data=request.form)
    retailer_names = [retailer.name for retailer in models.Retailer.query.all()]
    payment_type_names = [type.name for type in models.PaymentType.query.all()]
    form.retailer.options = retailer_names
    form.payment_type.options = payment_type_names
    new_transaction_data = session.get('new_transaction_data', None)
    if request.method == 'GET' and new_transaction_data is not None:
        form = forms.NewTransactionForm(formdata=MultiDict(new_transaction_data))
    if request.method == 'POST' and form.validate():
        session['new_transaction_data'] = MultiDict(form.data)
        return redirect(url_for('new_transaction.confirm'), 307)
    return render_template(
        'new_transaction/init.html',
        new_transaction_data=new_transaction_data,
        form=form)


@new_transaction.route('/confirm', methods=['GET', 'POST'])
def confirm():
    # Redirect if new_transaction not in session
    new_transaction_data = session.get('new_transaction_data', None)
    if new_transaction_data is None:
        return redirect(url_for('new_transaction.init'))
    form = forms.ConfirmTransactionForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.confirm.data:
            return 'Confirm'
        elif form.cancel.data:
            session.pop('new_transaction_data')
            return 'Cancel, popped from session'
    return render_template(
        'new_transaction/confirm.html',
        new_transaction_data=new_transaction_data,
        form=form)
