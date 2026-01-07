from typing import Any
from app.db import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
class CrudBase[ModelType:Base, CreateSchemaType:BaseModel]:
    def __init__(self, model:type[ModelType]):
        self.model = model

    async def get(self, session:AsyncSession, limit) -> list[ModelType]:
        response = await session.execute(select(self.model).limit(limit))
        return response.scalars().all()
    
    async def post(self, session:AsyncSession, *, object_in:BaseModel) -> ModelType:
        object = object_in.model_dump()
        obj = self.model(**object)
        session.add(obj)
        await session.commit()
        await session.refresh(self.model)
        return obj