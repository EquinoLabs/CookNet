import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, DateTime, func, ForeignKey
from database.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    object_key = Column(String, nullable=False, unique=True)  # full R2 key
    media_type = Column(String(20), nullable=False)  # "image" or "video"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
