"""
Tests for the resources in api_auth.resources.

Only the resources themselves are tested, schemas are not.
"""
import json

import pytest

from api_auth.extensions import db
from api_auth.models import User


class TestTokenResource:
    """Test the Token resource."""

    token_endpoint = '/token'

    @pytest.mark.parametrize('uname', ['test_user', 'somthing_else', '', None])
    @pytest.mark.parametrize('pword', ['password', '', None])
    def test_get_token_with_invalid_credentials(self, client, uname, pword):
        """Trying to get a token with invalid credentials fails."""
        # Add a temporary user to the database
        actual_username = 'test_user'
        actual_password = 'myactualpassword'
        user = User(username=actual_username, password=actual_password)
        db.session.add(user)

        # Attempt to get a token
        req_data = {'username': uname, 'password': pword}
        resp = client.get(self.token_endpoint, data=req_data)

        # Check the response for a token
        resp_data = json.loads(resp.data.decode('utf-8'))
        assert 'token' not in resp_data.keys()

        # Remove temporary user from database
        db.session.rollback()

    def test_get_token_with_valid_credentials(self, client):
        """Trying to get a token with valid credentials succeeds."""
        # Add a temporary user to the database
        actual_username = 'test_user'
        actual_password = 'myactualpassword'
        user = User(username=actual_username, password=actual_password)
        db.session.add(user)

        # Attempt to get a token
        req_data = {'username': actual_username, 'password': actual_password}
        resp = client.get(self.token_endpoint, data=req_data)

        # Check the response for a token
        resp_data = json.loads(resp.data.decode('utf-8'))
        assert 'token' in resp_data.keys()

        # Remove temporary user from database
        db.session.rollback()
