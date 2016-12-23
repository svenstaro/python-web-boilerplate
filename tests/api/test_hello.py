"""Tests for `api.hello`."""
from requests import codes

from tests.utils import make_headers


class TestWhoami:
    """Tests for `api.hello.whoami`."""

    def test_success(self, client, user):
        """Can access protected resources when logged in."""
        resp = client.get("/whoami", headers=make_headers(user, "GET"))
        assert resp.status_code == codes.OK

    def test_cant_access_protected_routes_without_login(self, client):
        """Can't access protected resources when not logged in."""
        resp = client.get("/whoami")
        assert resp.status_code == codes.UNAUTHORIZED
