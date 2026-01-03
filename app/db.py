import uuid
from collections.abc import AsyncGenerator
from sqlalchemy import Column, String, Text, DateTime, ForeignKey

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone
from app.config import settings
# Format: postgresql+asyncpg://user:password@host:port/dbname
DATABASE_URI = settings.DATABASE_URI

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column( Text)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))

engine = create_async_engine(DATABASE_URI)

session_session_maker = async_sessionmaker(expire_on_commit=True)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_sesson() -> AsyncGenerator[AsyncSession, None]:
    async with session_session_maker() as session:
        yield session