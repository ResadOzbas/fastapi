from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    print(response.json().get("message"))
    assert response.json().get("message") == "Welcome to my API!?"
    assert response.status_code == 200
