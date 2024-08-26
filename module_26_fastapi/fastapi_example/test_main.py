import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .main import app, Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Фикстура для создания новой базы данных перед каждым тестом."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """Фикстура для создания нового клиента с тестовой базой данных."""

    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_create_user(client):
    response = client.post("/users/", json={"name": "John Doe", "email": "john.doe@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"
    assert "id" in data


def test_read_user(client):
    # Сначала создаем пользователя
    client.post("/users/", json={"name": "John Doe", "email": "john.doe@example.com"})

    # Затем получаем пользователя по его id
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == "john.doe@example.com"


def test_read_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
