"""
Job model.
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean, JSON, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class JobType(str, enum.Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"


class ExperienceLevel(str, enum.Enum):
    INTERN = "intern"
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    EXECUTIVE = "executive"


class RemoteType(str, enum.Enum):
    ONSITE = "onsite"
    REMOTE = "remote"
    HYBRID = "hybrid"


class Job(BaseModel):
    """Job model."""
    __tablename__ = "jobs"

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String(255), nullable=False)
    department = Column(String(100))
    location = Column(String(255))
    remote_type = Column(Enum(RemoteType))
    salary_min = Column(Integer)  # in USD per year
    salary_max = Column(Integer)  # in USD per year
    currency = Column(String(10), default="USD")
    experience_level = Column(Enum(ExperienceLevel))
    employment_type = Column(Enum(JobType))
    skills_required = Column(JSON)  # List of required skills
    skills_preferred = Column(JSON)  # List of preferred skills
    application_url = Column(String(500))  # Direct company application URL
    posting_date = Column(DateTime)
    last_updated = Column(DateTime)
    ats_source = Column(String(50))  # workday, greenhouse, etc.
    job_description = Column(Text)
    is_active = Column(Boolean, default=True)
    match_score = Column(Integer, default=0)  # Computed match score for users

    # Relationships
    company = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job")