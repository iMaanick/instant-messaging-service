from abc import abstractmethod, ABC

from app.adapters.sqlalchemy_db.models import MessageDB


class MessageDataBaseGateway(ABC):
    @abstractmethod
    async def add_message(self, sender_id: int, recipient_id: int, text: str) -> None:
        raise NotImplementedError

