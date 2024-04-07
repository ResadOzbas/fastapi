from app import schema
from .database import client, session


def test_root(client):
    # Send a GET request to the root endpoint
    response = client.get("/")
    # Print the message from the response JSON
    print(response.json().get("message"))
    # Assert that the message is "Welcome to my API!?"
    assert response.json().get("message") == "Welcome to my API!?"
    assert response.status_code == 200


def test_create_user(client):
    # Send a POST request to the "/users/" endpoint with JSON data
    response = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    # Create a UserOut object from the response JSON
    newUser = schema.UserOut(**response.json())
    # Assert that the email of the new user is "hello123@gmail.com"
    assert newUser.email == "hello123@gmail.com"
    assert response.status_code == 201


def test_login_user(client):
    response = client.post(
        "/login", data={"username": "hello123@gmail.com", "password": "password123"})

    assert response.status_code == 200
