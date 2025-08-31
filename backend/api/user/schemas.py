import re
from typing import Optional
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from uuid import UUID
from api.user.enum import RoleEnum

# Base user model
class UserBase(BaseModel):
    username: str
    email: EmailStr

# For Google OAuth login
class GoogleLoginRequest(BaseModel):
    token: str

# For email verification
class EmailVerificationRequest(BaseModel):
    token: str

# For resending verification email
class ResendVerificationRequest(BaseModel):
    email: str

# For registration
class UserCreate(UserBase):
    password: str
    role: RoleEnum = RoleEnum.user

    @validator("username")
    def validate_username(cls, v):
        if len(v) > 20:  # you can adjust max length (e.g., 15–20 is common)
            raise ValueError("Username must not exceed 20 characters")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v

    @validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[!@#$%^&*()\-_=+\[\]{};:'\",.<>/?\\|]", v):
            raise ValueError("Password must contain at least one special character")
        return v

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
    role: RoleEnum = RoleEnum.user 

    class Config:
        orm_mode = True  # allows conversion from ORM objects

# For user creation with role
class UserCreateWithRole(UserBase):
    password: str
    role: RoleEnum

# For JWT token response
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse

# For token data
class TokenData(BaseModel):
    user_id: Optional[UUID] = None
