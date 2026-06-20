"""
Resume model.
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class Resume(BaseModel):
    """Resume model."""
    __tablename__ = "resumes"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    version = Column(String(50), nullable=False)  # e.g., "v1.0", "v2.1"
    content = Column(Text)  # Full resume text
    ats_score = Column(Integer, default=0)  # ATS compatibility score
    missing_keywords = Column(JSON)  # List of missing keywords
    suggestions = Column(JSON)  # Improvement suggestions
    file_url = Column(String(255))  # URL to stored resume file (PDF/DOCX)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for archived

    # Relationships
    user = relationship("User", back_populates="resumes")