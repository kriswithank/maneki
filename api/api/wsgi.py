"""
Provides a way to run api.

Running with flask run requires that app be defined outside the `if`
statment since it auto-discovers `app`.
You can also start the app by simply runing this file via
    `python /path/to/this/file/wsgi.py`
"""
from os import environ

from api.app import create_app

app = create_app(environ['FLASK_CONFIG_OVERRIDE'])

if __name__ == "__main__":
    app.run()
