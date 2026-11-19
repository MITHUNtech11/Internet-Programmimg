from datetime import datetime, timezone
import logging
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler

from server.database import get_db
from server.websocket_manager import manager
from server.services.email_service import send_broadcast_alert

logger = logging.getLogger("eventflow.scheduler")

scheduler: Optional[BackgroundScheduler] = None


def job_sync_event_lifecycle() -> int:
    """
    Check for events that have passed their scheduled date and mark them 'completed'.
    """
    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with get_db() as conn:
        cursor = conn.cursor()
        # Find events with date earlier than today and status 'upcoming' or 'ongoing'
        cursor.execute(
            """
            UPDATE events 
            SET status = 'completed' 
            WHERE date < ? AND status IN ('upcoming', 'ongoing')
            """,
            (now_date,),
        )
        updated_count = cursor.rowcount
        if updated_count > 0:
            logger.info(f"Lifecycle Sync: Marked {updated_count} past event(s) as 'completed'")
            manager.broadcast_sync("events", {"type": "lifecycle_sync", "updated_count": updated_count})
        return updated_count


def job_check_event_reminders() -> int:
    """
    Find events occurring today or tomorrow and dispatch automated reminders.
    """
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    scanned_count = 0
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.id, e.title, e.date, e.start_time, e.venue 
            FROM events e
            WHERE e.date >= ? AND e.status = 'upcoming'
            LIMIT 10
            """,
            (today_str,),
        )
        upcoming_events = cursor.fetchall()
        scanned_count = len(upcoming_events)

        for evt in upcoming_events:
            # Query registered participants
            cursor.execute(
                "SELECT email FROM registrations WHERE event_id = ?",
                (evt["id"],),
            )
            recipients = [r["email"] for r in cursor.fetchall() if r["email"]]
            if recipients:
                logger.info(f"Dispatching reminder for {evt['title']} to {len(recipients)} participant(s)")
                # Send notice through email and WebSocket
                manager.broadcast_sync(
                    "notifications",
                    {
                        "type": "event_reminder",
                        "event_id": evt["id"],
                        "title": f"Reminder: {evt['title']}",
                        "message": f"Event begins on {evt['date']} at {evt['start_time']} ({evt['venue']}). Please arrive on time with your QR pass.",
                    },
                )
    return scanned_count


def start_scheduler() -> BackgroundScheduler:
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler(daemon=True)
        # Register interval jobs
        scheduler.add_job(job_sync_event_lifecycle, "interval", minutes=10, id="sync_lifecycle")
        scheduler.add_job(job_check_event_reminders, "interval", minutes=30, id="event_reminders")

    if not scheduler.running:
        scheduler.start()
        logger.info("APScheduler background engine started successfully.")
    return scheduler


def stop_scheduler():
    global scheduler
    if scheduler is not None and scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("APScheduler background engine shut down.")
