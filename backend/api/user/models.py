import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database.database import Base
from api.community.models import community_members
from api.user.enum import RoleEnum

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default=RoleEnum.user.value, nullable=False, server_default=RoleEnum.user.value) # options: "user", "admin", "moderator"

    # Google OAuth fields
    google_id = Column(String(255), unique=True, nullable=True, index=True)
    is_email_verified = Column(Boolean, default=False, nullable=False)
    verification_email_sent = Column(Boolean, default=False)

    # Optional fields
    profile_image = Column(String(255), nullable=True)  # URL to profile image
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship with posts
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    # Relationship with communities
    created_communities = relationship("Community", back_populates="created_by")
    joined_communities = relationship("Community", secondary=community_members, back_populates="members")
