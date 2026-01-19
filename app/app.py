from fastapi import FastAPI, HTTPException, Form, File, UploadFile, Depends
from app.schemas.post import PostModel, PostCreateSchema
from contextlib import asynccontextmanager
from app.db.db import create_db_and_tables
from sqlalchemy import select
from app.crud.post import post_crud
from app.api import api_router
from app.users import fastapi_users, auth_backend, current_active_users
from app.schemas.users import UserCreate, UserRead, UserUpdate

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api")
app.include_router(fastapi_users.get_auth_router(backend=auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/auth", tags=["auth"])