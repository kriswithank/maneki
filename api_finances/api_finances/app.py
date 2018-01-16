"""
Contains common components for api-finances

Such as: app, db, api
"""
import wtforms
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask.json import jsonify
from flask_restful import Resource
from datetime import datetime
from werkzeug.datastructures import ImmutableMultiDict

from api_finances.extensions import db, api, register_extensions
from api_finances.commands import register_commands
from api_finances import models
from api_finances.utils.wtforms import ComboBoxField
from api_finances.blueprints.new_transaction.views import new_transaction


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/finances'
app.config["APPLICATION_ROOT"] = '/finances'
app.secret_key = 'notsosecret'


class ReverseProxied(object):
    """
    Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.
    In nginx:
    location /prefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /prefix;
        }
    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ.get('PATH_INFO', '')
            if path_info and path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]
        server = environ.get('HTTP_X_FORWARDED_SERVER_CUSTOM',
                             environ.get('HTTP_X_FORWARDED_SERVER', ''))
        if server:
            environ['HTTP_HOST'] = server
        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


app.wsgi_app = ReverseProxied(app.wsgi_app)


class NewRetailerForm(wtforms.Form):
    name = wtforms.StringField(
        'Name',
        [wtforms.validators.Length(min=4, max=120)])
    submit = wtforms.SubmitField('Add Retailer')


class NewPaymentTypeForm(wtforms.Form):
    name = wtforms.StringField(
        'Payment Type',
        [wtforms.validators.Length(min=4, max=120)])
    submit = wtforms.SubmitField('Add Payment Type')


@app.route('/add_retailer', methods=['POST'])
def add_retailer():
    new_retailer_form = NewRetailerForm(request.form)
    new_payment_type_form = NewPaymentTypeForm(request.form)
    if new_retailer_form.validate():
        new_retailer = models.Retailer(name=new_retailer_form.name.data)
        db.session.add(new_retailer)
        db.session.commit()
        flash('Retailer added')
    return render_template(
        'index.html',
        new_retailer_form=new_retailer_form,
        new_payment_type_form=new_payment_type_form,
        transactions=models.Transaction.query.all(),
        retailers=models.Retailer.query.all(),
        payment_types=models.PaymentType.query.all())


@app.route('/add_payment_type', methods=['POST'])
def add_payment_type():
    new_retailer_form = NewRetailerForm(request.form)
    new_payment_type_form = NewPaymentTypeForm(request.form)
    if new_payment_type_form.validate():
        new_payment_type = models.PaymentType(
            name=new_payment_type_form.name.data)
        db.session.add(new_payment_type)
        db.session.commit()
        flash('New payment type added')
    return render_template(
        'index.html',
        new_retailer_form=new_retailer_form,
        new_payment_type_form=new_payment_type_form,
        transactions=models.Transaction.query.all(),
        retailers=models.Retailer.query.all(),
        payment_types=models.PaymentType.query.all())


class User(db.Model):
    """A temporary class that's being used for testing purposes"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class HelloWorld(Resource):
    """Another temporary class for testing purposes"""
    def get(self):
        """A test method which gets the latest user entered"""
        users = User.query.all()
        new_user_name = 'myuser{0}'.format(str(len(users)))
        new_user = User(new_user_name, '{0}@gmail.com'.format(new_user_name))
        db.session.add(new_user)
        db.session.commit()
        latest_user = User.query.all()[-1]
        return jsonify({'username': latest_user.username, 'email': latest_user.email})


api.add_resource(HelloWorld, '/hellowworld')


@app.route('/', methods=['GET', 'POST'])
def index():
    new_retailer_form = NewRetailerForm(request.form)
    new_payment_type_form = NewPaymentTypeForm(request.form)
    return render_template(
        'index.html',
        new_retailer_form=new_retailer_form,
        new_payment_type_form=new_payment_type_form,
        transactions=models.Transaction.query.all(),
        retailers=models.Retailer.query.all(),
        payment_types=models.PaymentType.query.all())


register_extensions(app)
register_commands(app)
app.register_blueprint(new_transaction, url_prefix='/new_transaction')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
