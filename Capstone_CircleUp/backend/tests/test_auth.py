
from tests.conftest import make_user_payload, register_and_login


def test_register_creates_user_and_hides_password(client):
    resp = client.post("/api/auth/register", json=make_user_payload())
    assert resp.status_code == 201
    body = resp.json()
    assert body["email"] == make_user_payload()["email"]
    assert "password" not in body
    assert "password_hash" not in body


def test_password_is_hashed_not_stored_in_plaintext(client):
    from tests.conftest import TestingSessionLocal
    from app.models.user import User

    payload = make_user_payload(email="hash_check@example.com")
    client.post("/api/auth/register", json=payload)

    db = TestingSessionLocal()
    try:
        user = db.query(User).filter(User.email == payload["email"]).first()
        assert user is not None
        assert user.password_hash != payload["password"]
        assert user.password_hash.startswith("$2b$")   # bcrypt prefix
    finally:
        db.close()


def test_register_rejects_duplicate_email(client):
    client.post("/api/auth/register", json=make_user_payload(email="dup@example.com"))
    resp = client.post("/api/auth/register", json=make_user_payload(email="dup@example.com"))
    assert resp.status_code == 400


def test_register_rejects_short_password(client):
    resp = client.post("/api/auth/register", json=make_user_payload(password="short"))
    assert resp.status_code == 422


def test_login_returns_token(client):
    _h, payload = register_and_login(client, email="login_ok@example.com")
    resp = client.post("/api/auth/login", json={"email": payload["email"], "password": payload["password"]})
    assert resp.status_code == 200
    assert "access_token" in resp.json()
    assert resp.json()["token_type"] == "bearer"


def test_login_rejects_wrong_password(client):
    payload = make_user_payload(email="wp@example.com")
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/login", json={"email": payload["email"], "password": "WrongPass999"})
    assert resp.status_code == 401


def test_login_rejects_unknown_email(client):
    resp = client.post("/api/auth/login", json={"email": "ghost@example.com", "password": "whatever123"})
    assert resp.status_code == 401


def test_protected_endpoint_without_token_returns_401(client):
    assert client.get("/api/users/me").status_code == 401


def test_protected_endpoint_with_garbage_token_returns_401(client):
    resp = client.get("/api/users/me", headers={"Authorization": "Bearer garbage"})
    assert resp.status_code == 401


def test_protected_endpoint_with_valid_token_succeeds(client):
    headers, payload = register_and_login(client, email="ok@example.com")
    resp = client.get("/api/users/me", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == payload["email"]


def test_logout_invalidates_token(client):
    headers, _ = register_and_login(client, email="logout@example.com")
    assert client.get("/api/users/me", headers=headers).status_code == 200
    assert client.post("/api/auth/logout", headers=headers).status_code == 200
    assert client.get("/api/users/me", headers=headers).status_code == 401


def test_logout_without_token_returns_401(client):
    assert client.post("/api/auth/logout").status_code == 401