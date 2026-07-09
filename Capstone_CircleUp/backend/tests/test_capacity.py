"""
Tests — SRS section 7: Capacity Logic.

Covers:
  - Activity auto-transitions to FULL when approved count reaches max.
  - New requests rejected when FULL.
  - Approving beyond capacity is rejected (sequential test).
  - Concurrent approvals never exceed capacity (threading test).
"""
import threading
import tempfile
import os
from datetime import datetime, timedelta

from tests.conftest import register_and_login, make_activity_payload


def test_activity_becomes_full_at_capacity(client):
    owner_h, _ = register_and_login(client, email="full1_own@example.com")
    req_h, _ = register_and_login(client, email="full1_req@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(max_participants=1), headers=owner_h).json()["id"]
    rid = client.post(f"/api/activities/{aid}/requests", headers=req_h).json()["id"]
    client.post(f"/api/activities/{aid}/requests/{rid}/approve", headers=owner_h)
    detail = client.get(f"/api/activities/{aid}", headers=owner_h).json()
    assert detail["status"] == "full"
    assert detail["approved_participants_count"] == 1


def test_new_request_rejected_when_full(client):
    owner_h, _ = register_and_login(client, email="full2_own@example.com")
    req1_h, _ = register_and_login(client, email="full2_r1@example.com")
    req2_h, _ = register_and_login(client, email="full2_r2@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(max_participants=1), headers=owner_h).json()["id"]
    rid1 = client.post(f"/api/activities/{aid}/requests", headers=req1_h).json()["id"]
    client.post(f"/api/activities/{aid}/requests/{rid1}/approve", headers=owner_h)
    assert client.post(f"/api/activities/{aid}/requests", headers=req2_h).status_code == 400


def test_approve_beyond_capacity_is_rejected(client):
    """Sequential: first approval succeeds, second must be rejected."""
    owner_h, _ = register_and_login(client, email="cap_own@example.com")
    r1_h, _ = register_and_login(client, email="cap_r1@example.com")
    r2_h, _ = register_and_login(client, email="cap_r2@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(max_participants=1), headers=owner_h).json()["id"]
    rid1 = client.post(f"/api/activities/{aid}/requests", headers=r1_h).json()["id"]
    rid2 = client.post(f"/api/activities/{aid}/requests", headers=r2_h).json()["id"]
    assert client.post(f"/api/activities/{aid}/requests/{rid1}/approve", headers=owner_h).status_code == 200
    assert client.post(f"/api/activities/{aid}/requests/{rid2}/approve", headers=owner_h).status_code == 400
    assert client.get(f"/api/activities/{aid}", headers=owner_h).json()["approved_participants_count"] == 1


def test_approved_count_excludes_rejected(client):
    owner_h, _ = register_and_login(client, email="cnt_own@example.com")
    r1_h, _ = register_and_login(client, email="cnt_r1@example.com")
    r2_h, _ = register_and_login(client, email="cnt_r2@example.com")
    r3_h, _ = register_and_login(client, email="cnt_r3@example.com")
    aid = client.post("/api/activities", json=make_activity_payload(max_participants=3), headers=owner_h).json()["id"]
    rid1 = client.post(f"/api/activities/{aid}/requests", headers=r1_h).json()["id"]
    rid2 = client.post(f"/api/activities/{aid}/requests", headers=r2_h).json()["id"]
    rid3 = client.post(f"/api/activities/{aid}/requests", headers=r3_h).json()["id"]
    client.post(f"/api/activities/{aid}/requests/{rid1}/approve", headers=owner_h)
    client.post(f"/api/activities/{aid}/requests/{rid2}/reject", headers=owner_h)
    client.post(f"/api/activities/{aid}/requests/{rid3}/approve", headers=owner_h)
    detail = client.get(f"/api/activities/{aid}", headers=owner_h).json()
    assert detail["approved_participants_count"] == 2
    assert detail["status"] == "open"   # max=3, approved=2


def test_concurrent_approvals_never_exceed_capacity():
    """
    SRS 7: "This must hold even if two approvals are attempted around the
    same time — the system should never end up over capacity."

    Calls approve_participation_request directly from two threads, bypassing
    the API layer (per the SRS concurrency test note). Uses a file-based
    SQLite DB so each thread gets an independent connection and writes
    serialize correctly. In production PostgreSQL, SELECT FOR UPDATE
    provides the same guarantee.
    """
    from sqlalchemy import create_engine as _ce
    from sqlalchemy.orm import sessionmaker as _sm
    from app.database import Base
    from app.models.user import User as UModel
    from app.models.activity import Activity, ActivityStatus
    from app.models.participation import ParticipationRequest, ParticipationStatus
    from app.core.security import hash_password
    from app.services.participation_service import approve_participation_request
    from fastapi import HTTPException

    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        engine = _ce(
            f"sqlite:///{db_path}",
            connect_args={"check_same_thread": False, "timeout": 15},
        )
        Base.metadata.create_all(bind=engine)
        SL = _sm(autocommit=False, autoflush=False, bind=engine)

        # --- Set up: 1 owner, 2 requesters, activity with max=1 ---
        db = SL()
        owner = UModel(name="Owner", email="own@cct.com",
                       password_hash=hash_password("pass1234"), phone_number="1111111111")
        u1 = UModel(name="User1", email="u1@cct.com",
                    password_hash=hash_password("pass1234"), phone_number="2222222222")
        u2 = UModel(name="User2", email="u2@cct.com",
                    password_hash=hash_password("pass1234"), phone_number="3333333333")
        db.add_all([owner, u1, u2])
        db.commit()

        future = datetime.now() + timedelta(days=2)
        activity = Activity(
            creator_id=owner.id, title="Concurrency Test",
            category="Test", location="Here",
            date=future.date(), time=future.time(),
            max_participants=1, status=ActivityStatus.OPEN,
        )
        db.add(activity)
        db.commit()

        r1 = ParticipationRequest(activity_id=activity.id, user_id=u1.id,
                                   status=ParticipationStatus.PENDING)
        r2 = ParticipationRequest(activity_id=activity.id, user_id=u2.id,
                                   status=ParticipationStatus.PENDING)
        db.add_all([r1, r2])
        db.commit()
        owner_id, act_id, r1_id, r2_id = owner.id, activity.id, r1.id, r2.id
        db.close()

        # --- Two threads both try to approve ---
        results = []
        lock = threading.Lock()

        def try_approve(req_id):
            thread_db = SL()
            try:
                fresh_owner = thread_db.query(UModel).filter(UModel.id == owner_id).first()
                req = approve_participation_request(thread_db, act_id, req_id, fresh_owner)
                with lock:
                    results.append(("ok", req.status.value))
            except HTTPException as e:
                with lock:
                    results.append(("err", e.status_code))
            except Exception as ex:
                with lock:
                    results.append(("ex", str(ex)))
            finally:
                thread_db.close()

        t1 = threading.Thread(target=try_approve, args=(r1_id,))
        t2 = threading.Thread(target=try_approve, args=(r2_id,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        ok_count = sum(1 for r in results if r[0] == "ok")
        err_count = sum(1 for r in results if r[0] == "err")
        assert ok_count == 1, f"Expected exactly 1 approval. Got: {results}"
        assert err_count == 1, f"Expected exactly 1 failure. Got: {results}"

    finally:
        try:
            os.unlink(db_path)
        except OSError:
            pass