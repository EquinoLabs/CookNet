# api/community/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base
import uuid

# Association table for many-to-many relationship between users and communities
community_members = Table(
    'community_members',
    Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('community_id', UUID(as_uuid=True), ForeignKey('communities.id'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), server_default=func.now()),
    Column('role', String(20), default='member'),  # member, moderator, admin
    UniqueConstraint('user_id', 'community_id', name='unique_user_community')
)

class Community(Base):
    __tablename__ = "communities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)  # URL-friendly name
    description = Column(Text)
    display_photo_url = Column(String(500))
    banner_photo_url = Column(String(500))  # Extra: banner image
    
    # Community settings
    is_private = Column(Boolean, default=False)  # Extra: private communities
    is_verified = Column(Boolean, default=False)  # Extra: verified badge
    member_count = Column(Integer, default=0)  # Cached member count
    post_count = Column(Integer, default=0)  # Cached post count
    
    # Community rules and info
    rules = Column(Text)  # Extra: community rules
    category = Column(String(50))  # Extra: Food, Cooking, Baking, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign keys
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Relationships
    created_by = relationship("User", back_populates="created_communities")
    members = relationship(
        "User", 
        secondary=community_members, 
        back_populates="joined_communities"
    )
    posts = relationship("Post", back_populates="community", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Community(name='{self.name}', members={self.member_count})>"

class CommunityInvite(Base):
    __tablename__ = "community_invites"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    community_id = Column(UUID(as_uuid=True), ForeignKey("communities.id"), nullable=False)
    invited_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    invited_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))  # Optional: specific user
    invite_code = Column(String(50), unique=True, nullable=False)  # For shareable links
    
    # Invite settings
    expires_at = Column(DateTime(timezone=True))
    max_uses = Column(Integer, default=1)
    current_uses = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    community = relationship("Community")
    invited_by = relationship("User", foreign_keys=[invited_by_id])
    invited_user = relationship("User", foreign_keys=[invited_user_id])

# Add these to your existing User model (api/user/models.py)
# created_communities = relationship("Community", back_populates="created_by")
# joined_communities = relationship("Community", secondary=community_members, back_populates="members")

# Add this to your existing Post model (api/post/models.py) if you want posts to belong to communities
# community_id = Column(UUID(as_uuid=True), ForeignKey("communities.id"), nullable=True)
# community = relationship("Community", back_populates="posts")
