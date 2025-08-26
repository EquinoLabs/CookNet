import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, func, UniqueConstraint
from sqlalchemy.orm import relationship
from database.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Content fields
    content = Column(Text, nullable=True)  # Caption/description
    image_url = Column(String(500), nullable=True)  # Cloudflare image URL
    video_url = Column(String(500), nullable=True)  # Cloudflare video URL
    
    # Recipe specific fields
    recipe_title = Column(String(200), nullable=True)
    ingredients = Column(Text, nullable=True)  # Can store as JSON string or plain text
    instructions = Column(Text, nullable=True)
    cooking_time = Column(Integer, nullable=True)  # in minutes
    servings = Column(Integer, nullable=True)  # number of servings
    difficulty = Column(String(20), nullable=True)  # easy, medium, hard
    cuisine_type = Column(String(50), nullable=True)  # Italian, Mexican, etc.
    
    # Engagement metrics (for performance - avoid COUNT queries)
    likes_count = Column(Integer, default=0, nullable=False)
    comments_count = Column(Integer, default=0, nullable=False)
    saves_count = Column(Integer, default=0, nullable=False)
    
    # Status and visibility
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)  # Index for feed ordering
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Key
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    saves = relationship("Save", back_populates="post", cascade="all, delete-orphan")
    community_id = Column(UUID(as_uuid=True), ForeignKey("communities.id"), nullable=True)
    community = relationship("Community", back_populates="posts")


class Like(Base):
    __tablename__ = "likes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    post = relationship("Post", back_populates="likes")
    
    # Ensure one like per user per post
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    
    # For nested comments (replies)
    parent_comment_id = Column(UUID(as_uuid=True), ForeignKey("comments.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User")
    post = relationship("Post", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], backref="replies")


class Save(Base):
    __tablename__ = "saves"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    post = relationship("Post", back_populates="saves")
    
    # Ensure one save per user per post
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_user_post_save'),)
