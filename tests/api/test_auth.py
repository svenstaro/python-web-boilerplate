"""Tests for `api.auth`."""
import pytest
import json
from datetime import datetime, timedelta

from freezegun import freeze_time
from requests import codes

from boilerplateapp.extensions import db
from boilerplateapp.models.user import User

from tests.utils import make_headers


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestLogin:
    """Tests for `api.auth.login`."""

    def test_success(self, app, client, user_factory):
        """Can log in and get back a valid token."""
        user = user_factory.get()
        resp = client.post("/login",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": user.email,
                                            "password": "testtest"}))
        assert resp.status_code == codes.OK
        assert resp.json['token'] == user.current_auth_token

    def test_same_auth_token(self, app, client, user_factory):
        """Can log in and get back the same auth token if there's already a valid one."""
        user = user_factory.get()
        client.post("/login",
                    headers=make_headers('POST'),
                    data=json.dumps({"email": user.email,
                                     "password": "testtest"}))
        current_token = user.current_auth_token
        client.post("/login",
                    headers=make_headers('POST'),
                    data=json.dumps({"email": user.email,
                                     "password": "testtest"}))
        db.session.refresh(user)
        assert current_token == user.current_auth_token

    def test_fail_wrong_username(self, app, client, user_factory):
        """Can't login with a wrong username and get an error."""
        user_factory.get()
        resp = client.post("/login",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": "invalid@example.com",
                                            "password": "testtest"}))
        assert resp.status_code == codes.UNAUTHORIZED
        assert not resp.json.get('data')

    def test_fail_wrong_password(self, app, client, user_factory):
        """Can't login with a wrong username and get an error."""
        user = user_factory.get()
        resp = client.post("/login",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": user.email, "password": "invalid"}))
        assert resp.status_code == codes.UNAUTHORIZED
        assert not resp.json.get('data')


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestRegister:
    """Tests for `api.auth.register`."""

    def test_success(self, app, client):
        """Can register a new account with email and password and then log in with it."""
        new_email = "newuser@example.com"
        new_password = "test"
        resp = client.post("/register",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.CREATED
        new_user_id = resp.json['id']
        assert resp.json == {"id": new_user_id, "email": new_email}

        # Now try to log in using the new account.
        resp = client.post("/login",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.OK
        assert resp.json['token']

    def test_fail_on_duplicate_email(self, app, client):
        """Can't register with an existing email."""
        new_email = "newuser@example.com"
        new_password = "test"
        resp = client.post("/register",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.CREATED

        # Now try to create a new account with the same email.
        resp = client.post("/register",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.CONFLICT

    def test_fail_on_invalid_email(self, app, client):
        """Can't register with an invalid email."""
        new_email = "invalid"
        new_password = "test"
        resp = client.post("/register",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.UNPROCESSABLE_ENTITY
        assert db.session.query(User).count() == 0

    def test_fail_on_empty_email(self, app, client):
        """Can't register with an empty email."""
        new_email = ""
        new_password = "test"
        resp = client.post("/register",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.UNPROCESSABLE_ENTITY
        assert db.session.query(User).count() == 0

    def test_fail_on_empty_password(self, app, client):
        """Can't register with an empty password."""
        new_email = ""
        new_password = ""
        resp = client.post("/register",
                           headers=make_headers('POST'),
                           data=json.dumps({"email": new_email, "password": new_password}))
        assert resp.status_code == codes.UNPROCESSABLE_ENTITY
        assert db.session.query(User).count() == 0


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestLastAction:
    """Tests for User.last_action behavior and auth token timeouts."""

    def test_last_action_is_refreshed(self, app, client, user_factory):
        """With every authenticated API request, the last_action column is refreshed."""
        user = user_factory.get()
        client.get("/whoami", headers=make_headers("GET", user))
        last_action_old = user.last_action
        client.get("/whoami", headers=make_headers("GET", user))
        last_action_new = user.last_action
        assert last_action_old < last_action_new

    def test_last_action_can_get_too_old(self, app, client, user_factory):
        """An error is thrown if using an old auth token."""
        user = user_factory.get()
        headers = make_headers("GET", user)
        with freeze_time(datetime.utcnow() + app.config['AUTH_TOKEN_TIMEOUT'] + timedelta(days=1)):
            resp = client.get("/whoami", headers=headers)
            assert resp.status_code == codes.UNAUTHORIZED
            assert resp.json['message'] == "Auth token too old, please log in again."
