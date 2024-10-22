from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.adapters.sqlalchemy_db.models.base import Base

if TYPE_CHECKING:
    from ..chat import MessageDB


class UserDB(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    telegram_user_id: Mapped[int] = mapped_column(Integer, nullable=True)

    sent_messages: Mapped[list["MessageDB"]] = relationship("MessageDB", foreign_keys="MessageDB.from_user_id",
                                                            back_populates="from_user")
    received_messages: Mapped[list["MessageDB"]] = relationship("MessageDB", foreign_keys="MessageDB.to_user_id",
                                                                back_populates="to_user")