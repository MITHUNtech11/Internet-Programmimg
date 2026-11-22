import time
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from server.database import get_db
from server.schemas import EventCreateSchema, EventUpdateSchema
from server.services.interval_scheduler import IntervalScheduler

router = APIRouter(prefix="/api/events", tags=["events"])


class ConflictCheckRequest(BaseModel):
    venue: str
    date: str
    start_time: str
    end_time: str
    exclude_event_id: Optional[str] = None


@router.get("")
def list_events(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    with get_db() as conn:
        query = """
            SELECT 
                e.*,
                o.name as organizer_name,
                o.department as organizer_department,
                COUNT(s.id) as sessions_count
            FROM events e
            LEFT JOIN organizers o ON e.organizer_id = o.id
            LEFT JOIN event_sessions s ON e.id = s.event_id
            WHERE 1=1
        """
        params = []

        if category and category != "All":
            query += " AND e.category = ?"
            params.append(category)

        if status and status != "All":
            query += " AND e.status = ?"
            params.append(status)

        if search and search.strip():
            query += " AND (e.title LIKE ? OR e.description LIKE ? OR e.venue LIKE ? OR e.coordinator_name LIKE ?)"
            search_param = f"%{search.strip()}%"
            params.extend([search_param, search_param, search_param, search_param])

        query += " GROUP BY e.id ORDER BY e.date ASC, e.start_time ASC"

        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


@router.get("/{id}")
def get_event(id: str) -> Dict[str, Any]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                e.*,
                o.name as organizer_name,
                o.department as organizer_department,
                o.email as organizer_email,
                o.role as organizer_role
            FROM events e
            LEFT JOIN organizers o ON e.organizer_id = o.id
            WHERE e.id = ?
            """,
            (id,),
        )
        event_row = cursor.fetchone()
        if not event_row:
            raise HTTPException(status_code=404, detail="Event not found")

        cursor.execute(
            "SELECT * FROM event_sessions WHERE event_id = ? ORDER BY order_index ASC",
            (id,),
        )
        sessions = [dict(s) for s in cursor.fetchall()]

        cursor.execute(
            "SELECT * FROM announcements WHERE event_id = ? ORDER BY created_at DESC",
            (id,),
        )
        announcements = [dict(a) for a in cursor.fetchall()]

        data = dict(event_row)
        data["sessions"] = sessions
        data["announcements"] = announcements
        return data


@router.post("/check-conflict")
def check_event_conflict(payload: ConflictCheckRequest) -> Dict[str, Any]:
    """
    Pre-flight interval collision inspection endpoint.
    Returns collision status, conflicting event details, and intelligent slot/venue recommendations.
    """
    with get_db() as conn:
        conflict = IntervalScheduler.check_venue_collision(
            conn,
            venue=payload.venue,
            date=payload.date,
            start_time=payload.start_time,
            end_time=payload.end_time,
            exclude_event_id=payload.exclude_event_id,
        )
        if conflict:
            return conflict
        return {
            "is_collision": False,
            "message": f"Venue resource '{payload.venue}' is verified completely available for [{payload.start_time}, {payload.end_time}) on {payload.date}.",
            "venue": payload.venue,
            "date": payload.date,
        }


@router.post("/optimize-batch")
def optimize_batch_schedule(requests: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Execute greedy Earliest Finish Time (EFT) batch scheduling algorithm.
    Selects the maximum compatible event subset in O(M log M) time.
    """
    return IntervalScheduler.greedy_earliest_finish_time(requests)


@router.get("/venue-timeline/{date}")
def get_venue_timeline(date: str) -> Dict[str, Any]:
    """
    Retrieve all booked temporal intervals across campus venues for a specific date.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, title, category, venue, start_time, end_time, capacity, registered_count
            FROM events
            WHERE date = ? AND status != 'cancelled'
            ORDER BY venue ASC, start_time ASC
            """,
            (date,),
        )
        events = [dict(r) for r in cursor.fetchall()]
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for ev in events:
            v = ev["venue"]
            if v not in grouped:
                grouped[v] = []
            grouped[v].append(ev)
        return {
            "date": date,
            "venues": grouped,
            "total_events": len(events),
        }


@router.post("", status_code=201)
def create_event(payload: EventCreateSchema) -> Dict[str, Any]:
    event_id = f"evt-{int(time.time() * 1000)}"
    org_id = payload.organizer_id or "org-1"

    with get_db() as conn:
        # Preemptively verify half-open interval collision on requested venue
        conflict = IntervalScheduler.check_venue_collision(
            conn,
            venue=payload.venue,
            date=payload.date,
            start_time=payload.start_time or "09:00 AM",
            end_time=payload.end_time or "05:00 PM",
        )
        if conflict:
            raise HTTPException(
                status_code=409,
                detail=conflict,
            )

        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (
                id, organizer_id, title, description, category, venue, date,
                start_time, end_time, registration_deadline, capacity, registered_count,
                banner_url, coordinator_name, coordinator_contact, status
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, 0,
                ?, ?, ?, 'upcoming'
            )
            """,
            (
                event_id,
                org_id,
                payload.title,
                payload.description,
                payload.category,
                payload.venue,
                payload.date,
                payload.start_time or "09:00 AM",
                payload.end_time or "05:00 PM",
                payload.registration_deadline or payload.date,
                payload.capacity if payload.capacity is not None else 100,
                payload.banner_url
                or "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&auto=format&fit=crop&q=80",
                payload.coordinator_name,
                payload.coordinator_contact or "+91 99999 00000",
            ),
        )

        saved_sessions = []
        if payload.sessions:
            for idx, s in enumerate(payload.sessions):
                s_id = f"ses-{int(time.time() * 1000)}-{idx}"
                cursor.execute(
                    """
                    INSERT INTO event_sessions (
                        id, event_id, round_name, venue_room, start_time, end_time, description, order_index
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        s_id,
                        event_id,
                        s.round_name or f"Session {idx + 1}",
                        s.venue_room or payload.venue,
                        s.start_time or "09:00 AM",
                        s.end_time or "11:00 AM",
                        s.description or "",
                        s.order_index if s.order_index is not None else (idx + 1),
                    ),
                )
                saved_sessions.append(
                    {
                        "id": s_id,
                        "event_id": event_id,
                        "round_name": s.round_name or f"Session {idx + 1}",
                        "venue_room": s.venue_room or payload.venue,
                        "start_time": s.start_time or "09:00 AM",
                        "end_time": s.end_time or "11:00 AM",
                        "description": s.description or "",
                        "order_index": s.order_index if s.order_index is not None else (idx + 1),
                    }
                )

        return {
            "id": event_id,
            "title": payload.title,
            "description": payload.description,
            "category": payload.category,
            "venue": payload.venue,
            "date": payload.date,
            "sessions": saved_sessions,
        }


@router.put("/{id}")
def update_event(id: str, payload: EventUpdateSchema) -> Dict[str, str]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, venue, date, start_time, end_time FROM events WHERE id = ?", (id,))
        existing = cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Event not found")

        # If timing or venue updated, re-verify collision
        target_venue = payload.venue if payload.venue is not None else existing["venue"]
        target_date = payload.date if payload.date is not None else existing["date"]
        target_start = payload.start_time if payload.start_time is not None else existing["start_time"]
        target_end = payload.end_time if payload.end_time is not None else existing["end_time"]

        conflict = IntervalScheduler.check_venue_collision(
            conn,
            venue=target_venue,
            date=target_date,
            start_time=target_start,
            end_time=target_end,
            exclude_event_id=id,
        )
        if conflict:
            raise HTTPException(status_code=409, detail=conflict)

        cursor.execute(
            """
            UPDATE events SET
                title = COALESCE(?, title),
                description = COALESCE(?, description),
                category = COALESCE(?, category),
                venue = COALESCE(?, venue),
                date = COALESCE(?, date),
                start_time = COALESCE(?, start_time),
                end_time = COALESCE(?, end_time),
                registration_deadline = COALESCE(?, registration_deadline),
                capacity = COALESCE(?, capacity),
                coordinator_name = COALESCE(?, coordinator_name),
                coordinator_contact = COALESCE(?, coordinator_contact),
                status = COALESCE(?, status),
                banner_url = COALESCE(?, banner_url)
            WHERE id = ?
            """,
            (
                payload.title,
                payload.description,
                payload.category,
                payload.venue,
                payload.date,
                payload.start_time,
                payload.end_time,
                payload.registration_deadline,
                payload.capacity,
                payload.coordinator_name,
                payload.coordinator_contact,
                payload.status,
                payload.banner_url,
                id,
            ),
        )

        if payload.sessions is not None:
            cursor.execute("DELETE FROM event_sessions WHERE event_id = ?", (id,))
            for idx, s in enumerate(payload.sessions):
                s_id = f"ses-{int(time.time() * 1000)}-{idx}"
                cursor.execute(
                    """
                    INSERT INTO event_sessions (
                        id, event_id, round_name, venue_room, start_time, end_time, description, order_index
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        s_id,
                        id,
                        s.round_name or f"Session {idx + 1}",
                        s.venue_room or existing["venue"],
                        s.start_time or "09:00 AM",
                        s.end_time or "11:00 AM",
                        s.description or "",
                        s.order_index if s.order_index is not None else (idx + 1),
                    ),
                )

        return {"message": "Event updated successfully"}


@router.delete("/{id}")
def delete_event(id: str) -> Dict[str, str]:
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM events WHERE id = ?", (id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event deleted successfully"}
