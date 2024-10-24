from typing import Dict, List, Annotated

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse, Response
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.gateway.user_sql_gateway import UserSqlaGateway
from app.adapters.sqlalchemy_db.models import MessageDB, UserDB
from app.api.depends_stub import Stub
from app.application.auth.fastapi_users import fastapi_users
from app.application.auth.user_manager import UserManager
from app.application.chat.chat import get_user_by_id, get_user_by_cookie, get_message, add_message, \
    get_messages_between_users
from app.application.protocols.database.message_database_gateway import MessageDataBaseGateway
from app.application.protocols.database.uow import UoW
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway
from app.main.celery_app import send_notification_via_api

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

    async def disconnect(self, websocket: WebSocket, from_user_id: int, to_user_id: int):
        self.active_connections[from_user_id][to_user_id].remove(websocket)
        if not self.active_connections[from_user_id][to_user_id]:
            del self.active_connections[from_user_id][to_user_id]

        if not self.active_connections[from_user_id]:
            del self.active_connections[from_user_id]

    async def broadcast(self, message_data: dict, user_id: int, interlocutor_id: int):
        user_connections = self.active_connections.get(user_id, {})
        connections = user_connections.get(interlocutor_id, [])
        for connection in connections:
            await connection.send_json(message_data)

    async def display_message_to_sender(self, sender_id: int, recipient_id: int, text: str):
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
    ):
        if recipient_id not in manager.active_connections or manager.active_connections[recipient_id] is []:
            send_notification_via_api.delay(telegram_id, f'У вас новое сообщение: от {recipient_username}')
        await self.broadcast(
            {
                "sender_id": sender_id,
                "message": text
            },
            recipient_id,
            sender_id
        )


manager = ConnectionManager()


@chat_router.websocket("/ws/{recipient_id}")
async def chat_websocket(
        websocket: WebSocket,
        recipient_id: int,
        user_database: Annotated[UserDataBaseGateway, Depends(Stub(UserDataBaseGateway))],
        message_database: Annotated[MessageDataBaseGateway, Depends(Stub(MessageDataBaseGateway))],
        uow: Annotated[UoW, Depends()],
        user_manager: UserManager = Depends(Stub(UserManager)),
):
    current_user = await get_user_by_cookie(user_manager, websocket)

    if current_user is None:
        return

    recipient_user = await get_user_by_id(user_database, recipient_id)

    if recipient_user is None:
        return

    await manager.connect(websocket, current_user.id, recipient_id)
    try:
        while True:
            text = await get_message(websocket)

            await add_message(
                message_database,
                uow,
                current_user.id,
                recipient_user.id,
                text
            )
            await manager.display_message_to_sender(
                current_user.id,
                recipient_id,
                text
            )
            await manager.display_message_to_recipient(
                current_user.id,
                recipient_id,
                text,
                recipient_user.telegram_user_id,
                current_user.username
            )
    except WebSocketDisconnect:
        await manager.disconnect(websocket, current_user.id, recipient_id)


@chat_router.get("/{recipient_id}", response_class=Response)
async def chat_page(
        request: Request,
        recipient_id: int,
        user_database: Annotated[UserDataBaseGateway, Depends(Stub(UserDataBaseGateway))],
        message_database: Annotated[MessageDataBaseGateway, Depends(Stub(MessageDataBaseGateway))],
        user: UserDB = Depends(fastapi_users.current_user(optional=True))
) -> Response:
    if user is None:
        return RedirectResponse(url="/auth/login")

    recipient_user = await get_user_by_id(user_database, recipient_id)

    if recipient_user is None or recipient_user.id == user.id:
        return RedirectResponse(url="/")

    messages = await get_messages_between_users(message_database, user.id, recipient_user.id)
    return templates.TemplateResponse(
        "chat.html",
        {
            "request": request,
            "recipient_user_id": recipient_user.id,
            "recipient_username": recipient_user.username,
            "current_user_id": user.id,
            "messages": messages
        }
    )
