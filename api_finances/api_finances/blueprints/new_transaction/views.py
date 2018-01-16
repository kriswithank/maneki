from flask import (Blueprint, render_template, request, session, redirect,
                   url_for, flash)
from werkzeug.datastructures import MultiDict
from api_finances import models
from api_finances.blueprints.new_transaction import forms
from api_finances.extensions import db


new_transaction = Blueprint(
    'new_transaction',
    __name__,
    template_folder='templates')


@new_transaction.route('/', methods=['GET', 'POST'])
def init():
    form = forms.NewTransactionForm(request.form)
    retailer_names = [retailer.name for retailer in models.Retailer.query.all()]
    payment_type_names = [type.name for type in models.PaymentType.query.all()]
    form.retailer.options = retailer_names
    form.payment_type.options = payment_type_names
    if request.method == 'POST' and form.validate():
        if form.payment_type.data not in retailer_names:
            flash(f'Payment type {form.payment_type.data} does not exist, '
                  f'a new payment type will be created')
        if form.retailer.data not in retailer_names:
            flash(f'Retailer {form.retailer.data} does not exist, '
                  f'a new retailer will be created')
        return redirect(url_for('new_transaction.confirm'), 307)
    return render_template('new_transaction/init.html', form=form)


@new_transaction.route('/confirm', methods=['GET', 'POST'])
def confirm():
    # Redirect if new_transaction can't pass init form
    temp_init_form = forms.NewTransactionForm(request.form)
    if not temp_init_form.validate():
        return redirect(url_for('new_transaction.init'), 307)
    form = forms.ConfirmTransactionForm(request.form)
    if request.method == 'POST' and form.validate():
        if form.confirm.data:
            retailer = models.Retailer.query.filter_by(
                name=form.retailer.data).first()
            payment_type = models.PaymentType.query.filter_by(
                name=form.payment_type.data).first()
            if retailer is None:
                retailer = models.Retailer(name=form.retailer.data)
                db.session.add(retailer)
                flash(f'New retailer {retailer.name} created')
            if payment_type is None:
                payment_type = models.PaymentType(name=form.payment_type.data)
                db.session.add(payment_type)
                flash(f'New payment type {payment_type.name} created')
            transaction = models.Transaction(
                date=form.date.data,
                total=form.total.data,
                tax=form.tax.data,
                description=form.description.data,
                retailer=retailer,
                payment_type=payment_type)
            db.session.add(transaction)
            db.session.commit()
            return redirect(url_for('index'))
        elif form.cancel.data:
            return 'Cancel, popped from session'
    return render_template(
        'new_transaction/confirm.html',
        form=form)
