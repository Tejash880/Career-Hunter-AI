"""
Resume schemas.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class ResumeBase(BaseModel):
    version: str
    content: str
    file_url: Optional[str] = None


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    version: Optional[str] = None
    content: Optional[str] = None
    file_url: Optional[str] = None
    is_active: Optional[int] = None


class ResumeInDBBase(ResumeBase):
    id: int
    user_id: int
    ats_score: int
    missing_keywords: Optional[List[str]] = None
    suggestions: Optional[List[Dict[str, Any]]] = None
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ResumeResponse(ResumeInDBBase):
    pass


class ResumeAnalysisRequest(BaseModel):
    resume_content: str
    job_description: str


class ResumeAnalysisResponse(BaseModel):
    ats_score: int
    missing_keywords: List[str]
    suggestions: List[Dict[str, Any]]
    optimized_content: str