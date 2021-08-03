from fastapi.testclient import TestClient

import pytest

from main import app


client = TestClient(app)

valid_data = {
    "name": "string",
    "username": "string",
    "email": "user@example.com",
    "phone": "string"    
}

invalid_data = {
    "name": 10,
    "username": "string",
    "email": "userexample.com",
    "phone": "string"
}

@pytest.fixture
def user():
    test_user = {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "phone": "1-770-736-8031 x56442"
        }
    return test_user

def test_get_users_statuc_code():
    response = client.get("/users")
    assert response.status_code == 200

def test_get_users_fields(user):
    response = client.get("/users")
    resp = response.json()[0]
    assert resp["id"] == user['id']
    assert resp["name"] == user['name']
    assert resp["phone"] == user['phone']
    assert resp["email"] == user['email']
    assert resp["username"] == user['username']


class TestUserCreation:

    def test_create_user(self):
        response = client.post("/users/", json=valid_data)
        assert response.status_code == 201
        resp = response.json()
        assert resp["id"] == 11
        assert resp["name"] == valid_data["name"]
        assert resp["phone"] == valid_data["phone"]
        assert resp["email"] == valid_data["email"]
        assert resp["username"] == valid_data["username"]

    def test_invalid_creation(self):
        response = client.post("/users/", json=invalid_data)
        assert response.status_code == 422
        resp = response.json()
        assert len(resp.keys()) == 1