from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.adapters.sqlalchemy_db.models import Base

if TYPE_CHECKING:
    from app.adapters.sqlalchemy_db.models import UserDB


class MessageDB(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    to_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)

    from_user: Mapped["UserDB"] = relationship("UserDB", foreign_keys=[from_user_id], back_populates="sent_messages")
    to_user: Mapped["UserDB"] = relationship("UserDB", foreign_keys=[to_user_id], back_populates="received_messages")
