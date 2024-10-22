from typing import Annotated

from fastapi import Depends
from fastapi_users import FastAPIUsers

from app.adapters.sqlalchemy_db.models import UserDB
from app.api.depends_stub import Stub
from app.application.auth.auth import auth_backend
from app.application.auth.user_manager import get_user_manager, UserManager

fastapi_users = FastAPIUsers[UserDB, int](
    get_user_manager,
    [auth_backend],
)