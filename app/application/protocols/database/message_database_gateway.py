from abc import abstractmethod, ABC
from typing import List

from app.adapters.sqlalchemy_db.models import MessageDB


class MessageDataBaseGateway(ABC):
    @abstractmethod
    async def add_message(self, sender_id: int, recipient_id: int, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_messages_between_users(self, first_user_id: int, second_user_id: int) -> List[MessageDB]:
        raise NotImplementedError

