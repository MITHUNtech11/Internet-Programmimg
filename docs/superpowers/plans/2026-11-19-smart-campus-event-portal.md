# Smart Campus Event Registration & Management Web Portal (EventFlow) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the EventFlow platform into a production-grade implementation strictly aligned with the Review 1 PPT requirements, featuring real JWT/bcrypt RBAC authentication, server-side Python QR code generation, FastAPI WebSockets for live synchronization, an SMTP confirmation email service, and an APScheduler background engine.

**Architecture:** A high-performance FastAPI ASGI backend exposing modular REST and WebSocket endpoints, backed by a relational SQLite WAL database (with Supabase PostgreSQL support). The service layer coordinates real-time event broadcasts, email dispatches, and scheduled reminder workers, consuming and feeding a responsive React 18 frontend with complete Poppins typography and camera scanner support.

**Tech Stack:** Python 3.11, FastAPI, Uvicorn, PyJWT, Cryptography/Bcrypt, Pydantic v2, WebSockets, APScheduler, Python MIME/SMTP, React 18, Vite, Tailwind CSS, html5-qrcode.

**Spec:** `docs/superpowers/specs/2026-11-19-smart-campus-event-portal-design.md`

## Global Constraints
- Python 3.11+ compatibility on Windows.
- SQLite database configured with `PRAGMA foreign_keys = ON` and `PRAGMA journal_mode = WAL`.
- Deterministic ticket code format: `EVF-2026-XXXX`.
- JWT token signing using HMAC-SHA256 (`HS256`) with secret from environment.
- Email service must be resilient: if SMTP credentials are not configured, it logs the complete HTML preview without throwing exceptions.
- Zero broken tests: all existing 28 tests must remain passing, with new tests expanding coverage to $\ge 35$ tests.

## Review Focus
1. **Unauthenticated mutations**: Verify requests to create/delete events without a valid Bearer token are rejected with HTTP 401/403.
2. **Double-booking collision edge case**: Verify adjacent half-open events $[s_1, e_1)$ and $[e_1, e_2)$ are permitted while overlapping intervals are rejected with HTTP 409.
3. **Capacity overflow under concurrency**: Verify that when capacity is 1, two simultaneous registration requests result in exactly one HTTP 201 and one HTTP 400.
4. **Offline email resilience**: Verify registration succeeds with HTTP 201 even when external SMTP network is unreachable.
5. **WebSocket disconnect hygiene**: Verify client disconnection does not crash the server connection manager or block broadcasts to remaining clients.

---

### Task 1: Core Database Schema & Authentication Infrastructure (Module 1)

**Files:**
- Create: `server/auth.py`
- Modify: `server/database.py`
- Create: `server/routers/auth.py`
- Modify: `server/main.py`
- Create: `server/tests/test_auth.py`

**Interfaces:**
- Produces: `hash_password(password: str) -> str`
- Produces: `verify_password(password: str, hashed: str) -> bool`
- Produces: `create_access_token(data: dict) -> str`
- Produces: `get_current_user(token: str = Depends(oauth2_scheme)) -> dict`
- Produces: `require_role(allowed_roles: list[str]) -> Callable`

- [ ] **Step 1: Write failing tests for password hashing, token creation, and auth routes in `server/tests/test_auth.py`**
- [ ] **Step 2: Run `pytest server/tests/test_auth.py` to confirm failure**
- [ ] **Step 3: Implement `server/auth.py` with password hashing (`hashlib.pbkdf2_hmac` / `cryptography` + salt) and `jwt` encode/decode**
- [ ] **Step 4: Update `server/database.py` to include `users` table schema, indices, and seed accounts for Student, Organizer, and Faculty**
- [ ] **Step 5: Implement `server/routers/auth.py` exposing `/api/auth/register`, `/api/auth/login`, and `/api/auth/me`**
- [ ] **Step 6: Mount `auth_router` in `server/main.py`**
- [ ] **Step 7: Run `pytest server/tests/test_auth.py` to verify all pass**

---

### Task 2: Python QR Code Generation & Optical Attendance Verification (Module 2)

**Files:**
- Create: `server/qr_service.py`
- Modify: `server/routers/registrations.py`
- Modify: `server/routers/attendance.py`
- Create: `server/tests/test_qr_attendance.py`

**Interfaces:**
- Produces: `generate_qr_data_url(text: str) -> str`
- Produces: `generate_qr_png_bytes(text: str) -> bytes`
- Consumes: `generate_ticket_code() -> str`

- [ ] **Step 1: Write failing tests for QR asset generation and optical scan check-in in `server/tests/test_qr_attendance.py`**
- [ ] **Step 2: Run `pytest server/tests/test_qr_attendance.py` to confirm failure**
- [ ] **Step 3: Implement `server/qr_service.py` generating standard 2D QR matrix rendered to base64 Data URL and PNG bytes**
- [ ] **Step 4: Add `GET /api/tickets/{code}/qr` endpoint and embed `qr_data_url` in `/api/events/{id}/register` response**
- [ ] **Step 5: Enhance `/api/attendance/verify` with strict duplicate check-in timestamps and replay detection**
- [ ] **Step 6: Run `pytest server/tests/test_qr_attendance.py` to verify all pass**

---

### Task 3: Native WebSockets Real-Time Synchronization Hub (Module 3)

**Files:**
- Create: `server/websocket_manager.py`
- Modify: `server/main.py`
- Modify: `server/routers/registrations.py`
- Modify: `server/routers/attendance.py`
- Modify: `server/routers/announcements.py`
- Create: `server/tests/test_websockets.py`

**Interfaces:**
- Produces: `ConnectionManager.connect(websocket: WebSocket, channel: str)`
- Produces: `ConnectionManager.disconnect(websocket: WebSocket, channel: str)`
- Produces: `ConnectionManager.broadcast(channel: str, message: dict)`

- [ ] **Step 1: Write failing tests for WebSocket connection and broadcast in `server/tests/test_websockets.py`**
- [ ] **Step 2: Run `pytest server/tests/test_websockets.py` to confirm failure**
- [ ] **Step 3: Implement `ConnectionManager` in `server/websocket_manager.py` handling channel subscriptions (`events`, `notifications`)**
- [ ] **Step 4: Mount `WebSocket /ws/{channel}` endpoints in `server/main.py`**
- [ ] **Step 5: Trigger real-time broadcast in `registrations.py`, `attendance.py`, and `announcements.py`**
- [ ] **Step 6: Run `pytest server/tests/test_websockets.py` to verify all pass**

---

### Task 4: Production SMTP Email Confirmation Service (Module 3)

**Files:**
- Create: `server/services/email_service.py`
- Modify: `server/routers/registrations.py`
- Modify: `server/routers/announcements.py`
- Create: `server/tests/test_email_service.py`

**Interfaces:**
- Produces: `send_registration_confirmation(to_email: str, participant_name: str, event_title: str, ticket_code: str, qr_data_url: str)`
- Produces: `send_broadcast_alert(recipients: list[str], title: str, message: str, priority: str)`

- [ ] **Step 1: Write failing tests for email composition and fallback delivery in `server/tests/test_email_service.py`**
- [ ] **Step 2: Run `pytest server/tests/test_email_service.py` to confirm failure**
- [ ] **Step 3: Implement `email_service.py` with multi-part HTML templates and non-blocking delivery**
- [ ] **Step 4: Connect email triggers upon successful registration and emergency announcements**
- [ ] **Step 5: Run `pytest server/tests/test_email_service.py` to verify all pass**

---

### Task 5: APScheduler Background Engine (Module 3)

**Files:**
- Create: `server/services/scheduler.py`
- Modify: `server/main.py`
- Create: `server/tests/test_scheduler.py`

**Interfaces:**
- Produces: `start_scheduler() -> BackgroundScheduler`
- Produces: `stop_scheduler()`
- Produces: `job_check_event_reminders()`
- Produces: `job_sync_event_lifecycle()`

- [ ] **Step 1: Write failing tests for scheduler jobs in `server/tests/test_scheduler.py`**
- [ ] **Step 2: Run `pytest server/tests/test_scheduler.py` to confirm failure**
- [ ] **Step 3: Implement `scheduler.py` using `apscheduler.schedulers.background.BackgroundScheduler`**
- [ ] **Step 4: Wire scheduler startup/shutdown into FastAPI lifespan in `server/main.py`**
- [ ] **Step 5: Run `pytest server/tests/test_scheduler.py` to verify all pass**

---

### Task 6: Frontend Client Integration & Production Build

**Files:**
- Modify: `client/src/services/api.js`
- Modify: `client/src/components/AnnouncementTicker.jsx`
- Modify: `client/src/components/TicketPassModal.jsx`
- Modify: `client/src/context/AuthContext.jsx`

- [ ] **Step 1: Update `api.js` to handle real JWT authentication tokens and WebSocket connections**
- [ ] **Step 2: Connect `AnnouncementTicker.jsx` to live WebSocket notifications**
- [ ] **Step 3: Ensure `TicketPassModal.jsx` renders server-provided QR code asset**
- [ ] **Step 4: Execute production build `npm run build` in client and confirm 0 errors**

---

### Task 7: Full System Verification & Defense Artifact Update

**Files:**
- Update: `brain/<conv-id>/review_report.md`

- [ ] **Step 1: Run full pytest suite across entire backend: `pytest server/tests` (Confirm $\ge 35$ tests passing)**
- [ ] **Step 2: Verify all endpoints through automated integration pass**
- [ ] **Step 3: Update Review 1 defense artifact with final verified production metrics**
