from flask import (Blueprint, render_template, request, session, redirect,
                   url_for)
from werkzeug.datastructures import ImmutableMultiDict
from api_finances import models
from api_finances.blueprints.new_transaction import forms


new_transaction = Blueprint(
    'new_transaction',
    __name__,
    template_folder='templates')


@new_transaction.route('/', methods=['GET', 'POST'])
def init():
    form = forms.NewTransactionForm(request.form)
    retailer_names = [retailer.name for retailer in models.Retailer.query.all()]
    form.retailer.widget.options = retailer_names
    payment_type_names = [type.name for type in models.PaymentType.query.all()]
    form.payment_type.widget.options = payment_type_names
    if request.method == 'POST' and form.validate():
        session['new_transaction_data'] = form.data
        # {
        #     'date': form.date.data,
        #     'total': form.total.data,
        #     'tax': form.tax.data,
        #     'payment_type': form.payment_type.data,
        #     'retailer': form.retailer.data,
        #     'description': form.description.data}
        return redirect(url_for('add_transaction_confirm'))
    return render_template('new_transaction/init.html', form=form)


@new_transaction.route('/update', methods=['GET', 'POST'])
def add_transaction_update():
    form = forms.NewTransactionForm(request.form)
    retailer_names = [retailer.name for retailer in models.Retailer.query.all()]
    form.retailer.widget.options = retailer_names
    payment_type_names = [type.name for type in models.PaymentType.query.all()]
    form.payment_type.widget.options = payment_type_names
    new_transaction_data = session.get('new_transaction_data', None)
    if request.method == 'GET' and new_transaction_data is not None:
        form = forms.NewTransactionForm(data=new_transaction_data)
        form.payment_type.data = 'foobar'
        # form.date.data = new_transaction_data['date']
        # form.total.data = new_transaction_data['total']
        # form.tax.data = new_transaction_data['tax']
        # form.payment_type.data = new_transaction_data['payment_type']
        # form.retailer.data = new_transaction_data['retailer']
        # form.description.data = new_transaction_data['description']
    if request.method == 'POST' and form.validate():
        session['new_transaction_data'] = form.data
        # {
        #     'date': form.date.data,
        #     'total': form.total.data,
        #     'tax': form.tax.data,
        #     'payment_type': form.payment_type.data,
        #     'retailer': form.retailer.data,
        #     'description': form.description.data}
        return redirect(url_for('new_transaction.confirm'))
    return render_template(
        'new_transaction/update.html',
        new_transaction_data=ImmutableMultiDict(new_transaction_data),
        form=form)


@new_transaction.route('/confirm', methods=['GET', 'POST'])
def add_transaction_confirm():
    # Redirect if new_transaction not in session
    new_transaction_data = session.get('new_transaction_data', None)
    if new_transaction_data is None:
        return redirect(url_for('add_transaction_new'))
    form = forms.ConfirmTransactionForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.confirm:
            return 'Confirm'
        elif form.cancel:
            return 'Cancel'
    return render_template(
        'new_transaction/confirm.html',
        new_transaction_data=new_transaction_data,
        form=form)
