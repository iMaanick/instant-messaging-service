import os
from functools import partial
from logging import getLogger
from typing import Iterable

from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.adapters.sqlalchemy_db.gateway.message_sql_gateway import MessageSqlaGateway
from app.adapters.sqlalchemy_db.gateway.user_sql_gateway import UserSqlaGateway
from app.adapters.sqlalchemy_db.models import UserDB
from app.api.depends_stub import Stub
from app.application.auth.user_manager import UserManager, get_user_manager
from app.application.protocols.database.message_database_gateway import MessageDataBaseGateway
from app.application.protocols.database.uow import UoW
from app.application.protocols.database.user_database_gateway import UserDataBaseGateway

logger = getLogger(__name__)


def all_depends(cls: type) -> None:
    """
    Adds `Depends()` to the class `__init__` methods, so it can be used
    a fastapi dependency having own dependencies
    """
    init = cls.__init__
    total_ars = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(total_ars)
    )



async def new_user_gateway(session: AsyncSession = Depends(Stub(AsyncSession))):
    yield UserSqlaGateway(session)


async def new_message_gateway(session: AsyncSession = Depends(Stub(AsyncSession))):
    yield MessageSqlaGateway(session)


async def new_uow(session: AsyncSession = Depends(Stub(AsyncSession))):
    return session


async def get_new_user_db(session: AsyncSession = Depends(Stub(AsyncSession))):
    yield SQLAlchemyUserDatabase(session, UserDB)


def create_session_maker():
    load_dotenv()
    db_uri = os.getenv('DATABASE_URI')
    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_async_engine(
        db_uri,
        echo=True,
        # pool_size=15,
        # max_overflow=15,
        # connect_args={
        #     "connect_timeout": 5,
        # },
    )
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def new_session(session_maker: async_sessionmaker) -> Iterable[AsyncSession]:
    async with session_maker() as session:
        yield session


def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()

    app.dependency_overrides[AsyncSession] = partial(new_session, session_maker)
    app.dependency_overrides[UserDataBaseGateway] = new_user_gateway
    app.dependency_overrides[MessageDataBaseGateway] = new_message_gateway

    app.dependency_overrides[SQLAlchemyUserDatabase] = get_new_user_db
    app.dependency_overrides[UserManager] = get_user_manager
    app.dependency_overrides[UoW] = new_uow
