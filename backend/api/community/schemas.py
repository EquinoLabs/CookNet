# api/community/schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
import re

# Base schemas
class CommunityBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=50)
    rules: Optional[str] = Field(None, max_length=2000)
    is_private: bool = False
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError('Community name cannot be empty')
        return v.strip()
    
    @validator('category')
    def validate_category(cls, v):
        if v:
            allowed_categories = [
                'cooking', 'baking', 'healthy-eating', 'vegetarian', 
                'vegan', 'desserts', 'international', 'quick-meals', 
                'meal-prep', 'restaurant-reviews', 'food-photography', 'other'
            ]
            if v.lower() not in allowed_categories:
                raise ValueError(f'Category must be one of: {", ".join(allowed_categories)}')
        return v.lower() if v else v

class CommunityCreate(CommunityBase):
    pass

class CommunityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    category: Optional[str] = Field(None, max_length=50)
    rules: Optional[str] = Field(None, max_length=2000)
    is_private: Optional[bool] = None

# User schemas for community context
class CommunityMember(BaseModel):
    id: UUID
    username: str
    display_name: Optional[str]
    profile_picture_url: Optional[str]
    joined_at: datetime
    role: str = "member"  # member, moderator, admin
    
    class Config:
        from_attributes = True

class CommunityCreator(BaseModel):
    id: UUID
    username: str
    display_name: Optional[str]
    profile_picture_url: Optional[str]
    
    class Config:
        from_attributes = True

# Community response schemas
class CommunityResponse(CommunityBase):
    id: UUID
    slug: str
    display_photo_url: Optional[str]
    banner_photo_url: Optional[str]
    is_verified: bool
    member_count: int
    post_count: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: CommunityCreator
    
    class Config:
        from_attributes = True

class CommunityDetailResponse(CommunityResponse):
    members: List[CommunityMember] = []
    is_member: bool = False  # Whether current user is a member
    user_role: Optional[str] = None  # Current user's role in community
    
    class Config:
        from_attributes = True

class CommunityListResponse(BaseModel):
    communities: List[CommunityResponse]
    total: int
    page: int
    size: int
    total_pages: int

# Membership schemas
class JoinCommunityRequest(BaseModel):
    invite_code: Optional[str] = None  # For private communities

class MembershipResponse(BaseModel):
    community_id: UUID
    user_id: UUID
    role: str
    joined_at: datetime
    
    class Config:
        from_attributes = True

# Invite schemas
class CreateInviteRequest(BaseModel):
    max_uses: Optional[int] = Field(1, ge=1, le=100)
    expires_in_hours: Optional[int] = Field(24, ge=1, le=168)  # Max 1 week
    invited_user_id: Optional[UUID] = None  # For specific user invites

class InviteResponse(BaseModel):
    id: UUID
    invite_code: str
    community_id: UUID
    max_uses: int
    current_uses: int
    expires_at: Optional[datetime]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Search and filter schemas
class CommunityFilters(BaseModel):
    category: Optional[str] = None
    search: Optional[str] = None
    is_private: Optional[bool] = None
    is_verified: Optional[bool] = None
    min_members: Optional[int] = Field(None, ge=0)
    max_members: Optional[int] = Field(None, ge=1)

# Statistics schema
class CommunityStats(BaseModel):
    total_members: int
    total_posts: int
    posts_this_week: int
    new_members_this_week: int
    top_contributors: List[CommunityMember]
    
    class Config:
        from_attributes = True
