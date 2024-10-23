from typing import Annotated, List

from fastapi import Depends

from app.adapters.sqlalchemy_db.gateway.user_sql_gateway import UserSqlaGateway
from app.adapters.sqlalchemy_db.models import UserDB
from app.api.depends_stub import Stub
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway


async def get_users_excluding_current(
        database: UserDataBaseGateway,
        user_id: int
) -> List[UserDB]:
    users = await database.get_users_excluding_current(user_id)
    return users
