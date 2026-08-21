
from datetime import datetime, timedelta
from tests.conftest import register_and_login, make_activity_payload, make_user_payload



def test_password_requires_uppercase(client):
    """Password without any uppercase letter must be rejected (422)."""
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_up@v.com", password="alllower1"))
    assert resp.status_code == 422


def test_password_requires_number(client):
    """Password without a digit must be rejected (422)."""
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_num@v.com", password="NoNumbers"))
    assert resp.status_code == 422


def test_password_7_chars_rejected(client):
    """7-character password (even with uppercase + number) must be rejected."""
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_7@v.com", password="Short1A"))
    assert resp.status_code == 422


def test_password_exactly_8_chars_accepted(client):
    """Exactly 8 chars meeting all rules must be accepted (boundary value)."""
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_8@v.com", password="Secure12"))
    assert resp.status_code == 201


def test_password_all_requirements_met(client):
    """Long password meeting all rules must be accepted."""
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_ok@v.com", password="ValidPass123"))
    assert resp.status_code == 201


def test_password_uppercase_only_no_number_rejected(client):
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_ucn@v.com", password="ALLUPPERCASE"))
    assert resp.status_code == 422


def test_password_number_only_no_uppercase_rejected(client):
    resp = client.post("/api/auth/register",
                       json=make_user_payload(email="pw_nup@v.com", password="alllower12345"))
    assert resp.status_code == 422


def test_password_empty_rejected(client):
    resp = client.post("/api/auth/register", json={
        "name": "Test", "email": "pw_empty@v.com",
        "password": "", "phone_number": "9876543210"
    })
    assert resp.status_code == 422



def test_email_without_at_sign_rejected(client):
    resp = client.post("/api/auth/register", json={
        "name": "Test", "email": "notanemail",
        "password": "ValidPass1", "phone_number": "9876543210"
    })
    assert resp.status_code == 422


def test_email_without_domain_rejected(client):
    resp = client.post("/api/auth/register", json={
        "name": "Test", "email": "user@",
        "password": "ValidPass1", "phone_number": "9876543210"
    })
    assert resp.status_code == 422


def test_valid_email_formats_accepted(client):
    resp = client.post("/api/auth/register", json={
        "name": "Test", "email": "test.user+tag@example.co.in",
        "password": "ValidPass1", "phone_number": "9876543210"
    })
    assert resp.status_code == 201


def test_email_uniqueness_enforced(client):
    """Duplicate email must return 400."""
    payload = make_user_payload(email="uniquecheck@v.com")
    client.post("/api/auth/register", json=payload)
    resp = client.post("/api/auth/register", json=payload)
    assert resp.status_code == 400




def test_max_participants_zero_rejected(client):
    headers, _ = register_and_login(client, email="av1@v.com")
    resp = client.post("/api/activities",
                       json=make_activity_payload(max_participants=0), headers=headers)
    assert resp.status_code == 422


def test_max_participants_negative_rejected(client):
    headers, _ = register_and_login(client, email="av2@v.com")
    resp = client.post("/api/activities",
                       json=make_activity_payload(max_participants=-3), headers=headers)
    assert resp.status_code == 422


def test_max_participants_one_is_valid_boundary(client):
    """max_participants=1 is the minimum valid value."""
    headers, _ = register_and_login(client, email="av3@v.com")
    resp = client.post("/api/activities",
                       json=make_activity_payload(max_participants=1), headers=headers)
    assert resp.status_code == 201


def test_past_date_rejected(client):
    headers, _ = register_and_login(client, email="av4@v.com")
    past = (datetime.now() - timedelta(days=1)).date().isoformat()
    resp = client.post("/api/activities",
                       json=make_activity_payload(date=past, time="10:00:00"), headers=headers)
    assert resp.status_code == 422


def test_edit_max_participants_to_zero_rejected(client):
    headers, _ = register_and_login(client, email="av5@v.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=headers).json()["id"]
    resp = client.put(f"/api/activities/{aid}", json={"max_participants": 0}, headers=headers)
    assert resp.status_code == 422




def test_cannot_request_completed_activity(client):
    """Activities past their scheduled date/time must reject new join requests."""
    from tests.conftest import TestingSessionLocal
    from app.models.activity import Activity, ActivityStatus

    owner_h, _ = register_and_login(client, email="comp1@v.com")
    req_h, _   = register_and_login(client, email="comp2@v.com")
    owner_id = client.get("/api/users/me", headers=owner_h).json()["id"]

    db = TestingSessionLocal()
    past = datetime.now() - timedelta(days=1)
    act = Activity(
        creator_id=owner_id, title="Past Activity",
        category="Test", location="Somewhere",
        date=past.date(), time=past.time(),
        max_participants=5, status=ActivityStatus.OPEN,
    )
    db.add(act)
    db.commit()
    aid = act.id
    db.close()

    resp = client.post(f"/api/activities/{aid}/requests", headers=req_h)
    assert resp.status_code == 400


def test_completed_activity_returns_correct_status(client):
    """Past activity must return status='completed' even though DB stores 'open'."""
    from tests.conftest import TestingSessionLocal
    from app.models.activity import Activity, ActivityStatus

    headers, _ = register_and_login(client, email="comp3@v.com")
    uid = client.get("/api/users/me", headers=headers).json()["id"]

    db = TestingSessionLocal()
    past = datetime.now() - timedelta(days=2)
    act = Activity(
        creator_id=uid, title="Completed Activity",
        category="Test", location="Somewhere",
        date=past.date(), time=past.time(),
        max_participants=5, status=ActivityStatus.OPEN,
    )
    db.add(act)
    db.commit()
    aid = act.id
    db.close()

    resp = client.get(f"/api/activities/{aid}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
    