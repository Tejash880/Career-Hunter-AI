"""
Job schemas.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.job import JobType, ExperienceLevel, RemoteType


class JobBase(BaseModel):
    title: str
    department: Optional[str] = None
    location: Optional[str] = None
    remote_type: Optional[RemoteType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = "USD"
    experience_level: Optional[ExperienceLevel] = None
    employment_type: Optional[JobType] = None
    skills_required: Optional[List[str]] = None
    skills_preferred: Optional[List[str]] = None
    application_url: Optional[str] = None
    posting_date: Optional[datetime] = None
    job_description: Optional[str] = None


class JobCreate(JobBase):
    company_id: int
    ats_source: str


class JobUpdate(BaseModel):
    title: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    remote_type: Optional[RemoteType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None
    employment_type: Optional[JobType] = None
    skills_required: Optional[List[str]] = None
    skills_preferred: Optional[List[str]] = None
    application_url: Optional[str] = None
    posting_date: Optional[datetime] = None
    job_description: Optional[str] = None
    is_active: Optional[bool] = None


class JobInDBBase(JobBase):
    id: int
    company_id: int
    last_updated: datetime
    ats_source: str
    is_active: bool
    match_score: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class JobResponse(JobInDBBase):
    pass


class JobSearchParams(BaseModel):
    query: Optional[str] = None
    location: Optional[str] = None
    remote_type: Optional[RemoteType] = None
    experience_level: Optional[ExperienceLevel] = None
    employment_type: Optional[JobType] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    skills: Optional[List[str]] = None
    company_ids: Optional[List[int]] = None
    limit: int = 20
    offset: int = 0