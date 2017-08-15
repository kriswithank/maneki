"""
Contains common components for api-finances

Such as: app, db, api
"""
from flask import Flask
from flask.json import jsonify
from flask_restful import Resource

from api_finances.extensions import db, api, register_extensions
from api_finances.commands import register_commands

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/finances'


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


api.add_resource(HelloWorld, '/')

register_extensions(app)
register_commands(app)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
