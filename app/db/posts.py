from sqlalchemy import Column, Text, String, DateTime
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db.db import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    caption = Column( Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))