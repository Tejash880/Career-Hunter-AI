"""
User endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.core.security import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user.
    """
    if user_in.first_name is not None:
        current_user.first_name = user_in.first_name
    if user_in.last_name is not None:
        current_user.last_name = user_in.last_name
    if user_in.linkedin_url is not None:
        current_user.linkedin_url = user_in.linkedin_url
    if user_in.github_url is not None:
        current_user.github_url = user_in.github_url
    if user_in.avatar_url is not None:
        current_user.avatar_url = user_in.avatar_url
    if user_in.bio is not None:
        current_user.bio = user_in.bio
    if user_in.is_active is not None:
        current_user.is_active = user_in.is_active

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if user == current_user:
        return user
    # In a real app, you might want to restrict this or show limited info
    return user