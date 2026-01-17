from typing import Any
from app.db.db import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from pydantic import BaseModel
import uuid

class CrudBase[ModelType:Base, CreateSchemaType:BaseModel]:
    def __init__(self, model:type[ModelType]):
        self.model = model

    async def get(self, session:AsyncSession, id) -> ModelType:
        response = await session.execute(select(self.model).where(self.model.id == id))
        return response.scalars().first()

    async def list(self, session:AsyncSession, limit: int) -> list[ModelType]:
        response = await session.execute(select(self.model).limit(limit))
        return response.scalars().all()
    
    async def create(self, session:AsyncSession, object_in:CreateSchemaType) -> ModelType:
        object = object_in.model_dump()
        print(f"modeldump{object} objectin {object_in}")
        obj = self.model(**object)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    
    async def delete(self, session:AsyncSession, id:str) -> ModelType | None:
        obj = await self.get(session, id)
        if not obj:
            return None
        await session.delete(obj)
        await session.commit()
        return obj
