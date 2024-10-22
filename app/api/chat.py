import json
from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.models import MessageDB, UserDB
from app.api.depends_stub import Stub
from app.application.auth.auth import auth_backend
from app.application.auth.fastapi_users import fastapi_users
from app.application.auth.user_manager import UserManager

chat_router = APIRouter(prefix="/chat", tags=["chat"])

templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, List[WebSocket]]] = {}

    async def connect(self, websocket: WebSocket, from_user_id: int, to_user_id: int):
        await websocket.accept()
        if from_user_id not in self.active_connections:
            self.active_connections[from_user_id] = {}
        if to_user_id not in self.active_connections[from_user_id]:
            self.active_connections[from_user_id][to_user_id] = []
        self.active_connections[from_user_id][to_user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, from_user_id: int, to_user_id: int):
        self.active_connections[from_user_id][to_user_id].remove(websocket)

    async def broadcast(self, message: dict, from_user_id: int, to_user_id: int):
        from_user_connections = self.active_connections.get(from_user_id, {})
        connections = from_user_connections.get(to_user_id, [])
        for connection in connections:
            await connection.send_json(message)


manager = ConnectionManager()


@chat_router.websocket("/ws/{recipient_id}")
async def chat_websocket(
        websocket: WebSocket,
        recipient_id: int,
        session: AsyncSession = Depends(Stub(AsyncSession)),
        user_manager: UserManager = Depends(Stub(UserManager)),
):
    cookie = websocket.cookies.get("fastapiusersauth")
    current_user = await auth_backend.get_strategy().read_token(cookie, user_manager)

    result = await session.execute(select(UserDB).where(UserDB.id == recipient_id))
    recipient_user = result.scalars().first()
    print("recipient_user: ", recipient_user)
    if recipient_user is None:
        return

    await manager.connect(websocket, current_user.id, recipient_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            message = message_data["message"]

            new_message = MessageDB(
                from_user_id=current_user.id,
                to_user_id=recipient_id,
                text=message
            )
            session.add(new_message)
            await session.commit()
            await session.refresh(new_message)

            await manager.broadcast(
                {
                    "sender_id": current_user.id,
                    "sender_name": "You",
                    "message": message
                },
                current_user.id,
                recipient_id
            )
            await manager.broadcast(
                {
                    "sender_id": current_user.id,
                    "sender_name": recipient_user.username,
                    "message": message
                },
                recipient_id,
                current_user.id
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, current_user.id, recipient_id)


@chat_router.get("/{recipient_id}")
async def chat_page(
        request: Request,
        recipient_id: int,
        session: AsyncSession = Depends(Stub(AsyncSession)),
        user: UserDB = Depends(fastapi_users.current_user(optional=True))

):
    result = await session.execute(select(UserDB).where(UserDB.id == recipient_id))
    recipient_user = result.scalars().first()
    if recipient_user is None:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("chat.html", {"request": request,
                                                    "recipient_id": recipient_id,
                                                    "current_user": user,
                                                    "current_user_id": user.id
                                                    })
