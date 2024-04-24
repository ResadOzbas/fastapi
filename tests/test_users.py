import pytest
from jose import jwt
from app import schema
from app.config import settings


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
    login_res = schema.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    id = payload.get("user_id")

    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert response.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('resad.ozbas@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post(
        "/login", data={"username": email, "password": password})
    assert response.status_code == status_code
    # assert response.json().get("detail") == "invalid credentials"
