from fastapi import APIRouter

from .auth import auth_router
from .chat import chat_router
# from .index import index_router
from .index import index_router
from ..application.auth.auth import auth_backend
from ..application.auth.fastapi_users import fastapi_users
from ..application.auth.models import UserRead, UserCreate

root_router = APIRouter()


root_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

root_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

root_router.include_router(
    auth_router,
    tags=["test"]

)

root_router.include_router(
    chat_router,
)

root_router.include_router(
    index_router,
)
