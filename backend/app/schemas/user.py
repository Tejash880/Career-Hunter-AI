"""
User schemas.
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserInDB(UserInDBBase):
    hashed_password: str


class UserResponse(UserInDBBase):
    pass


class UserWithToken(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[int] = None