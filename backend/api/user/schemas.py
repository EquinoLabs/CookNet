from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    username: str
    email: EmailStr


# For registration
class UserCreate(UserBase):
    password: str


# For login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Basic user info for posts/relationships (to avoid circular imports)
class UserBasic(BaseModel):
    id: UUID
    username: str
    profile_image: Optional[str] = None

    class Config:
        from_attributes = True  # Updated from orm_mode for Pydantic v2


# For returning user info (without password)
class UserResponse(UserBase):
    id: UUID
    is_active: bool
    profile_image: Optional[str] = None   # optional

    class Config:
        orm_mode = True  # allows conversion from ORM objects


# For JWT token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


# For token data
class TokenData(BaseModel):
    user_id: Optional[UUID] = None
