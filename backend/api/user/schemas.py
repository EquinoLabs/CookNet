from typing import Optional
from pydantic import BaseModel, EmailStr


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


# For returning user info (without password)
class UserResponse(UserBase):
    id: int
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
    user_id: Optional[int] = None
