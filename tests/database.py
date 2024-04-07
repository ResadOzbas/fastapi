from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.main import app
from app.config import settings
from app.database import Base


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


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
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
