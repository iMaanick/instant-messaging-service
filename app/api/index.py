# from typing import Annotated, List
#
# from fastapi import APIRouter, Request, Depends, WebSocketDisconnect
#
# from app.adapters.sqlalchemy_db.models import UserDB
# from app.api.auth import templates
# from app.api.depends_stub import Stub
# from app.application.auth.auth import auth_backend
# from app.application.auth.fastapi_users import fastapi_users
# from app.application.auth.user_manager import get_user_manager, UserManager
# from app.application.protocols.database.database_gateway import DatabaseGateway
# from app.application.protocols.database.uow import UoW
#
# index_router = APIRouter()
#
# # @index_router.get("/")
# # async def index(
# #         request: Request,
# #         database: Annotated[DatabaseGateway, Depends()],
# #         uow: Annotated[UoW, Depends()],
# # ) -> dict:
# #     # user = await database.add_user()
# #     # await uow.commit()
# #     # return {"1": user.id}
# #     return {"1": 1231}
#
# from fastapi import FastAPI, WebSocket
# from fastapi.responses import HTMLResponse
#
# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
#
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: list[WebSocket] = []
#
#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)
#
#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)
#
#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)
#
#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)
#
#
# manager = ConnectionManager()
#
#
# @index_router.get("/")
# async def get(
#         request: Request,
#         user: UserDB = Depends(fastapi_users.current_user(optional=True))
# ):
#     if user:
#         return HTMLResponse(html)
#     return templates.TemplateResponse("login.html", {"request": request})
#
#
# @index_router.websocket("/ws/{client_id}")
# async def websocket_endpoint(
#         websocket: WebSocket,
#         client_id: int,
#         user_manager: Annotated[UserManager, Depends(Stub(UserManager))],
# ):
#     cookie = websocket.cookies.get("fastapiusersauth")
#     user = await auth_backend.get_strategy().read_token(cookie, user_manager)
#     if user:
#         print("YES USER")
#     else:
#         print("NO USER")
#     await manager.connect(websocket)
#     print(manager.active_connections)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
