from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from app.adapters.sqlalchemy_db.models import Base


class MessageDB(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    recipient_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
