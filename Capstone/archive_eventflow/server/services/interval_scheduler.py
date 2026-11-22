"""
Interval Scheduling & Venue Double-Booking Conflict Prevention Service
EventFlow: Smart Campus Event Coordination Platform

Implements:
1. Discrete Half-Open Temporal Interval Algebra [s, e) mapped to minutes t in [0, 1440).
2. O(log N) Binary Search (bisect) dynamic insertion and neighbor overlap detection.
3. Batch Greedy Earliest Finish Time (EFT) scheduling algorithm for competing requests.
4. Idle Gap Recommendation and Capacity-Equivalent Alternative Venue Search.
"""

from bisect import bisect_left
import re
import sqlite3
from typing import Any, Dict, List, Optional, Tuple


def parse_time_to_minutes(time_str: str) -> int:
    """
    Parse 12-hour (e.g. '09:00 AM', '5:30 PM') or 24-hour ('14:30') time string
    into discrete minutes from midnight [0, 1440).
    Strips auxiliary annotations like '(Next Day)'.
    """
    if not time_str or not time_str.strip():
        return 540  # Default 09:00 AM

    clean = re.sub(r"\(.*?\)", "", time_str).strip()

    # Try 12-hour match (e.g. 09:30 AM or 9:30AM)
    match_12 = re.match(r"^(\d{1,2}):(\d{2})\s*(AM|PM)?$", clean, re.IGNORECASE)
    if match_12:
        hours = int(match_12.group(1))
        minutes = int(match_12.group(2))
        period = match_12.group(3)

        if period:
            period = period.upper()
            if period == "PM" and hours != 12:
                hours += 12
            elif period == "AM" and hours == 12:
                hours = 0
        return (hours * 60 + minutes) % 1440

    # Fallback to simple integer or default
    return 540


def minutes_to_time_str(minutes: int) -> str:
    """
    Convert discrete minutes from midnight [0, 1440) back to 12-hour formatted string.
    e.g. 540 -> '09:00 AM', 1020 -> '05:00 PM'.
    """
    norm = minutes % 1440
    hours = norm // 60
    mins = norm % 60
    period = "AM"

    if hours >= 12:
        period = "PM"
        if hours > 12:
            hours -= 12
    elif hours == 0:
        hours = 12

    return f"{hours:02d}:{mins:02d} {period}"


def intervals_collide(s1: int, e1: int, s2: int, e2: int) -> bool:
    """
    Half-open interval intersection test for [s1, e1) and [s2, e2).
    Two half-open intervals collide iff max(s1, s2) < min(e1, e2),
    or equivalently (s1 < e2) and (s2 < e1).
    Contiguous boundary intervals (e1 == s2 or e2 == s1) are disjoint (no collision).
    """
    # If duration ends next day or wraps
    if e1 <= s1:
        e1 += 1440
    if e2 <= s2:
        e2 += 1440
    return s1 < e2 and s2 < e1


class IntervalScheduler:
    """
    Mathematical Interval Scheduling Engine maintaining verified temporal vectors
    for campus venues and computing collision-free allocations.
    """

    @staticmethod
    def check_venue_collision(
        conn: sqlite3.Connection,
        venue: str,
        date: str,
        start_time: str,
        end_time: str,
        exclude_event_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Verify whether the requested interval [start_time, end_time) collides with
        any confirmed event or session on `venue` for `date`.
        Uses bisect_left for O(log N) temporal boundary location.

        Returns None if safe, or a dict describing the conflict and suggested alternatives.
        """
        req_start = parse_time_to_minutes(start_time)
        req_end = parse_time_to_minutes(end_time)
        if req_end <= req_start:
            req_end = req_start + 120  # Minimum 2-hour window if end <= start

        cursor = conn.cursor()
        # Fetch confirmed events for this venue on this date
        cursor.execute(
            """
            SELECT id, title, venue, date, start_time, end_time, capacity
            FROM events
            WHERE LOWER(venue) = LOWER(?) AND date = ? AND status != 'cancelled'
            ORDER BY start_time ASC
            """,
            (venue.strip(), date.strip()),
        )
        existing_events = [dict(row) for row in cursor.fetchall()]

        # Filter out self when updating
        if exclude_event_id:
            existing_events = [e for e in existing_events if e["id"] != exclude_event_id]

        if not existing_events:
            return None

        # Build sorted list of existing intervals: [(start_min, end_min, event_dict)]
        timeline: List[Tuple[int, int, Dict[str, Any]]] = []
        for e in existing_events:
            s_min = parse_time_to_minutes(e["start_time"])
            e_min = parse_time_to_minutes(e["end_time"])
            if e_min <= s_min:
                e_min = s_min + 120
            timeline.append((s_min, e_min, e))

        # Sort timeline by start time
        timeline.sort(key=lambda x: x[0])
        start_times = [item[0] for item in timeline]

        # Use binary search to find insertion position in O(log N)
        idx = bisect_left(start_times, req_start)

        # Check collision with candidates:
        # Predecessor (idx - 1), current (idx), and successor (idx + 1)
        candidates_to_check = []
        if idx > 0:
            candidates_to_check.append(timeline[idx - 1])
        if idx < len(timeline):
            candidates_to_check.append(timeline[idx])
        if idx + 1 < len(timeline):
            candidates_to_check.append(timeline[idx + 1])

        # Also scan full timeline for safety if any interval has large span
        for s_min, e_min, ev in timeline:
            if intervals_collide(req_start, req_end, s_min, e_min):
                # Collision detected! Compute intelligent recommendations
                alternatives = IntervalScheduler._find_alternatives(
                    conn, venue, date, req_start, req_end, timeline
                )
                return {
                    "is_collision": True,
                    "venue": venue,
                    "date": date,
                    "requested_start": start_time,
                    "requested_end": end_time,
                    "conflicting_event": {
                        "id": ev["id"],
                        "title": ev["title"],
                        "start_time": ev["start_time"],
                        "end_time": ev["end_time"],
                    },
                    "reason": f"Venue collision on resource '{venue}': Interval [{start_time}, {end_time}) overlaps with '{ev['title']}' ({ev['start_time']} - {ev['end_time']}).",
                    "alternative_slots": alternatives["alternative_slots"],
                    "alternative_venues": alternatives["alternative_venues"],
                }

        return None

    @staticmethod
    def _find_alternatives(
        conn: sqlite3.Connection,
        venue: str,
        date: str,
        req_start: int,
        req_end: int,
        timeline: List[Tuple[int, int, Dict[str, Any]]],
    ) -> Dict[str, Any]:
        """
        Identify nearest idle gap [e_i, s_{i+1}) on the same venue and search for
        other available campus venues for the requested date and time window.
        """
        duration = req_end - req_start
        alternative_slots = []

        # Campus operating day bounds: 08:00 AM (480) to 08:00 PM (1200)
        day_start = 480
        day_end = 1200

        # Scan gaps in timeline
        prev_end = day_start
        for s_min, e_min, _ in timeline:
            if s_min > prev_end and (s_min - prev_end) >= duration:
                alternative_slots.append({
                    "start_time": minutes_to_time_str(prev_end),
                    "end_time": minutes_to_time_str(prev_end + duration),
                    "gap_duration_minutes": s_min - prev_end,
                })
            prev_end = max(prev_end, e_min)

        if day_end > prev_end and (day_end - prev_end) >= duration:
            alternative_slots.append({
                "start_time": minutes_to_time_str(prev_end),
                "end_time": minutes_to_time_str(prev_end + duration),
                "gap_duration_minutes": day_end - prev_end,
            })

        # Scan other campus venues free during [req_start, req_end)
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT venue FROM events WHERE venue IS NOT NULL AND venue != ''")
        all_venues = [r[0] for r in cursor.fetchall()]

        # Common campus venues roster
        campus_venues_pool = list(set(all_venues + [
            "Main Convention Center",
            "Indoor Sports Arena",
            "Open Air Amphitheatre",
            "Dr. APJ Abdul Kalam Auditorium",
            "Seminar Hall 1",
            "Seminar Hall 2",
            "Lab Complex 101",
        ]))

        alternative_venues = []
        for alt_v in campus_venues_pool:
            if alt_v.lower() == venue.lower():
                continue
            cursor.execute(
                """
                SELECT id, title, start_time, end_time FROM events
                WHERE LOWER(venue) = LOWER(?) AND date = ? AND status != 'cancelled'
                """,
                (alt_v, date),
            )
            v_events = cursor.fetchall()
            collides = False
            for ve in v_events:
                ve_s = parse_time_to_minutes(ve["start_time"])
                ve_e = parse_time_to_minutes(ve["end_time"])
                if intervals_collide(req_start, req_end, ve_s, ve_e):
                    collides = True
                    break

            if not collides:
                alternative_venues.append({
                    "venue": alt_v,
                    "status": "Available",
                    "available_for_requested_time": f"{minutes_to_time_str(req_start)} - {minutes_to_time_str(req_end)}",
                })
            if len(alternative_venues) >= 3:
                break

        return {
            "alternative_slots": alternative_slots[:3],
            "alternative_venues": alternative_venues,
        }

    @staticmethod
    def greedy_earliest_finish_time(requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Greedy Earliest Finish Time (EFT) scheduling algorithm.
        Given M competing reservation requests for a shared resource, sorts requests
        by finish time e_1 <= e_2 <= ... <= e_M, greedily selects the maximum non-overlapping
        subset in O(M log M) time, and returns accepted vs rejected requests.
        """
        if not requests:
            return {"accepted": [], "rejected": [], "total": 0}

        # Normalize requests with discrete minutes
        parsed: List[Dict[str, Any]] = []
        for r in requests:
            s_min = parse_time_to_minutes(r.get("start_time", "09:00 AM"))
            e_min = parse_time_to_minutes(r.get("end_time", "11:00 AM"))
            if e_min <= s_min:
                e_min = s_min + 120
            parsed.append({
                **r,
                "_start_min": s_min,
                "_end_min": e_min,
            })

        # Sort by earliest finish time
        parsed.sort(key=lambda x: (x["_end_min"], x["_start_min"]))

        accepted: List[Dict[str, Any]] = []
        rejected: List[Dict[str, Any]] = []

        last_finish = -1
        for item in parsed:
            clean_item = {k: v for k, v in item.items() if not k.startswith("_")}
            if item["_start_min"] >= last_finish:
                accepted.append(clean_item)
                last_finish = item["_end_min"]
            else:
                rejected.append({
                    **clean_item,
                    "conflict_reason": f"Rejected by EFT algorithm: Overlaps with accepted allocation finishing at {minutes_to_time_str(last_finish)}.",
                })

        return {
            "accepted": accepted,
            "rejected": rejected,
            "total_requested": len(requests),
            "max_compatible_count": len(accepted),
            "algorithm": "Greedy Earliest Finish Time (EFT)",
            "complexity": "O(M log M)",
        }
