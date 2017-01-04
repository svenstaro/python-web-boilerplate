import pytest
from requests import codes


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestBeforeHandlers:
    """Tests for before_request handlers."""

    def test_send_data_without_json_content_type(self, client):
        """'POST' and 'PUT' methods always require the 'Content-Type' to be 'application/json'"""
        resp = client.post('/login')
        assert resp.status_code == codes.BAD_REQUEST


@pytest.mark.usefixtures('dbmodels', 'dbtransaction')
class TestAfterRequestHandlers:
    """Tests for after_request handlers."""

    def test_cors_headers(self, client):
        """CORS headers are added to every request."""
        resp = client.get('/health_check')
        assert 'Access-Control-Allow-Origin' in resp.headers
        assert 'Access-Control-Allow-Methods' in resp.headers
        assert 'Access-Control-Allow-Headers' in resp.headers
