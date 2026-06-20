"""
User model.
"""
from sqlalchemy import Boolean, Column, String, Text, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class User(BaseModel):
    """User model."""
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    linkedin_url = Column(String(255))
    github_url = Column(String(255))
    avatar_url = Column(String(255))
    bio = Column(Text)

    # Resume information
    resume_url = Column(String(255))  # URL to stored resume file
    resume_content = Column(Text)     # Parsed resume text

    # Preferences stored as JSON
    preferences = Column(JSON, default={})

    # Relationships
    applications = relationship("Application", back_populates="user")
    watchlists = relationship("Watchlist", back_populates="user")
    resumes = relationship("Resume", back_populates="user")