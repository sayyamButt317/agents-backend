from __future__ import annotations

import asyncio
from typing import Dict, Set
from fastapi import WebSocket
from app.utils.mongo_serializer import serialize_mongo_data


class WebSocketManager:
    def __init__(self) -> None:
        self._all_connections: Set[WebSocket] = set()
        self._user_connections: Dict[str, Set[WebSocket]] = {}
        self._role_connections: Dict[str, Set[WebSocket]] = {}
        self._lock = asyncio.Lock()

    # =========================
    # CONNECT
    # =========================
    async def connect(
        self,
        websocket: WebSocket,
        *,
        user_id: str | None = None,
        role: str | None = None,
    ):
        await websocket.accept()

        async with self._lock:
            self._all_connections.add(websocket)

            if user_id:
                self._user_connections.setdefault(user_id, set()).add(websocket)

            if role:
                self._role_connections.setdefault(role, set()).add(websocket)

        print("\n🔌 WS CONNECTED")
        print(f"Total connections: {len(self._all_connections)}")
        print(f"User ID: {user_id}")
        print(f"Role   : {role}")

    # =========================
    # DISCONNECT
    # =========================
    async def disconnect(self, websocket: WebSocket):
        disconnected_users = []

        async with self._lock:
            self._all_connections.discard(websocket)

            for user_id, sockets in self._user_connections.items():
                if websocket in sockets:
                    sockets.discard(websocket)
                    disconnected_users.append((user_id, len(sockets)))

            for role, sockets in self._role_connections.items():
                if websocket in sockets:
                    sockets.discard(websocket)

        print("\n❌ WS DISCONNECTED")
        print(f"Total connections: {len(self._all_connections)}")

        for user_id, count in disconnected_users:
            print(f"👤 User {user_id} now has {count} socket(s)")

    # =========================
    # SEND TO SINGLE USER
    # =========================
    async def send_to_user(self, user_id: str, payload: dict) -> int:

        serialized_payload = serialize_mongo_data(payload)

        async with self._lock:
            sockets = list(self._user_connections.get(user_id, set()))

        print("\n" + "=" * 80)
        print("📡 SEND_TO_USER")
        print(f"User ID           : {user_id}")
        print(f"Connected sockets : {len(sockets)}")
        print(f"Type              : {payload.get('type')}")
        print("=" * 80)

        delivered = 0

        for ws in sockets:
            try:
                await ws.send_json(serialized_payload)
                delivered += 1
                print("✅ Delivered to socket")
            except Exception as e:
                print(f"❌ WS send failed: {e}")

        print(f"📊 Total delivered: {delivered}")
        print("=" * 80 + "\n")

        return delivered

    # =========================
    # BROADCAST BY ROLE (IMPORTANT)
    # =========================
    async def broadcast_role(self, role: str, payload: dict) -> int:

        serialized_payload = serialize_mongo_data(payload)

        async with self._lock:
            sockets = list(self._role_connections.get(role, set()))

        print("\n" + "=" * 80)
        print("📡 BROADCAST_ROLE")
        print(f"Role              : {role}")
        print(f"Connected sockets : {len(sockets)}")
        print(f"Type              : {payload.get('type')}")
        print("=" * 80)

        delivered = 0

        for ws in sockets:
            try:
                await ws.send_json(serialized_payload)
                delivered += 1
                print("✅ Delivered to role socket")
            except Exception as e:
                print(f"❌ WS send failed: {e}")

        print(f"📊 Total delivered: {delivered}")
        print("=" * 80 + "\n")

        return delivered

    # =========================
    # GLOBAL BROADCAST
    # =========================
    async def broadcast_event(self, event_type: str, payload: dict) -> int:

        message = {
            "type": event_type,
            "payload": serialize_mongo_data(payload),
        }

        async with self._lock:
            sockets = list(self._all_connections)

        print("\n" + "=" * 80)
        print("📡 BROADCAST_EVENT")
        print(f"Event             : {event_type}")
        print(f"Total sockets     : {len(sockets)}")
        print("=" * 80)

        delivered = 0

        for ws in sockets:
            try:
                await ws.send_json(message)
                delivered += 1
                print("✅ Delivered to global socket")
            except Exception as e:
                print(f"❌ WS send failed: {e}")

        print(f"📊 Total delivered: {delivered}")
        print("=" * 80 + "\n")

        return delivered

    # =========================
    # DEBUG
    # =========================
    def debug_connections(self):
        print("\n" + "=" * 80)
        print("🔍 ACTIVE WS CONNECTIONS")
        print("=" * 80)
        print(f"Total sockets: {len(self._all_connections)}")
        print("\nUsers:")
        for user_id, sockets in self._user_connections.items():
            print(f"  {user_id} -> {len(sockets)} socket(s)")
        print("\nRoles:")
        for role, sockets in self._role_connections.items():
            print(f"  {role} -> {len(sockets)} socket(s)")
        print("=" * 80 + "\n")


ws_manager = WebSocketManager()
