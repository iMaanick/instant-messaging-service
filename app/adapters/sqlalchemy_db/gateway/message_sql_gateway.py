from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.sqlalchemy_db.models import MessageDB
from app.application.protocols.database.message_database_gateway import MessageDataBaseGateway


class MessageSqlaGateway(MessageDataBaseGateway):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, sender_id: int, recipient_id: int, text: str) -> None:
        message = MessageDB(
            sender_id=sender_id,
            recipient_id=recipient_id,
            text=text
        )
        self.session.add(message)


