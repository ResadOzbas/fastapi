from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.main import app
from app.config import settings
from app.database import Base
from app.oath2 import createAccessToken
from app import models


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@{settings.database_hostname}:"
    f"{settings.database_port}/{settings.database_name}_test"
)

# Create a SQLAlchemy engine using the provided database URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory with specific settings
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture()
def session():
    # drop all tables then create them for testing
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        # Yield the session to be used as the dependency
        yield db
    finally:
        # Close the session after it's been used
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():

        try:
            # Yield the session to be used as the dependency
            yield session
        finally:
            # Close the session after it's been used
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user2(client):
    user_data = {"email": "hello1234@gmail.com", "password": "password123"}

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture()
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}

    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user


@pytest.fixture()
def token(test_user):
    return createAccessToken({"user_id": test_user['id']})


@pytest.fixture()
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(test_user, session, test_user2):
    post_data = [{
        "title": "first",
        "content": "first cont",
        "owner_id": test_user['id']
    }, {
        "title": "second",
        "content": "second cont",
        "owner_id": test_user['id']
    }, {
        "title": "third",
        "content": "third cont",
        "owner_id": test_user['id']
    }, {
        "title": "4",
        "content": "4th cont",
        "owner_id": test_user2['id']
    }]

    def create_post_model(posts):
        return models.Post(**posts)

    post_map = map(create_post_model, post_data)

    posts = list(post_map)
    print(posts[0].content)
    session.add_all(posts)

    session.commit()

    posts_query = session.query(models.Post).all()

    return posts_query
