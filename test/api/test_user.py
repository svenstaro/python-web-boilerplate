from application.storage import UserInput, User, UserTokens
from fastapi.testclient import TestClient
import uuid


def test_proper_register(app):
    with TestClient(app) as client:
        resp = client.post("/register", json={"name": "user1", "password": "pwd1"})

        assert resp.status_code == 200
        assert resp.json()

def test_malformed_register(app):
    with TestClient(app) as client:
        resp = client.post("/register", json={"name":"user1", "password1": True})

        assert resp.status_code == 422

def test_no_double_names(app):
    with TestClient(app) as client:
        resp = client.post("/register", json={"name":"user1", "password":"pwd1"})

        assert not resp.json()

def test_no_token(app):
    with TestClient(app) as client:
        resp = client.get("/whoami")

        assert resp.status_code == 422 

def test_unknown_token(app):
    with TestClient(app) as client:
        resp = client.get("/whoami", headers={"auth-token":"totoro"})

        assert resp.status_code == 404
        # assert resp.message == "No such token" 

def test_worong_user_auth(app):
    with TestClient(app) as client:
        resp = client.post("/auth?access_origin=1", 
                json={"name":"user2", "password":"pwd1"})

        assert resp.status_code == 200
        assert resp.json() is None

def test_successful_auth(app, mocker):
    with TestClient(app) as client:
        mocker.patch('uuid.uuid4', return_value="lol")
        resp = client.post("/auth?access_origin=1", 
                json={"name":"user1", "password":"pwd1"})

        assert resp.status_code == 200
        assert resp.json()['token'] == "lol"

def test_succesful_whoami(app):
    with TestClient(app) as client:
        resp = client.get("/whoami", headers={"auth-token":"lol"})

        assert resp.status_code == 200
        assert resp.json()["name"] == "user1"

def test_no_user_delition(app):
    with TestClient(app) as client:
        resp = client.delete("/delete", json={"name":"usr2", "password":"pwd2"})

        assert resp.status_code == 200
        assert not resp.json()

def test_user_deletion(app):
    with TestClient(app) as client:
        resp = client.delete("/delete", json={"name":"user1", "password":"pwd1"})

        assert resp.status_code == 200
        assert resp.json()

