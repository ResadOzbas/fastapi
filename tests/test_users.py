from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.main import app
from app import schema
from app.config import settings

# creating a test database
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}_test"
)


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# override the get_db dependency with the override_get_db function
app.dependency_overrides[get_db] = override_get_db

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
    assert newUser.email == "hello123@gmail.com"
    assert response.status_code == 201
