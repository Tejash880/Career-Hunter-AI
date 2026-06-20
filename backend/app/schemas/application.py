"""
Application schemas.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    job_id: int
    resume_version_used: Optional[str] = None
    notes: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None


class ApplicationInDBBase(BaseModel):
    id: int
    user_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    resume_version_used: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ApplicationResponse(ApplicationInDBBase):
    pass


class ApplicationWithJob(ApplicationResponse):
    job: dict  # Will be populated with JobResponse


class ApplicationStats(BaseModel):
    total_applications: int
    oa_received: int
    interviews_scheduled: int
    offers_received: int
    acceptances: int
    oa_conversion_rate: float
    offer_rate: float