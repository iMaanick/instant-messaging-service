from abc import ABC, abstractmethod

from app.adapters.sqlalchemy_db.models import UserDB


class DatabaseGateway(ABC):
    @abstractmethod
    async def add_user(self) -> UserDB:
        raise NotImplementedError
