from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway


class UserSqlaGateway(UserDataBaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_users_excluding_current(self, user_id: int) -> List[UserDB]:
        result = await self.session.execute(select(UserDB).where(UserDB.id != user_id).order_by(UserDB.username))
        users = result.scalars().all()
        return list(users)

    async def get_user_by_id(self, user_id: int) -> Optional[UserDB]:
        result = await self.session.execute(select(UserDB).where(UserDB.id == user_id))
        recipient_user = result.scalars().first()
        return recipient_user
