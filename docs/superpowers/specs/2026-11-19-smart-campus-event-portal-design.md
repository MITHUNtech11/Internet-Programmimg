# Design Specification: Smart Campus Event Registration & Management Web Portal (EventFlow)
## Production-Grade System Architecture Aligned with Review 1 Presentation (CSA4317)

**Date**: 2026-11-19  
**Status**: Approved by User  
**Course**: CSA4317 - INTERNET PROGRAMMING  
**Project**: Development of a Smart Campus Event Registration and Management Web Portal (EventFlow)  
**Authors**: Swathika P (192324197), Nancy Flora (192324117), Mithun Senthil (192324056)  
**Guide**: Dr. A. Selvakumar, SIMATS Engineering  

---

## 1. System Goals & Requirements

### 1.1 Problem Statement
Campus events such as workshops, hackathons, and symposiums are traditionally coordinated via disconnected paper forms, spreadsheets, and transient messaging groups. This leads to duplicate entries, inaccurate attendance records, delayed broadcast of schedule updates, and venue double-booking conflicts.

### 1.2 Target Objectives (Review 1 Slide 7 Alignment)
1. **Module 1**: Robust User Authentication and Event Management with Role-Based Access Control (RBAC) for students, event organizers (club leads), and faculty administrators.
2. **Module 2**: Online Event Discovery and Registration with atomic capacity control, unique QR pass issuance, and optical scan check-in verification.
3. **Module 3**: Real-Time Notifications and Event Tracking via WebSockets for instantaneous count and bulletin synchronization, SMTP email confirmations with embedded QR passes, and APScheduler background tasks for automated event lifecycle and reminder workflows.

---

## 2. Technical Stack & Architectural Decisions

### 2.1 Technology Selection
* **Backend Framework**: **FastAPI** (Python 3.11+ ASGI), chosen for sub-millisecond asynchronous request latency, automatic OpenAPI 3.1 documentation, native WebSocket support, and strict data validation via Pydantic v2.
* **Security & Auth**: `bcrypt` password hashing with salt rounds + stateless standard **JWT Bearer tokens** (HMAC-SHA256) with role-based FastAPI dependency injection (`require_role`).
* **Database & ORM Layer**: Relational database architecture with **SQLite WAL mode** (zero-configuration local failover with ACID guarantees and foreign keys enabled) and seamless **Supabase Cloud PostgreSQL** connection capabilities.
* **QR Engine**: Python `qrcode` library on the backend producing Base64/PNG image payloads with verifiable `EVF-2026-XXXX` cryptographic tokens.
* **Real-Time Layer**: Native **FastAPI WebSockets** (`/ws/events`, `/ws/notifications`) broadcasting events and ticker updates across all active browser clients without polling.
* **Automated Worker**: **APScheduler** (BackgroundScheduler) managing automated reminder dispatch and status transitions (`upcoming` -> `ongoing` -> `completed`).
* **Email Service**: Asynchronous **SMTP Email Service** with HTML templates, dynamic event details, embedded QR pass, and local console-preview logging fallback.
* **Frontend Client**: **React 18** + **Vite** + **Tailwind CSS** + **Lucide Icons** + **html5-qrcode** scanner.

---

## 3. Data Models & Database Schema

### 3.1 Relational Tables
1. **`users`**:
   - `id` (TEXT PK)
   - `name` (TEXT NOT NULL)
   - `email` (TEXT UNIQUE NOT NULL)
   - `password_hash` (TEXT NOT NULL)
   - `role` (TEXT NOT NULL: `'student'`, `'organizer'`, `'faculty_dean'`, `'admin'`)
   - `department` (TEXT NOT NULL)
   - `year_of_study` (TEXT)
   - `roll_number` (TEXT)
   - `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)

2. **`organizers`**:
   - `id` (TEXT PK)
   - `user_id` (TEXT REFERENCES users(id))
   - `name` (TEXT NOT NULL)
   - `email` (TEXT UNIQUE NOT NULL)
   - `department` (TEXT NOT NULL)
   - `role` (TEXT NOT NULL DEFAULT `'Club Lead'`)
   - `avatar_url` (TEXT)
   - `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)

3. **`events`**:
   - `id` (TEXT PK)
   - `organizer_id` (TEXT REFERENCES organizers(id))
   - `title` (TEXT NOT NULL)
   - `description` (TEXT NOT NULL)
   - `category` (TEXT NOT NULL: `'Technical'`, `'Cultural'`, `'Workshop'`, `'Sports'`, `'General'`)
   - `venue` (TEXT NOT NULL)
   - `date` (TEXT NOT NULL)
   - `start_time` (TEXT NOT NULL)
   - `end_time` (TEXT NOT NULL)
   - `registration_deadline` (TEXT NOT NULL)
   - `capacity` (INTEGER NOT NULL DEFAULT 100)
   - `registered_count` (INTEGER NOT NULL DEFAULT 0)
   - `banner_url` (TEXT)
   - `coordinator_name` (TEXT NOT NULL)
   - `coordinator_contact` (TEXT NOT NULL)
   - `status` (TEXT NOT NULL DEFAULT `'upcoming'`)
   - `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)

4. **`event_sessions`** (Multi-Round Support):
   - `id` (TEXT PK)
   - `event_id` (TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE)
   - `round_name` (TEXT NOT NULL)
   - `venue_room` (TEXT NOT NULL)
   - `start_time` (TEXT NOT NULL)
   - `end_time` (TEXT NOT NULL)
   - `description` (TEXT)
   - `order_index` (INTEGER NOT NULL DEFAULT 1)

5. **`registrations`**:
   - `id` (TEXT PK)
   - `event_id` (TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE)
   - `user_id` (TEXT REFERENCES users(id))
   - `ticket_code` (TEXT NOT NULL UNIQUE)
   - `participant_name` (TEXT NOT NULL)
   - `email` (TEXT NOT NULL)
   - `phone` (TEXT NOT NULL)
   - `college` (TEXT NOT NULL)
   - `department` (TEXT NOT NULL)
   - `year_of_study` (TEXT NOT NULL)
   - `qr_data_url` (TEXT)
   - `registered_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)

6. **`attendance`**:
   - `id` (TEXT PK)
   - `registration_id` (TEXT NOT NULL UNIQUE REFERENCES registrations(id) ON DELETE CASCADE)
   - `event_id` (TEXT NOT NULL REFERENCES events(id) ON DELETE CASCADE)
   - `status` (TEXT NOT NULL DEFAULT `'registered'`) -- `'registered'`, `'checked_in'`, `'absent'`
   - `check_in_time` (DATETIME)

7. **`announcements`**:
   - `id` (TEXT PK)
   - `event_id` (TEXT REFERENCES events(id) ON DELETE CASCADE)
   - `title` (TEXT NOT NULL)
   - `message` (TEXT NOT NULL)
   - `priority` (TEXT NOT NULL DEFAULT `'info'`) -- `'urgent'`, `'update'`, `'info'`
   - `published_by` (TEXT NOT NULL)
   - `created_at` (DATETIME DEFAULT CURRENT_TIMESTAMP)

---

## 4. API Endpoints Contract

### 4.1 Authentication (`/api/auth`)
* `POST /api/auth/register`: Register new student or organizer with bcrypt password hash.
* `POST /api/auth/login`: Authenticate email/password; returns JWT access token + user persona profile.
* `GET /api/auth/me`: Validate JWT token and return active user profile.

### 4.2 Events & Sessions (`/api/events`)
* `GET /api/events`: List events with category, status, and search filters.
* `GET /api/events/{id}`: Detailed event view with nested rounds and announcements.
* `POST /api/events`: Create event (Requires `organizer` or `faculty_dean` role) with interval collision validation.
* `PUT /api/events/{id}`: Update event details or schedule.
* `DELETE /api/events/{id}`: Delete event with cascading cleanup.

### 4.3 Registrations & QR (`/api/registrations`, `/api/tickets`)
* `POST /api/events/{id}/register`: Atomic check on `capacity` and email duplicate; creates registration, generates ticket `EVF-2026-XXXX`, dispatches confirmation email, increments counter, and broadcasts WebSocket update.
* `GET /api/tickets/{ticket_code}/qr`: Returns base64 PNG QR code asset generated by Python `qrcode`.
* `GET /api/registrations/my-registrations`: Retrieves all tickets for logged-in user.
* `GET /api/events/{id}/attendees`: Retrieves event attendee roster for organizers with CSV export support.

### 4.4 Attendance & Check-In (`/api/attendance`)
* `POST /api/attendance/verify`: Validates ticket code, displays attendee card, marks check-in with UTC timestamp, rejects duplicate scans, and pushes WebSocket event.
* `PATCH /api/registrations/{id}/attendance`: Manual override of attendance status.

### 4.5 Real-Time Notifications & Scheduling (`/api/announcements`, `/ws`)
* `GET /api/announcements`: List recent priority broadcasts.
* `POST /api/announcements`: Publish announcement and broadcast to WebSocket channel.
* `WebSocket /ws/events`: Push-notification connection for live registration numbers and attendance counters.
* `WebSocket /ws/notifications`: Push-notification connection for emergency campus bulletins.

---

## 5. Background Services & Real-Time Engine

### 5.1 APScheduler Engine
* Runs as a singleton in the FastAPI lifespan.
* Job 1 (Every 5 minutes): `check_upcoming_reminders` — queries events starting in $<24$ hours and triggers reminder notifications.
* Job 2 (Every 10 minutes): `sync_event_lifecycle` — marks past events as `completed` and active events as `ongoing`.

### 5.2 SMTP Email Dispatcher
* Handles asynchronous email sending using standard Python MIME and SSL/TLS.
* Generates multipart HTML emails featuring event title, schedule, venue, instructions, and inline base64 QR code pass.
* Implements mock/preview fallback logging when running without SMTP server credentials so local testing is 100% reliable.

---

## 6. Testing Strategy
* Unit tests for password hashing (`bcrypt`), JWT verification, and RBAC policies.
* Unit tests for Python `qrcode` generation and half-open $[s, e)$ interval collision detection.
* Integration tests for registration flow, capacity capping, and duplicate rejection.
* WebSocket broadcast testing via FastAPI TestClient.
* End-to-end integration test suite targeting $\ge 30$ automated pytest cases with 100% pass rate.
