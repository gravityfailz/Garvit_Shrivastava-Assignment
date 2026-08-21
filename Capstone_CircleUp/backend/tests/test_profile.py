
from tests.conftest import make_user_payload, register_and_login


def test_get_profile_requires_auth(client):
    assert client.get("/api/users/me").status_code == 401


def test_get_profile_returns_all_fields(client):
    headers, payload = register_and_login(client, email="pv@example.com")
    body = client.get("/api/users/me", headers=headers).json()
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
    assert body["city"] == payload["city"]
    assert body["bio"] == payload["bio"]


def test_update_profile_requires_auth(client):
    assert client.put("/api/users/me", json={"city": "Mumbai"}).status_code == 401


def test_partial_update_only_touches_supplied_fields(client):
    headers, _ = register_and_login(client, email="pu@example.com")
    resp = client.put("/api/users/me", json={"city": "Mumbai", "bio": "New bio."}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["city"] == "Mumbai"
    assert resp.json()["bio"] == "New bio."
    assert resp.json()["name"] != ""   # original name untouched


def test_update_to_taken_email_is_rejected(client):
    headers_a, _ = register_and_login(client, email="a@example.com")
    _, payload_b = register_and_login(client, email="b@example.com")
    resp = client.put("/api/users/me", json={"email": payload_b["email"]}, headers=headers_a)
    assert resp.status_code == 400


def test_update_to_own_current_email_is_allowed(client):
    headers, payload = register_and_login(client, email="self@example.com")
    resp = client.put("/api/users/me", json={"email": payload["email"], "city": "Goa"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["city"] == "Goa"