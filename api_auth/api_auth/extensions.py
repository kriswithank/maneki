"""General purpose extensions to the flask app."""
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()
