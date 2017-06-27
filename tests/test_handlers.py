"""Tests for handlers."""
import pytest
import uuid
from requests import codes

from flask import abort

from boilerplateapp.helpers.decorators import login_exempt

from tests.utils import make_headers


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestBeforeHandlers:
    """Tests for before_request handlers."""

    def test_send_data_without_json_content_type(self, client):
        """'POST' and 'PUT' methods always require the 'Content-Type' to be 'application/json'."""
        resp = client.post('/login')
        assert resp.status_code == codes.BAD_REQUEST

    def test_no_auth_required(self, app, client):
        """Do not require authentication for a few specific routes."""
        exempt_routes = [
            'api.login',
            'api.register',
        ]
        for rule in app.url_map.iter_rules():
            endpoint = str(rule.endpoint)
            view = app.view_functions[endpoint]

            if endpoint in exempt_routes:
                assert view.login_exempt is True
            else:
                assert not hasattr(view, 'login_exempt')

    def test_login_fail_no_authorization(self, client, user_factory):
        """Can't login without authorization in headers."""
        user_factory.get()
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        url = '/whoami'
        resp = client.get(url, headers=headers)

        assert resp.status_code == codes.BAD_REQUEST
        assert resp.json['message'] == "'Authorization' not found in headers."

    @pytest.mark.parametrize('token', ['invalid', 'Bearer: foobar'])
    def test_login_fail_invalid_format(self, client, user_factory, token):
        """Can't login with a wrongly formatted authorization header."""
        user_factory.get()
        headers = {
            'Accept': 'application/json',
            'Authorization': token,
            'Content-Type': 'application/json',
        }
        url = '/whoami'
        resp = client.get(url, headers=headers)

        assert resp.status_code == codes.BAD_REQUEST
        assert resp.json['message'] == "'Authorization' header has wrong format."

    def test_login_fail_other_user(self, app, client, user_factory):
        """Can't login with a login token that contains a valid auth token but another user id."""
        user = user_factory.get()
        other_user = user_factory.get()
        user.generate_auth_token()

        login_token = '{user_id}:{auth_token}'.format(
            user_id=other_user.id,
            auth_token=user.current_auth_token,
        )

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {login_token}'.format(login_token=login_token),
            'Content-Type': 'application/json',
        }
        url = '/whoami'

        resp = client.get(url, headers=headers)

        assert resp.status_code == codes.BAD_REQUEST
        assert resp.json['message'] == "Invalid login token."

    def test_login_fail_invalid_user(self, app, client, user_factory):
        """Can't login with a login token that contains an invalid user id."""
        user = user_factory.get()
        user.generate_auth_token()

        login_token = '{user_id}:{auth_token}'.format(
            user_id=uuid.uuid4(),
            auth_token=user.current_auth_token,
        )

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {login_token}'.format(login_token=login_token),
            'Content-Type': 'application/json',
        }
        url = '/whoami'

        resp = client.get(url, headers=headers)

        assert resp.status_code == codes.BAD_REQUEST
        assert resp.json['message'] == "Invalid login token."

    def test_login_fail_invalid_auth_token(self, app, client, user_factory):
        """Can't login with a login token that contains an invalid auth token."""
        user = user_factory.get()

        login_token = '{user_id}:{auth_token}'.format(
            user_id=user.id,
            auth_token=uuid.uuid4(),
        )

        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {login_token}'.format(login_token=login_token),
            'Content-Type': 'application/json',
        }
        url = '/whoami'

        resp = client.get(url, headers=headers)

        assert resp.status_code == codes.BAD_REQUEST
        assert resp.json['message'] == "Invalid login token."

    def test_error_handlers(self, app, client):
        """Error handlers work fine."""
        @app.route('/error-400')
        @login_exempt
        def error_400():
            abort(400)

        @app.route('/error-401')
        @login_exempt
        def error_401():
            abort(401)

        @app.route('/error-403')
        @login_exempt
        def error_403():
            abort(403)

        @app.route('/error-404')
        @login_exempt
        def error_404():
            abort(404)

        @app.route('/error-405')
        @login_exempt
        def error_405():
            abort(405)

        @app.route('/error-409')
        @login_exempt
        def error_409():
            abort(409)

        @app.route('/error-422')
        @login_exempt
        def error_422():
            abort(422)

        error_codes = [400, 401, 403, 404, 405, 409, 422]
        for error_code in error_codes:
            resp = client.get('/error-{code}'.format(code=error_code),
                              headers=make_headers('GET'))
            assert resp.status_code == error_code
            assert resp.json['message']


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestAfterRequestHandlers:
    """Tests for after_request handlers."""

    def test_cors_headers(self, client):
        """CORS headers are added to every request."""
        resp = client.get('/health_check')
        assert 'Access-Control-Allow-Origin' in resp.headers
        assert 'Access-Control-Allow-Methods' in resp.headers
        assert 'Access-Control-Allow-Headers' in resp.headers
