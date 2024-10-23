from typing import Annotated, List

from fastapi import Depends

from app.adapters.sqlalchemy_db.gateway.user_sql_gateway import UserSqlaGateway
from app.adapters.sqlalchemy_db.models import UserDB
from app.api.depends_stub import Stub


async def get_users_excluding_current(
        database: Annotated[UserSqlaGateway, Depends(Stub(UserSqlaGateway))],
        user_id: int
) -> List[UserDB]:
    users = await database.get_users_excluding_current(user_id)
    return users
