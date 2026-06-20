"""
Watchlist schemas.
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime


class WatchlistBase(BaseModel):
    name: str
    description: Optional[str] = None
    company_ids: Optional[List[int]] = None
    location_filter: Optional[str] = None
    role_filter: Optional[str] = None
    is_active: Optional[int] = None


class WatchlistCreate(WatchlistBase):
    pass


class WatchlistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    company_ids: Optional[List[int]] = None
    location_filter: Optional[str] = None
    role_filter: Optional[str] = None
    is_active: Optional[int] = None


class WatchlistInDBBase(WatchlistBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class WatchlistResponse(WatchlistInDBBase):
    pass


class WatchlistWithJobs(WatchlistResponse):
    jobs: List[dict] = []  # Will be populated with JobResponse
