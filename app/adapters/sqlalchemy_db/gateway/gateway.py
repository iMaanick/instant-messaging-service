from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.adapters.sqlalchemy_db.models import UserDB
from app.application.protocols.database.database_gateway import DatabaseGateway


class SqlaGateway(DatabaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self) -> UserDB:
        user = UserDB(email="mnk@mail.ru", username="mnk", hashed_password="fgss",
                      is_active=True,
                      is_superuser=False,
                      is_verified=False
                      )
        self.session.add(user)
        return user
