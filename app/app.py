from fastapi import FastAPI, HTTPException, Form, File, UploadFile, Depends
from app.schemas.schema import PostModel, PostCreateSchema
from contextlib import asynccontextmanager
from app.db.db import create_db_and_tables, get_async_session, AsyncSession, Post
from sqlalchemy import select
from app.crud.PostCrud import post_crud
from app.api import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")