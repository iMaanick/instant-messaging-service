import json
from typing import Optional, List

from pydantic import ValidationError
from starlette.websockets import WebSocket

from app.adapters.sqlalchemy_db.models import UserDB, MessageDB
from app.application.auth.auth_backend import auth_backend
from app.application.auth.user_manager import UserManager
from app.application.models.chat.message import MessageModel
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


async def get_message(websocket: WebSocket) -> str:
    data = await websocket.receive_text()
    message_data = json.loads(data)
    try:
        validated_data = MessageModel(**message_data)
        return validated_data.message
    except ValidationError as e:
        print(f"Validation error: {e}")
        raise ValueError("Invalid message format")


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


async def get_messages_between_users(
        database: MessageDataBaseGateway,
        first_user_id: int,
        second_user_id: int
) -> List[MessageDB]:
    messages = await database.get_messages_between_users(first_user_id, second_user_id)
    return messages
