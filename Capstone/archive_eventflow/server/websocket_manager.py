import asyncio
import logging
from typing import Any, Dict, List
from fastapi import WebSocket

logger = logging.getLogger("eventflow.ws")


class ConnectionManager:
    def __init__(self):
        # Maps channel_name -> list of active WebSockets
        self.active_connections: Dict[str, List[WebSocket]] = {
            "events": [],
            "notifications": [],
            "general": [],
        }

    async def connect(self, websocket: WebSocket, channel: str = "events"):
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = []
        self.active_connections[channel].append(websocket)
        logger.info(f"WebSocket client connected to channel '{channel}'. Total: {len(self.active_connections[channel])}")

    def disconnect(self, websocket: WebSocket, channel: str = "events"):
        if channel in self.active_connections:
            if websocket in self.active_connections[channel]:
                self.active_connections[channel].remove(websocket)
                logger.info(f"WebSocket client disconnected from '{channel}'. Remaining: {len(self.active_connections[channel])}")

    async def broadcast(self, channel: str, message: Dict[str, Any]):
        """
        Asynchronously send message to all clients connected to channel.
        """
        connections = self.active_connections.get(channel, [])
        dead_connections = []
        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Error broadcasting to WebSocket client: {e}")
                dead_connections.append(connection)

        for dead in dead_connections:
            self.disconnect(dead, channel)

    def broadcast_sync(self, channel: str, message: Dict[str, Any]):
        """
        Synchronous wrapper to safely schedule broadcast from sync route handlers.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.create_task(self.broadcast(channel, message))
            else:
                loop.run_until_complete(self.broadcast(channel, message))
        except Exception:
            # When called from separate threads or if no loop running, create task in new loop
            try:
                new_loop = asyncio.new_event_loop()
                new_loop.run_until_complete(self.broadcast(channel, message))
                new_loop.close()
            except Exception as e:
                logger.error(f"Failed to broadcast sync: {e}")


manager = ConnectionManager()
