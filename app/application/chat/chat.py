import json
from typing import Optional

from starlette.websockets import WebSocket

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.auth.auth_backend import auth_backend
from app.application.auth.user_manager import UserManager
from app.application.protocols.database.message_database_gateway import MessageDataBaseGateway
from app.application.protocols.database.uow import UoW
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway


async def get_user_by_id(
        database: UserDataBaseGateway,
        user_id: int
) -> Optional[UserDB]:
    user = await database.get_user_by_id(user_id)
    return user


async def get_user_by_cookie(
        user_manager: UserManager,
        websocket: WebSocket,
) -> Optional[UserDB]:
    cookie = websocket.cookies.get("fastapiusersauth")
    user = await auth_backend.get_strategy().read_token(cookie, user_manager)
    return user


async def get_message(
        websocket: WebSocket
) -> str:
    data = await websocket.receive_text()
    message_data = json.loads(data)
    message = message_data["message"]
    return message


async def add_message(
        database: MessageDataBaseGateway,
        uow: UoW,
        sender_id: int,
        recipient_id: int,
        text: str
) -> None:
    await database.add_message(sender_id, recipient_id, text)
    await uow.commit()
    return
