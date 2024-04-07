import pytest
from app import schema
from .database import client, session


@pytest.fixture()
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


# def test_root(client):
#     # Send a GET request to the root endpoint
#     response = client.get("/")
#     # Print the message from the response JSON
#     print(response.json().get("message"))
#     # Assert that the message is "Welcome to my API!?"
#     assert response.json().get("message") == "Welcome to my API!?"
#     assert response.status_code == 200


def test_create_user(client):
    # Send a POST request to the "/users/" endpoint with JSON data
    response = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"})
    # Create a UserOut object from the response JSON
    newUser = schema.UserOut(**response.json())
    # Assert that the email of the new user is "hello123@gmail.com"
    assert newUser.email == "hello123@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})

    assert response.status_code == 200
