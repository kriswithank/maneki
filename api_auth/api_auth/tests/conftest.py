"""Common pytest fixtures that are automatically loaded for use."""
from api_auth import app as auth_app, const, utils
from api_auth.extensions import db
import pytest

# pylint: disable=redefined-outer-name


@pytest.fixture(scope='session')
def app():
    """Return an instance of the flask app configured with test env variables."""
    app = auth_app.create_app(const.CONFIG_TESTING)
    with app.app_context():
        utils.create_sqla_db(app, db)
        yield app


@pytest.fixture
def client(app):
    """Return the testing client of the flask app."""
    return app.test_client()
