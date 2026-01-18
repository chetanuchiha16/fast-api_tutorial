from fastapi_users.db import SQLAlchemyBaseUserTableUUID, SQLAlchemyUserDatabase
from app.db.posts import Post
from sqlalchemy.orm import relationship
from app.db.db import Base
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db import get_async_session


class User(SQLAlchemyBaseUserTableUUID, Base):
    posts = relationship("Post", back_populates="user")


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)