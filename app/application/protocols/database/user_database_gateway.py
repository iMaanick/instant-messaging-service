from abc import ABC, abstractmethod
from typing import List, Optional

from app.adapters.sqlalchemy_db.models import UserDB


class UserDataBaseGateway(ABC):
    @abstractmethod
    async def get_users_excluding_current(self, user_id: int) -> List[UserDB]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[UserDB]:
        raise NotImplementedError
