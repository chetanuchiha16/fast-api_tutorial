from fastapi_users import BaseUserManager, UUIDIDMixin, FastAPIUsers
from app.db.users import User
import uuid
from app.config import settings
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi import Depends
from app.db.users import get_user_db
from fastapi_users.authentication import JWTStrategy, BearerTransport, AuthenticationBackend

class UserManager(UUIDIDMixin, BaseUserManager[User,uuid.UUID]):
    reset_password_token_secret = settings.AUTH_SECRET
    verification_token_secret = settings.AUTH_SECRET

async def get_user_manager(user_db:SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db=user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
    return JWTStrategy(secret=settings.AUTH_SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager=get_user_manager, auth_backends=[auth_backend])

current_active_users = fastapi_users.current_user(active=True)