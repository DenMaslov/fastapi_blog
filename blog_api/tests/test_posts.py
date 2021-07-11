from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

valid_data = {
  "userId": 1,
  "title": "string",
  "body": "string"
}

invalid_data = {
  "userId": "sds",
  "title": 12,
  "body": "string"
}


def test_post_list():
    response = client.get("/posts")
    assert response.status_code == 200
    resp = response.json()[0]
    assert resp["author"]["id"]
    assert resp["author"]["name"]
    assert resp["author"]["phone"]
    assert resp["author"]["email"]
    assert resp["author"]["username"]

def test_create_post():
    response = client.post("/posts/", json=valid_data)
    assert response.status_code == 201
    resp = response.json()
    assert resp["author"]["id"]
    assert resp["author"]["name"]
    assert resp["author"]["phone"]
    assert resp["author"]["email"]
    assert resp["author"]["username"]

def test_invalid_creation_post():
    response = client.post("/posts/", json=invalid_data)
    assert response.status_code == 422
    resp = response.json()
    assert "author" not in resp

def test_get_detail_post():
    response = client.get("/posts/3")
    assert response.status_code == 200
    resp = response.json()
    assert resp["author"]["id"]
    assert resp["comments"]

def test_update_post():
    data = {"title": "string", "body": "string"}
    response = client.put("/posts/3", json=data)
    assert response.status_code == 200
    resp = response.json()
    for key in data.keys():
        assert data[key] == resp[key]
