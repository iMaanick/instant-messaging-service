from typing import Dict, List, Union

from starlette.websockets import WebSocket
from app.main.celery_app import send_notification_via_api


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[int, Dict[int, List[WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, from_user_id: int, to_user_id: int) -> None:
        await websocket.accept()
        if from_user_id not in self.active_connections:
            self.active_connections[from_user_id] = {}
        if to_user_id not in self.active_connections[from_user_id]:
            self.active_connections[from_user_id][to_user_id] = []
        self.active_connections[from_user_id][to_user_id].append(websocket)

    async def disconnect(self, websocket: WebSocket, from_user_id: int, to_user_id: int) -> None:
        self.active_connections[from_user_id][to_user_id].remove(websocket)
        if not self.active_connections[from_user_id][to_user_id]:
            del self.active_connections[from_user_id][to_user_id]

        if not self.active_connections[from_user_id]:
            del self.active_connections[from_user_id]

    async def broadcast(self, message_data: Dict[str, Union[str, int]], user_id: int, interlocutor_id: int) -> None:
        user_connections = self.active_connections.get(user_id, {})
        connections = user_connections.get(interlocutor_id, [])
        for connection in connections:
            await connection.send_json(message_data)

    async def display_message_to_sender(self, sender_id: int, recipient_id: int, text: str) -> None:
        await self.broadcast(
            {
                "sender_id": sender_id,
                "message": text
            },
            sender_id,
            recipient_id
        )

    async def display_message_to_recipient(
            self,
            sender_id: int,
            recipient_id: int,
            text: str,
            telegram_id: int,
            recipient_username: str
    ) -> None:
        if recipient_id not in self.active_connections:
            send_notification_via_api.delay(telegram_id, f'У вас новое сообщение: от {recipient_username}')
        await self.broadcast(
            {
                "sender_id": sender_id,
                "message": text
            },
            recipient_id,
            sender_id
        )
