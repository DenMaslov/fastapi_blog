from fastapi.testclient import TestClient

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

def test_get_users_statuc_code():
    response = client.get("/users")
    assert response.status_code == 200

def test_get_users_fields():
    response = client.get("/users")
    resp = response.json()[0]
    assert isinstance(resp["id"], int)
    assert isinstance(resp["name"], str)
    assert isinstance(resp["phone"], str)
    assert isinstance(resp["email"], str)
    assert isinstance(resp["username"], str)

def test_create_user():
    response = client.post("/users/", json=valid_data)
    assert response.status_code == 201
    resp = response.json()
    assert resp["id"] == 11
    assert resp["name"] == valid_data["name"]
    assert resp["phone"] == valid_data["phone"]
    assert resp["email"] == valid_data["email"]
    assert resp["username"] == valid_data["username"]

def test_invalid_creation():
    response = client.post("/users/", json=invalid_data)
    assert response.status_code == 422
    resp = response.json()
    assert len(resp.keys()) == 1