
from datetime import datetime, timedelta

from tests.conftest import register_and_login


def _make(client, headers, title, category, location, days, time="18:00:00", max_p=4):
    future = (datetime.now() + timedelta(days=days)).date().isoformat()
    resp = client.post("/api/activities", headers=headers, json={
        "title": title, "category": category, "location": location,
        "date": future, "time": time, "max_participants": max_p,
        "description": "Test activity",
    })
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def test_no_filters_returns_all(client):
    h, _ = register_and_login(client, email="flt_all@example.com")
    _make(client, h, "A1", "Cricket Match", "Mumbai", 3)
    _make(client, h, "A2", "Cafe Meetup", "Delhi", 4)
    resp = client.get("/api/activities", headers=h)
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_filter_by_category_exact(client):
    h, _ = register_and_login(client, email="flt_cat@example.com")
    _make(client, h, "Cricket Game", "Cricket Match", "Mumbai", 3)
    _make(client, h, "Badminton Fun", "Badminton Session", "Delhi", 4)
    resp = client.get("/api/activities?category=Cricket+Match", headers=h)
    results = resp.json()
    assert len(results) == 1
    assert results[0]["category"] == "Cricket Match"


def test_filter_by_category_partial(client):
    h, _ = register_and_login(client, email="flt_catp@example.com")
    _make(client, h, "Game1", "Cricket Match", "Pune", 3)
    _make(client, h, "Game2", "Cafe Meetup", "Pune", 4)
    resp = client.get("/api/activities?category=Cricket", headers=h)
    results = resp.json()
    assert len(results) == 1
    assert "Cricket" in results[0]["category"]


def test_filter_by_location_partial(client):
    h, _ = register_and_login(client, email="flt_loc@example.com")
    _make(client, h, "Mumbai Activity", "Cricket Match", "Andheri, Mumbai", 3)
    _make(client, h, "Delhi Activity", "Cafe Meetup", "Connaught Place, Delhi", 4)
    resp = client.get("/api/activities?location=Mumbai", headers=h)
    results = resp.json()
    assert len(results) == 1
    assert "Mumbai" in results[0]["location"]


def test_filter_by_exact_date(client):
    h, _ = register_and_login(client, email="flt_date@example.com")
    target = (datetime.now() + timedelta(days=5)).date()
    other  = (datetime.now() + timedelta(days=8)).date()
    _make(client, h, "Target Day", "Cricket Match", "Pune", 5)
    _make(client, h, "Other Day", "Cafe Meetup", "Delhi", 8)
    resp = client.get(f"/api/activities?date={target.isoformat()}", headers=h)
    results = resp.json()
    assert len(results) == 1
    assert results[0]["date"] == target.isoformat()


def test_filter_date_returns_empty_when_no_match(client):
    h, _ = register_and_login(client, email="flt_nodate@example.com")
    _make(client, h, "Some Activity", "Cricket Match", "Pune", 3)
    far_future = (datetime.now() + timedelta(days=365)).date().isoformat()
    resp = client.get(f"/api/activities?date={far_future}", headers=h)
    assert resp.json() == []


def test_sort_by_date_ascending(client):
    h, _ = register_and_login(client, email="flt_asc@example.com")
    _make(client, h, "Far Future",  "Cricket Match", "Pune",  10)
    _make(client, h, "Near Future", "Cafe Meetup",   "Delhi",  3)
    results = client.get("/api/activities?sort_by_date=asc", headers=h).json()
    assert len(results) == 2
    assert results[0]["date"] <= results[1]["date"]


def test_sort_by_date_descending(client):
    h, _ = register_and_login(client, email="flt_desc@example.com")
    _make(client, h, "Far Future",  "Cricket Match", "Pune",  10)
    _make(client, h, "Near Future", "Cafe Meetup",   "Delhi",  3)
    results = client.get("/api/activities?sort_by_date=desc", headers=h).json()
    assert len(results) == 2
    assert results[0]["date"] >= results[1]["date"]


def test_combined_category_and_location_filter(client):
    h, _ = register_and_login(client, email="flt_comb@example.com")
    _make(client, h, "Cricket Mumbai", "Cricket Match",   "Mumbai", 3)
    _make(client, h, "Cricket Delhi",  "Cricket Match",   "Delhi",  4)
    _make(client, h, "Cafe Mumbai",    "Cafe Meetup",     "Mumbai", 5)
    resp = client.get("/api/activities?category=Cricket&location=Mumbai", headers=h)
    results = resp.json()
    assert len(results) == 1
    assert results[0]["title"] == "Cricket Mumbai"


def test_combined_category_and_date_filter(client):
    h, _ = register_and_login(client, email="flt_cdate@example.com")
    target_date = (datetime.now() + timedelta(days=5)).date()
    _make(client, h, "Cricket Day5",  "Cricket Match", "Pune",  5)
    _make(client, h, "Cricket Day10", "Cricket Match", "Pune", 10)
    _make(client, h, "Cafe Day5",     "Cafe Meetup",   "Pune",  5)
    resp = client.get(f"/api/activities?category=Cricket&date={target_date.isoformat()}", headers=h)
    results = resp.json()
    assert len(results) == 1
    assert results[0]["title"] == "Cricket Day5"