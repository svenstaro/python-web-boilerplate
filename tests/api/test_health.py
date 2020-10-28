from fastapi.testclient import TestClient


def test_healthcheck(app):
    with TestClient(app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert "Healthy" in response.json()
