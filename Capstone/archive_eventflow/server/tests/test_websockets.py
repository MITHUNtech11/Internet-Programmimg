import pytest
from fastapi.testclient import TestClient

from server.main import app
from server.websocket_manager import manager

client = TestClient(app)


def test_websocket_connection_and_echo():
    with client.websocket_connect("/ws/events") as websocket:
        # Send ping
        websocket.send_json({"action": "ping"})
        data = websocket.receive_json()
        assert data["type"] == "pong"


def test_websocket_channel_subscription():
    with client.websocket_connect("/ws/notifications") as ws_notify:
        # Verify connection active in manager
        assert len(manager.active_connections.get("notifications", [])) > 0
        ws_notify.send_json({"action": "subscribe", "channel": "bulletins"})
        data = ws_notify.receive_json()
        assert data["status"] == "subscribed"


def test_broadcast_registration_event():
    with client.websocket_connect("/ws/events") as ws:
        # Trigger an action that broadcasts
        reg_payload = {
            "participant_name": "Arun Kumar",
            "email": "arun.kumar@college.edu",
            "phone": "+91 94444 11111",
            "college": "SIMATS",
            "department": "Mechanical Engineering",
            "year_of_study": "4th Year"
        }
        res = client.post("/api/events/evt-2/register", json=reg_payload)
        assert res.status_code == 201

        # Receive WebSocket message
        message = ws.receive_json()
        assert message["type"] == "registration_created"
        assert message["event_id"] == "evt-2"
