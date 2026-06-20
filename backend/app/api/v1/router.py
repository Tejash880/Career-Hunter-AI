"""
API v1 router.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, jobs, applications, resumes, watchlists, notifications

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(watchlists.router, prefix="/watchlists", tags=["watchlists"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])