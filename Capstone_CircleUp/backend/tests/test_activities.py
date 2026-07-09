"""
Tests — SRS section 4: Activity validation + ownership.
  - max_participants > 0
  - date/time must be in the future
  - Only the creator may edit/cancel
  - Unauthenticated users are blocked
"""
from datetime import datetime, timedelta
from tests.conftest import register_and_login, make_activity_payload


def test_create_activity_requires_auth(client):
    assert client.post("/api/activities", json=make_activity_payload()).status_code == 401


def test_create_activity_success(client):
    headers, _ = register_and_login(client, email="c1@example.com")
    resp = client.post("/api/activities", json=make_activity_payload(title="Cricket Match"), headers=headers)
    assert resp.status_code == 201
    assert resp.json()["status"] == "open"
    assert resp.json()["approved_participants_count"] == 0


def test_create_rejects_zero_max_participants(client):
    headers, _ = register_and_login(client, email="c2@example.com")
    assert client.post("/api/activities", json=make_activity_payload(max_participants=0), headers=headers).status_code == 422


def test_create_rejects_negative_max_participants(client):
    headers, _ = register_and_login(client, email="c3@example.com")
    assert client.post("/api/activities", json=make_activity_payload(max_participants=-1), headers=headers).status_code == 422


def test_create_rejects_past_date(client):
    headers, _ = register_and_login(client, email="c4@example.com")
    past = (datetime.now() - timedelta(days=1)).date().isoformat()
    assert client.post("/api/activities", json=make_activity_payload(date=past, time="10:00:00"), headers=headers).status_code == 422


def test_create_rejects_past_time_today(client):
    headers, _ = register_and_login(client, email="c5@example.com")
    past = datetime.now() - timedelta(minutes=10)
    resp = client.post("/api/activities", json=make_activity_payload(
        date=past.date().isoformat(), time=past.time().isoformat()
    ), headers=headers)
    assert resp.status_code == 422


def test_get_activity_requires_auth(client):
    headers, _ = register_and_login(client, email="c6@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    assert client.get(f"/api/activities/{aid}").status_code == 401


def test_get_activity_success(client):
    headers, _ = register_and_login(client, email="c7@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    assert client.get(f"/api/activities/{aid}", headers=headers).status_code == 200


def test_get_nonexistent_returns_404(client):
    headers, _ = register_and_login(client, email="c8@example.com")
    assert client.get("/api/activities/999999", headers=headers).status_code == 404


def test_list_activities_requires_auth(client):
    assert client.get("/api/activities").status_code == 401


def test_list_includes_created_activity(client):
    headers, _ = register_and_login(client, email="c9@example.com")
    client.post("/api/activities", json=make_activity_payload(title="Weekend Trip"), headers=headers)
    titles = [a["title"] for a in client.get("/api/activities", headers=headers).json()]
    assert "Weekend Trip" in titles


# ---- Edit ----

def test_owner_can_edit(client):
    headers, _ = register_and_login(client, email="o1@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    resp = client.put(f"/api/activities/{aid}", json={"title": "Updated", "max_participants": 8}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated"


def test_non_owner_cannot_edit(client):
    owner, _ = register_and_login(client, email="o2@example.com")
    other, _ = register_and_login(client, email="i1@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner).json()["id"]
    assert client.put(f"/api/activities/{aid}", json={"title": "Hijacked"}, headers=other).status_code == 403


def test_edit_requires_auth(client):
    headers, _ = register_and_login(client, email="o3@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    assert client.put(f"/api/activities/{aid}", json={"title": "No Auth"}).status_code == 401


def test_edit_nonexistent_returns_404(client):
    headers, _ = register_and_login(client, email="o4@example.com")
    assert client.put("/api/activities/999999", json={"title": "Ghost"}, headers=headers).status_code == 404


def test_edit_rejects_past_resulting_datetime(client):
    headers, _ = register_and_login(client, email="o5@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    past = (datetime.now() - timedelta(days=2)).date().isoformat()
    assert client.put(f"/api/activities/{aid}", json={"date": past}, headers=headers).status_code == 400


def test_edit_rejects_zero_max_participants(client):
    headers, _ = register_and_login(client, email="o6@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    assert client.put(f"/api/activities/{aid}", json={"max_participants": 0}, headers=headers).status_code == 422


# ---- Cancel ----

def test_owner_can_cancel(client):
    headers, _ = register_and_login(client, email="o7@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    resp = client.post(f"/api/activities/{aid}/cancel", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "cancelled"


def test_non_owner_cannot_cancel(client):
    owner, _ = register_and_login(client, email="o8@example.com")
    other, _ = register_and_login(client, email="i2@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner).json()["id"]
    assert client.post(f"/api/activities/{aid}/cancel", headers=other).status_code == 403
    assert client.get(f"/api/activities/{aid}", headers=owner).json()["status"] == "open"


def test_cancel_requires_auth(client):
    headers, _ = register_and_login(client, email="o9@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    assert client.post(f"/api/activities/{aid}/cancel").status_code == 401


def test_cancel_nonexistent_returns_404(client):
    headers, _ = register_and_login(client, email="o10@example.com")
    assert client.post("/api/activities/999999/cancel", headers=headers).status_code == 404


def test_cannot_cancel_already_cancelled(client):
    headers, _ = register_and_login(client, email="o11@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    client.post(f"/api/activities/{aid}/cancel", headers=headers)
    assert client.post(f"/api/activities/{aid}/cancel", headers=headers).status_code == 400


def test_cannot_edit_cancelled_activity(client):
    headers, _ = register_and_login(client, email="o12@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    client.post(f"/api/activities/{aid}/cancel", headers=headers)
    assert client.put(f"/api/activities/{aid}", json={"title": "Edit after cancel"}, headers=headers).status_code == 400