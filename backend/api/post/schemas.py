from typing import Optional, List
from pydantic import BaseModel, validator
from datetime import datetime
from api.user.schemas import UserBasic  # Import basic user schema to avoid circular imports
from uuid import UUID

class PostBase(BaseModel):
    content: Optional[str] = None
    recipe_title: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    cooking_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    cuisine_type: Optional[str] = None
    is_public: bool = True


class PostCreate(PostBase):
    # Additional validation for creation
    @validator('difficulty')
    def validate_difficulty(cls, v):
        if v and v.lower() not in ['easy', 'medium', 'hard']:
            raise ValueError('Difficulty must be easy, medium, or hard')
        return v.lower() if v else v
    
    @validator('cooking_time')
    def validate_cooking_time(cls, v):
        if v and v <= 0:
            raise ValueError('Cooking time must be positive')
        return v
    
    @validator('servings')
    def validate_servings(cls, v):
        if v and v <= 0:
            raise ValueError('Servings must be positive')
        return v


class PostUpdate(BaseModel):
    content: Optional[str] = None
    recipe_title: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    cooking_time: Optional[int] = None
    servings: Optional[int] = None
    difficulty: Optional[str] = None
    cuisine_type: Optional[str] = None
    is_public: Optional[bool] = None


# For file upload response
class MediaUploadResponse(BaseModel):
    url: str
    file_type: str  # image or video
    size: int


class PostResponse(PostBase):
    id: UUID
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    likes_count: int
    comments_count: int
    saves_count: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: UserBasic
    
    # User interaction flags (if authenticated user)
    is_liked: Optional[bool] = None
    is_saved: Optional[bool] = None
    
    class Config:
        from_attributes = True


# For feed response with pagination
class FeedResponse(BaseModel):
    posts: List[PostResponse]
    has_more: bool
    next_cursor: Optional[UUID] = None
    total_count: Optional[int] = None


# Like related schemas
class LikeResponse(BaseModel):
    liked: bool
    likes_count: int


# Comment schemas
class CommentBase(BaseModel):
    content: str
    parent_comment_id: Optional[UUID] = None


class CommentCreate(CommentBase):
    @validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Comment content cannot be empty')
        if len(v) > 1000:
            raise ValueError('Comment cannot exceed 1000 characters')
        return v.strip()


class CommentResponse(CommentBase):
    id: UUID
    user: UserBasic
    created_at: datetime
    updated_at: Optional[datetime] = None
    replies: List['CommentResponse'] = []  # For nested comments
    
    class Config:
        from_attributes = True


# Update the forward reference for nested comments
CommentResponse.model_rebuild()


class CommentsResponse(BaseModel):
    comments: List[CommentResponse]
    total_count: int


# Save response
class SaveResponse(BaseModel):
    saved: bool
    saves_count: int


# Search and filter schemas
class PostFilters(BaseModel):
    cuisine_type: Optional[str] = None
    difficulty: Optional[str] = None
    max_cooking_time: Optional[int] = None
    min_cooking_time: Optional[int] = None
    author_id: Optional[UUID] = None
    search_query: Optional[str] = None  # For searching in title, content, ingredients


# Statistics schema (for dashboard)
class PostStats(BaseModel):
    total_posts: int
    total_likes: int
    total_comments: int
    total_saves: int
    average_engagement: float
