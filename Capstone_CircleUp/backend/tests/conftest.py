
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app import models  # noqa: F401

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture(autouse=True)
def fresh_schema():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


# ---------- Helpers ----------

DEFAULT_PASSWORD = "StrongPass123"


def make_user_payload(**overrides):
    payload = {
        "name": "Asha Verma",
        "email": "asha@example.com",
        "password": DEFAULT_PASSWORD,
        "phone_number": "9876500001",
        "city": "Pune",
        "bio": "Loves badminton.",
    }
    payload.update(overrides)
    return payload


def register_and_login(client, **overrides) -> tuple[dict, dict]:
    """Registers + logs in a user. Returns (auth_headers, payload)."""
    payload = make_user_payload(**overrides)
    reg = client.post("/api/auth/register", json=payload)
    assert reg.status_code == 201, reg.text
    login = client.post("/api/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert login.status_code == 200, login.text
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}, payload


def make_activity_payload(**overrides):
    from datetime import datetime, timedelta
    future = datetime.now() + timedelta(days=3)
    payload = {
        "title": "Sunday Badminton Session",
        "description": "Casual doubles, all levels welcome.",
        "category": "Badminton Session",
        "location": "Green Park Courts, Pune",
        "date": future.date().isoformat(),
        "time": "18:00:00",
        "max_participants": 4,
    }
    payload.update(overrides)
    return payload