from fastapi_users import FastAPIUsers

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.auth.auth_backend import auth_backend
from app.application.auth.user_manager import get_user_manager

fastapi_users = FastAPIUsers[UserDB, int](
    get_user_manager,
    [auth_backend],
)
