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

engine = create_async_engine(DATABASE_URI)

session_maker = async_sessionmaker(expire_on_commit=True, bind=engine)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session