from fastapi.testclient import TestClient
from app.main import app
from app import schema

client = TestClient(app)


def test_root():
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "Welcome to my API!?"
    assert response.status_code == 200


def test_create_user():
    response = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    newUser = schema.UserOut(**response.json())
    assert response.json().get("email") == "hello123@gmail.com"
    assert response.status_code == 201
