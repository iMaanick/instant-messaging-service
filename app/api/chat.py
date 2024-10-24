from typing import Annotated

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Request
from starlette.responses import RedirectResponse, Response
from starlette.templating import Jinja2Templates

from app.adapters.sqlalchemy_db.models import UserDB
from app.api.depends_stub import Stub
from app.application.auth.fastapi_users import fastapi_users
from app.application.auth.user_manager import UserManager
from app.application.chat.chat import get_user_by_id, get_user_by_cookie, get_message, add_message, \
    get_messages_between_users
from app.application.chat.connection_manager import ConnectionManager
from app.application.protocols.database.message_database_gateway import MessageDataBaseGateway
from app.application.protocols.database.uow import UoW
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway

chat_router = APIRouter(prefix="/chat", tags=["chat"])

templates = Jinja2Templates(directory="app/templates")

manager = ConnectionManager()


@chat_router.websocket("/ws/{recipient_id}")
async def chat_websocket(
        websocket: WebSocket,
        recipient_id: int,
        user_database: Annotated[UserDataBaseGateway, Depends(Stub(UserDataBaseGateway))],
        message_database: Annotated[MessageDataBaseGateway, Depends(Stub(MessageDataBaseGateway))],
        uow: Annotated[UoW, Depends()],
        user_manager: UserManager = Depends(Stub(UserManager)),
) -> None:
    """
        Handles WebSocket connections for real-time chat between users.
    """
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
    """
       Renders the chat page for the current user to chat with a specified recipient.

       This endpoint retrieves the chat history between the current user and the recipient
       specified by recipient_id. If the user is not authenticated or the recipient is invalid,
       the user is redirected accordingly.

       Returns:
           Response: The rendered chat page or a redirect response.

       Redirects:
           - To the login page if the user is not authenticated.
           - To the index page if the recipient is invalid or is the same as the current user.
    """
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
