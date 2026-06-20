"""
Application model.
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class ApplicationStatus(str, enum.Enum):
    APPLIED = "applied"
    OA_RECEIVED = "oa_received"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    REJECTED = "rejected"
    OFFER_RECEIVED = "offer_received"
    ACCEPTED = "accepted"


class Application(BaseModel):
    """Application model."""
    __tablename__ = "applications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED)
    applied_at = Column(DateTime, nullable=False)
    resume_version_used = Column(String(100))  # Reference to which resume version was used
    notes = Column(Text)

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")