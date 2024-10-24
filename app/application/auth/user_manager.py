from typing import Optional, Annotated, AsyncGenerator

from fastapi import Request, Depends
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from app.adapters.sqlalchemy_db.models import UserDB
from app.api.depends_stub import Stub

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[UserDB, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: UserDB, request: Optional[Request] = None) -> None:
        print(f"User {user.id} has registered.")


async def get_user_manager(
        user_db: Annotated[SQLAlchemyUserDatabase,
                           Depends(Stub(SQLAlchemyUserDatabase))]
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
