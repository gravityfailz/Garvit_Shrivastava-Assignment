
from tests.conftest import register_and_login, make_activity_payload


def _create_and_request(client, owner_h, req_h, extra=None):
    """Create an activity as owner, submit a request as requester."""
    payload = make_activity_payload(**(extra or {}))
    aid = client.post("/api/activities", json=payload, headers=owner_h).json()["id"]
    rid = client.post(f"/api/activities/{aid}/requests", headers=req_h).json()["id"]
    return aid, rid


# ---- Create request ----

def test_request_to_join_success(client):
    owner_h, _ = register_and_login(client, email="rj_own@example.com")
    req_h, _ = register_and_login(client, email="rj_req@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner_h).json()["id"]
    resp = client.post(f"/api/activities/{aid}/requests", headers=req_h)
    assert resp.status_code == 201
    assert resp.json()["status"] == "pending"


def test_request_requires_auth(client):
    owner_h, _ = register_and_login(client, email="ra_own@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner_h).json()["id"]
    assert client.post(f"/api/activities/{aid}/requests").status_code == 401


def test_cannot_request_own_activity(client):
    owner_h, _ = register_and_login(client, email="own_own@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner_h).json()["id"]
    assert client.post(f"/api/activities/{aid}/requests", headers=owner_h).status_code == 400


def test_duplicate_request_rejected(client):
    owner_h, _ = register_and_login(client, email="dup_own@example.com")
    req_h, _ = register_and_login(client, email="dup_req@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner_h).json()["id"]
    assert client.post(f"/api/activities/{aid}/requests", headers=req_h).status_code == 201
    assert client.post(f"/api/activities/{aid}/requests", headers=req_h).status_code == 400


def test_cannot_request_cancelled_activity(client):
    owner_h, _ = register_and_login(client, email="can_own@example.com")
    req_h, _ = register_and_login(client, email="can_req@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(), headers=owner_h).json()["id"]
    client.post(f"/api/activities/{aid}/cancel", headers=owner_h)
    assert client.post(f"/api/activities/{aid}/requests", headers=req_h).status_code == 400


def test_request_nonexistent_activity_returns_404(client):
    req_h, _ = register_and_login(client, email="r404@example.com")
    assert client.post("/api/activities/999999/requests", headers=req_h).status_code == 404


# ---- Approve ----

def test_owner_can_approve(client):
    owner_h, _ = register_and_login(client, email="ap_own@example.com")
    req_h, _ = register_and_login(client, email="ap_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    resp = client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    assert resp.status_code == 200
    assert resp.json()["status"] == "approved"


def test_non_owner_cannot_approve(client):
    owner_h, _ = register_and_login(client, email="nap_own@example.com")
    req_h, _ = register_and_login(client, email="nap_req@example.com")
    other_h, _ = register_and_login(client, email="nap_oth@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    assert client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=other_h).status_code == 403


def test_approve_requires_auth(client):
    owner_h, _ = register_and_login(client, email="aauth_own@example.com")
    req_h, _ = register_and_login(client, email="aauth_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    assert client.post(f"/api/activities/{aid}/requests/{rid}/approve").status_code == 401


def test_cannot_approve_already_approved(client):
    owner_h, _ = register_and_login(client, email="dap_own@example.com")
    req_h, _ = register_and_login(client, email="dap_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    assert client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h).status_code == 400


# ---- Reject ----

def test_owner_can_reject(client):
    owner_h, _ = register_and_login(client, email="rj2_own@example.com")
    req_h, _ = register_and_login(client, email="rj2_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    resp = client.post(f"/api/activities/{aid}/requests/{rid}/reject", headers=owner_h)
    assert resp.status_code == 200
    assert resp.json()["status"] == "rejected"


def test_non_owner_cannot_reject(client):
    owner_h, _ = register_and_login(client, email="nrj_own@example.com")
    req_h, _ = register_and_login(client, email="nrj_req@example.com")
    other_h, _ = register_and_login(client, email="nrj_oth@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    assert client.post(f"/api/activities/{aid}/requests/{rid}/reject", headers=other_h).status_code == 403


def test_cannot_reject_already_rejected(client):
    owner_h, _ = register_and_login(client, email="drj_own@example.com")
    req_h, _ = register_and_login(client, email="drj_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    client.post(f"/api/activities/{aid}/requests/{rid}/reject", headers=owner_h)
    assert client.post(f"/api/activities/{aid}/requests/{rid}/reject", headers=owner_h).status_code == 400


# ---- Contact info visibility ----

def test_organizer_phone_hidden_before_approval(client):
    owner_h, _ = register_and_login(client, email="ci1_own@example.com")
    req_h, _ = register_and_login(client, email="ci1_req@example.com")
    aid, _ = _create_and_request(client, owner_h, req_h)
    detail = client.get(f"/api/activities/{aid}", headers=req_h).json()
    assert detail["organizer_phone"] is None
    assert detail["my_request_status"] == "pending"


def test_organizer_phone_visible_after_approval(client):
    owner_h, owner_p = register_and_login(client, email="ci2_own@example.com")
    req_h, _ = register_and_login(client, email="ci2_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    detail = client.get(f"/api/activities/{aid}", headers=req_h).json()
    assert detail["organizer_phone"] == owner_p["phone_number"]
    assert detail["my_request_status"] == "approved"


def test_organizer_phone_hidden_after_rejection(client):
    owner_h, _ = register_and_login(client, email="ci3_own@example.com")
    req_h, _ = register_and_login(client, email="ci3_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    client.post(f"/api/activities/{aid}/requests/{rid}/reject", headers=owner_h)
    detail = client.get(f"/api/activities/{aid}", headers=req_h).json()
    assert detail["organizer_phone"] is None


def test_owner_sees_approved_participant_phone(client):
    owner_h, _ = register_and_login(client, email="ci4_own@example.com")
    req_h, req_p = register_and_login(client, email="ci4_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    # Before: phone hidden
    reqs = client.get(f"/api/activities/{aid}/requests", headers=owner_h).json()
    assert next(r for r in reqs if r["id"] == rid)["requester_phone"] is None
    # After approve: phone visible
    client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    reqs = client.get(f"/api/activities/{aid}/requests", headers=owner_h).json()
    assert next(r for r in reqs if r["id"] == rid)["requester_phone"] == req_p["phone_number"]


def test_owner_cannot_see_pending_participant_phone(client):
    owner_h, _ = register_and_login(client, email="ci5_own@example.com")
    req_h, _ = register_and_login(client, email="ci5_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    reqs = client.get(f"/api/activities/{aid}/requests", headers=owner_h).json()
    assert next(r for r in reqs if r["id"] == rid)["requester_phone"] is None


def test_non_owner_cannot_list_requests(client):
    owner_h, _ = register_and_login(client, email="ci6_own@example.com")
    req_h, _ = register_and_login(client, email="ci6_req@example.com")
    aid, _ = _create_and_request(client, owner_h, req_h)
    assert client.get(f"/api/activities/{aid}/requests", headers=req_h).status_code == 403


# ---- My Activities  ----

def test_my_created_activities_returns_only_mine(client):
    own_h, _ = register_and_login(client, email="myc1@example.com")
    oth_h, _ = register_and_login(client, email="myc2@example.com")
    client.post("/api/activities", json=make_activity_payload(title="Mine"), headers=own_h)
    client.post("/api/activities", json=make_activity_payload(title="Theirs"), headers=oth_h)
    mine = client.get("/api/users/me/activities", headers=own_h).json()
    assert len(mine) == 1
    assert mine[0]["title"] == "Mine"


def test_my_joined_activities_after_approval(client):
    owner_h, _ = register_and_login(client, email="myj_own@example.com")
    req_h, _ = register_and_login(client, email="myj_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    assert client.get("/api/users/me/joined", headers=req_h).json() == []
    client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    joined = client.get("/api/users/me/joined", headers=req_h).json()
    assert len(joined) == 1 and joined[0]["id"] == aid


def test_my_requests_shows_all_statuses(client):
    owner_h, _ = register_and_login(client, email="myr_own@example.com")
    req_h, _ = register_and_login(client, email="myr_req@example.com")
    aid1, rid1 = _create_and_request(client, owner_h, req_h, {"title": "Act1"})
    aid2, rid2 = _create_and_request(client, owner_h, req_h, {"title": "Act2", "max_participants": 5})
    client.post(f"/api/activities/{aid1}/requests/{rid1}/approve", headers=owner_h)
    client.post(f"/api/activities/{aid2}/requests/{rid2}/reject", headers=owner_h)
    statuses = {r["status"] for r in client.get("/api/users/me/requests", headers=req_h).json()}
    assert "approved" in statuses
    assert "rejected" in statuses


def test_my_requests_organizer_phone_only_when_approved(client):
    owner_h, owner_p = register_and_login(client, email="myp_own@example.com")
    req_h, _ = register_and_login(client, email="myp_req@example.com")
    aid, rid = _create_and_request(client, owner_h, req_h)
    before = client.get("/api/users/me/requests", headers=req_h).json()
    assert before[0]["organizer_phone"] is None
    client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    after = client.get("/api/users/me/requests", headers=req_h).json()
    approved = next(r for r in after if r["id"] == rid)
    assert approved["organizer_phone"] == owner_p["phone_number"]
    