from typing import List

from sqlalchemy import select
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

    async def get_messages_between_users(self, first_user_id: int, second_user_id: int) -> List[MessageDB]:
        stmt = (
            select(MessageDB)
            .filter(
                (MessageDB.sender_id == first_user_id) &
                (MessageDB.recipient_id == second_user_id) |
                (MessageDB.sender_id == second_user_id) &
                (MessageDB.recipient_id == first_user_id)
            )
            .order_by(MessageDB.id)
        )

        result = await self.session.execute(stmt)
        messages = result.scalars().all()
        return list(messages)



