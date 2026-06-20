"""
Company model.
"""
from sqlalchemy import Column, String, Text, Integer, JSON, Boolean
from sqlalchemy.orm import relationship
from .base import BaseModel


class Company(BaseModel):
    """Company model."""
    __tablename__ = "companies"

    name = Column(String(255), unique=True, index=True, nullable=False)
    careers_url = Column(String(255))
    ats_type = Column(String(50))  # workday, greenhouse, lever, etc.
    tech_stack = Column(JSON)      # List of technologies used
    hiring_frequency = Column(String(50))  # e.g., "weekly", "monthly"
    is_active = Column(Boolean, default=True)
    description = Column(Text)
    logo_url = Column(String(255))
    website_url = Column(String(255))

    # Relationships
    jobs = relationship("Job", back_populates="company")