from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

@pytest.fixture
def valid_data():
    valid_d = {
        "userId": 1,
        "title": "string",
        "body": "string"
    }
    return valid_d

@pytest.fixture
def invalid_data():
    data = {
    "userId": "sds",
    "title": 12,
    "body": "string"
    }
    return data

@pytest.fixture
def post():
    post = {
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto",
        "author": {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz",
        "phone": "1-770-736-8031 x56442"
        }
    }
    return post

def test_post_list(post):
    response = client.get("/posts")
    assert response.status_code == 200
    resp = response.json()[0]
    assert resp["id"] == post['id']
    assert resp["author"] == post['author']
    assert resp["title"] == post['title']

def test_create_post(valid_data):
    response = client.post("/posts/", json=valid_data)
    assert response.status_code == 201
    resp = response.json()
    assert resp["title"] == valid_data['title']

def test_invalid_creation_post(invalid_data):
    response = client.post("/posts/", json=invalid_data)
    assert response.status_code == 422
    resp = response.json()
    assert "author" not in resp

def test_get_detail_post(post):
    response = client.get("/posts/1")
    assert response.status_code == 200
    resp = response.json()
    assert resp["id"] == post['id']
    assert resp["author"] == post['author']
    assert resp["title"] == post['title']

def test_update_post():
    data = {"title": "string", "body": "string"}
    response = client.put("/posts/3", json=data)
    assert response.status_code == 200
    resp = response.json()
    for key in data.keys():
        assert data[key] == resp[key]
