import pytest
from fastapi.testclient import TestClient

from server.main import app
from server.auth import hash_password, verify_password, create_access_token, decode_access_token

client = TestClient(app)


def test_password_hashing():
    raw = "SecurePassword123!"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation_and_decode():
    payload = {"sub": "user-123", "email": "test@college.edu", "role": "student"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "user-123"
    assert decoded["email"] == "test@college.edu"
    assert decoded["role"] == "student"


def test_auth_login_seeded_student():
    response = client.post(
        "/api/auth/login",
        json={"email": "aditya.nair@college.edu", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "student"
    assert data["user"]["email"] == "aditya.nair@college.edu"


def test_auth_login_seeded_organizer():
    response = client.post(
        "/api/auth/login",
        json={"email": "aarav.sharma@college.edu", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "organizer"


def test_auth_login_invalid_password():
    response = client.post(
        "/api/auth/login",
        json={"email": "aditya.nair@college.edu", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["error"]


def test_auth_register_and_me():
    new_user = {
        "name": "Kavya Ramesh",
        "email": "kavya.ramesh@college.edu",
        "password": "mypassword123",
        "role": "student",
        "department": "Computer Science & Engineering",
        "year_of_study": "2nd Year",
        "roll_number": "CS24B1099"
    }
    # Register
    reg_res = client.post("/api/auth/register", json=new_user)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    token = reg_data["access_token"]
    assert reg_data["user"]["name"] == "Kavya Ramesh"

    # Verify /api/auth/me
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "kavya.ramesh@college.edu"
