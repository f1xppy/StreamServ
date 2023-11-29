from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase)
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import mapped_column, relationship

from app.users import database
from geoalchemy2 import Geometry


class Group(database.BASE):
    __tablename__ = 'groupTable'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(length=128))


class User(SQLAlchemyBaseUserTableUUID, database.BASE):
    nickname = Column(String(length=128), nullable=True)
    real_name = Column(String(length=128), nullable=True)
    age = Column(Integer(), nullable=True)
    geopos = Column(Geometry(geometry_type="POINT", srid=4326), nullable=True)
    group_id = mapped_column(ForeignKey("groupTable.id"))
    group = relationship("Group", uselist=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database.initializer.async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
