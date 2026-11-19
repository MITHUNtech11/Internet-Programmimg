import pytest
from server.services.scheduler import (
    start_scheduler,
    stop_scheduler,
    job_check_event_reminders,
    job_sync_event_lifecycle,
    scheduler
)
from server.database import get_db


def test_scheduler_lifecycle():
    sched = start_scheduler()
    assert sched is not None
    assert sched.running is True
    stop_scheduler()
    assert sched.running is False


def test_job_sync_event_lifecycle():
    # Insert an event in the past with status 'upcoming'
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO events (
                id, organizer_id, title, description, category, venue, date,
                start_time, end_time, registration_deadline, capacity, registered_count,
                coordinator_name, coordinator_contact, status
            ) VALUES (
                'evt-past-test', 'org-1', 'Past Event Test', 'Desc', 'Technical', 'Hall 1',
                '2020-01-01', '09:00 AM', '11:00 AM', '2020-01-01', 50, 10,
                'Coord', '+91 99999 11111', 'upcoming'
            )
            """
        )

    # Run lifecycle job
    updated_count = job_sync_event_lifecycle()
    assert updated_count >= 1

    # Verify event is now marked 'completed'
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM events WHERE id = 'evt-past-test'")
        row = cursor.fetchone()
        assert row["status"] == "completed"


def test_job_check_event_reminders():
    # Runs without errors and returns number of upcoming events scanned
    scanned_count = job_check_event_reminders()
    assert isinstance(scanned_count, int)
    assert scanned_count >= 0
