from requests import codes

from tests.utils import make_headers


class TestWhoami:
    def test_success(self, client, user):
        """We'll get an error when trying to access a protected route."""

        resp = client.get("/whoami", headers=make_headers(user, "GET"))
        assert resp.status_code == codes.OK

    def test_cant_access_protected_routes_without_login(self, client):
        """We'll get an error when trying to access a protected route."""

        resp = client.get("/whoami")
        assert resp.status_code == codes.UNAUTHORIZED
