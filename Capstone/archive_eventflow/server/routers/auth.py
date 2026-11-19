import time
import uuid
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from server.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from server.database import get_db

router = APIRouter(prefix="/api/auth", tags=["authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "student"
    department: Optional[str] = "Computer Science & Engineering"
    year_of_study: Optional[str] = "1st Year"
    roll_number: Optional[str] = None


@router.post("/login")
def login(payload: LoginRequest) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(?)", (payload.email.strip(),))
        user = cursor.fetchone()

        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password.")

        token_data = {
            "sub": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "department": user["department"],
        }
        token = create_access_token(token_data)

        user_dict = dict(user)
        user_dict.pop("password_hash", None)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user_dict,
        }


@router.post("/register", status_code=201)
def register(payload: RegisterRequest) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (payload.email.strip(),))
        if cursor.fetchone():
            raise HTTPException(status_code=409, detail="An account with this email already exists.")

        user_id = f"usr-{int(time.time() * 1000)}"
        hashed = hash_password(payload.password)
        role = payload.role if payload.role in ["student", "organizer", "faculty_dean", "admin"] else "student"

        cursor.execute(
            """
            INSERT INTO users (id, name, email, password_hash, role, department, year_of_study, roll_number)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                payload.name.strip(),
                payload.email.strip(),
                hashed,
                role,
                payload.department or "Computer Science & Engineering",
                payload.year_of_study or "1st Year",
                payload.roll_number,
            ),
        )

        # If registering as organizer, also insert into organizers table
        if role in ["organizer", "faculty_dean", "admin"]:
            cursor.execute(
                """
                INSERT OR IGNORE INTO organizers (id, user_id, name, email, department, role)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    f"org-{user_id}",
                    user_id,
                    payload.name.strip(),
                    payload.email.strip(),
                    payload.department or "Computer Science & Engineering",
                    "Club Lead" if role == "organizer" else "Faculty Coordinator",
                ),
            )

        token_data = {
            "sub": user_id,
            "email": payload.email.strip(),
            "name": payload.name.strip(),
            "role": role,
            "department": payload.department,
        }
        token = create_access_token(token_data)

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "name": payload.name.strip(),
                "email": payload.email.strip(),
                "role": role,
                "department": payload.department,
                "year_of_study": payload.year_of_study,
                "roll_number": payload.roll_number,
            },
        }


@router.get("/me")
def get_me(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (current_user["sub"],))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_dict = dict(user)
        user_dict.pop("password_hash", None)
        return user_dict
