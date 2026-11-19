import pytest
from server.services.email_service import (
    email_service,
    send_registration_confirmation,
    send_broadcast_alert,
)


def test_send_registration_confirmation_generates_html_and_qr():
    email_service.clear_sent_box()

    success = send_registration_confirmation(
        to_email="student@college.edu",
        participant_name="Pooja Sundar",
        event_title="National AI Symposium 2026",
        ticket_code="EVF-2026-AI99",
        event_date="2026-12-10",
        event_time="10:00 AM - 04:00 PM",
        event_venue="Main University Auditorium",
        qr_data_url="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    )

    assert success is True
    assert len(email_service.sent_emails) == 1
    last_email = email_service.sent_emails[-1]
    assert last_email["to"] == "student@college.edu"
    assert "National AI Symposium 2026" in last_email["subject"]
    assert "EVF-2026-AI99" in last_email["body"]
    assert "Main University Auditorium" in last_email["body"]


def test_send_broadcast_alert():
    email_service.clear_sent_box()

    recipients = ["pooja@college.edu", "arun@college.edu"]
    sent_count = send_broadcast_alert(
        recipients=recipients,
        title="Urgent Room Change",
        message="Session moved to Seminar Hall 3 due to maintenance.",
        priority="urgent"
    )

    assert sent_count == 2
    assert len(email_service.sent_emails) == 2
    assert "URGENT" in email_service.sent_emails[0]["subject"]
    assert "Seminar Hall 3" in email_service.sent_emails[0]["body"]
