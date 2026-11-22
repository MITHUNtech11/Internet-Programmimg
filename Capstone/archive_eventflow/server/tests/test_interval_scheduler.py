import pytest
from fastapi.testclient import TestClient

from server.main import app
from server.services.interval_scheduler import (
    parse_time_to_minutes,
    minutes_to_time_str,
    intervals_collide,
    IntervalScheduler,
)

client = TestClient(app)


def test_time_conversions():
    assert parse_time_to_minutes("09:00 AM") == 540
    assert parse_time_to_minutes("12:00 PM") == 720
    assert parse_time_to_minutes("01:30 PM") == 810
    assert parse_time_to_minutes("12:00 AM") == 0
    assert parse_time_to_minutes("05:00 PM (Next Day)") == 1020

    assert minutes_to_time_str(540) == "09:00 AM"
    assert minutes_to_time_str(720) == "12:00 PM"
    assert minutes_to_time_str(810) == "01:30 PM"
    assert minutes_to_time_str(0) == "12:00 AM"


def test_half_open_interval_collision_math():
    # 1. Non-overlapping disjoint intervals
    assert intervals_collide(540, 660, 720, 840) is False  # [09:00, 11:00) vs [12:00, 14:00)

    # 2. Contiguous boundary neighbors (Half-open [s, e)) -> NO COLLISION
    assert intervals_collide(540, 660, 660, 780) is False  # [09:00, 11:00) vs [11:00, 13:00)
    assert intervals_collide(660, 780, 540, 660) is False

    # 3. Partial overlap -> COLLISION
    assert intervals_collide(600, 720, 660, 840) is True   # [10:00, 12:00) vs [11:00, 14:00)

    # 4. Enclosed / Nested overlap -> COLLISION
    assert intervals_collide(540, 1020, 600, 720) is True  # [09:00, 17:00) enclosing [10:00, 12:00)


def test_preflight_conflict_check_endpoint():
    # Pre-flight check on an unreserved date
    res = client.post(
        "/api/events/check-conflict",
        json={
            "venue": "Dr. APJ Abdul Kalam Auditorium",
            "date": "2026-12-25",
            "start_time": "10:00 AM",
            "end_time": "02:00 PM",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["is_collision"] is False


def test_venue_double_booking_prevention_flow():
    venue = "Seminar Hall 4"
    date = "2026-12-15"

    # 1. Book first event: 09:00 AM to 01:00 PM
    payload_1 = {
        "title": "Quantum Computing Workshop",
        "description": "Foundations of Quantum Algorithms",
        "category": "Workshop",
        "venue": venue,
        "date": date,
        "registration_deadline": date,
        "start_time": "09:00 AM",
        "end_time": "01:00 PM",
        "capacity": 60,
        "coordinator_name": "Dr. Raman",
        "coordinator_contact": "+91 98765 43210",
    }
    res1 = client.post("/api/events", json=payload_1)
    assert res1.status_code == 201
    evt1_id = res1.json()["id"]

    try:
        # 2. Book adjacent contiguous event: 01:00 PM to 04:00 PM (Should SUCCEED under half-open algebra)
        payload_adjacent = {
            "title": "Robotics Club Briefing",
            "description": "Contiguous event in same hall",
            "category": "Technical",
            "venue": venue,
            "date": date,
            "registration_deadline": date,
            "start_time": "01:00 PM",
            "end_time": "04:00 PM",
            "capacity": 60,
            "coordinator_name": "Rohan Deshmukh",
            "coordinator_contact": "+91 98765 12345",
        }
        res_adj = client.post("/api/events", json=payload_adjacent)
        assert res_adj.status_code == 201, f"Adjacent event rejected: {res_adj.text}"
        adj_id = res_adj.json()["id"]

        # 3. Book overlapping conflicting event: 11:30 AM to 02:30 PM (Must be REJECTED with HTTP 409)
        payload_conflict = {
            "title": "AI Masterclass",
            "description": "Conflicting event",
            "category": "Seminar",
            "venue": venue,
            "date": date,
            "registration_deadline": date,
            "start_time": "11:30 AM",
            "end_time": "02:30 PM",
            "capacity": 50,
            "coordinator_name": "Sneha Verma",
            "coordinator_contact": "+91 98765 99999",
        }
        res_conflict = client.post("/api/events", json=payload_conflict)
        assert res_conflict.status_code == 409
        conflict_data = res_conflict.json()
        assert "is_collision" in conflict_data or "error" in conflict_data

        # 4. Test pre-flight check endpoint accurately reports collision
        check_res = client.post(
            "/api/events/check-conflict",
            json={
                "venue": venue,
                "date": date,
                "start_time": "10:00 AM",
                "end_time": "12:00 PM",
            },
        )
        assert check_res.status_code == 200
        assert check_res.json()["is_collision"] is True
        assert "alternative_slots" in check_res.json()
        assert "alternative_venues" in check_res.json()

        # Clean up adjacent event
        client.delete(f"/api/events/{adj_id}")

    finally:
        # Clean up first event
        client.delete(f"/api/events/{evt1_id}")


def test_greedy_earliest_finish_time_optimizer():
    # 4 competing event requests for the same hall
    requests = [
        {"id": "req-1", "title": "Session A", "start_time": "09:00 AM", "end_time": "11:00 AM"},
        {"id": "req-2", "title": "Session B", "start_time": "10:00 AM", "end_time": "01:00 PM"},
        {"id": "req-3", "title": "Session C", "start_time": "11:00 AM", "end_time": "01:30 PM"},
        {"id": "req-4", "title": "Session D", "start_time": "01:30 PM", "end_time": "03:30 PM"},
    ]

    res = client.post("/api/events/optimize-batch", json=requests)
    assert res.status_code == 200
    data = res.json()

    assert data["algorithm"] == "Greedy Earliest Finish Time (EFT)"
    assert data["complexity"] == "O(M log M)"
    # Optimal non-overlapping subset: Session A (09-11), Session C (11-13:30), Session D (13:30-15:30)
    accepted_ids = [r["id"] for r in data["accepted"]]
    assert "req-1" in accepted_ids
    assert "req-3" in accepted_ids
    assert "req-4" in accepted_ids
    # Session B overlaps with A and C, so it must be rejected
    rejected_ids = [r["id"] for r in data["rejected"]]
    assert "req-2" in rejected_ids
