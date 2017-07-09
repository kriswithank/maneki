import click
from flask import Flask
from flask.json import jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@database/postgres'
db = SQLAlchemy(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class HelloWorld(Resource):
    def get(self):
        users = User.query.all()
        new_user_name = 'myuser{0}'.format(str(len(users)))
        new_user = User(new_user_name, '{0}@gmail.com'.format(new_user_name))
        db.session.add(new_user)
        db.session.commit()
        latest_user = User.query.all()[-1]
        return jsonify({'username': latest_user.username, 'email': latest_user.email})


api.add_resource(HelloWorld, '/')


@app.cli.command()
def initdb():
    db.create_all()
    click.echo('Created all tables')


@app.cli.command()
def dropdb():
    db.drop_all()
    click.echo('Dropped all tables')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
