import pytest
from fastapi.testclient import TestClient

from server.main import app
from server.qr_service import generate_qr_matrix, generate_qr_data_url, generate_qr_png_bytes

client = TestClient(app)


def test_qr_service_matrix_and_data_url():
    ticket = "EVF-2026-TEST"
    matrix = generate_qr_matrix(ticket)
    assert len(matrix) == 25
    assert len(matrix[0]) == 25
    # Finder pattern corner check
    assert matrix[0][0] == 1
    assert matrix[0][6] == 1
    assert matrix[6][0] == 1

    data_url = generate_qr_data_url(ticket)
    assert data_url.startswith("data:image/")
    assert len(data_url) > 100

    png_bytes = generate_qr_png_bytes(ticket)
    assert png_bytes.startswith(b"\x89PNG")


def test_get_ticket_qr_endpoint():
    response = client.get("/api/tickets/EVF-2026-X801/qr")
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG")


def test_registration_returns_qr_data_url():
    payload = {
        "participant_name": "Divya Prakash",
        "email": "divya.prakash@college.edu",
        "phone": "+91 91234 56789",
        "college": "SIMATS Engineering",
        "department": "Information Technology",
        "year_of_study": "3rd Year"
    }
    response = client.post("/api/events/evt-1/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "ticket_code" in data
    assert "qr_data_url" in data
    assert data["qr_data_url"].startswith("data:image/")


def test_attendance_verification_duplicate_prevention():
    # 1. Verify valid ticket with auto check-in
    res1 = client.post("/api/attendance/verify", json={"ticket_code": "EVF-2026-X801", "auto_check_in": True})
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["verified"] is True
    assert data1["registration"]["attendance_status"] == "checked_in"

    # 2. Re-verify the same ticket -> must indicate already checked in
    res2 = client.post("/api/attendance/verify", json={"ticket_code": "EVF-2026-X801", "auto_check_in": True})
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["already_checked_in"] is True
    assert "Already Checked In" in data2["message"]
