"""
Job endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobResponse, JobCreate, JobUpdate, JobSearchParams
from app.services.job_service import JobService
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[JobResponse])
def read_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = Query(default=20, lte=100),
    query: Optional[str] = None,
    location: Optional[str] = None,
    remote_type: Optional[str] = None,
    experience_level: Optional[str] = None,
    employment_type: Optional[str] = None,
    salary_min: Optional[int] = None,
    salary_max: Optional[int] = None,
    company_ids: Optional[str] = None,  # Comma-separated string
    skills: Optional[str] = None,  # Comma-separated string
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve jobs with optional filtering.
    """
    # Parse comma-separated query parameters
    company_ids_list = [int(id.strip()) for id in company_ids.split(",")] if company_ids else None
    skills_list = [skill.strip() for skill in skills.split(",")] if skills else None
    
    search_params = JobSearchParams(
        query=query,
        location=location,
        remote_type=remote_type,
        experience_level=experience_level,
        employment_type=employment_type,
        salary_min=salary_min,
        salary_max=salary_max,
        company_ids=company_ids_list,
        skills=skills_list,
        limit=limit,
        offset=skip
    )
    
    jobs = JobService.get_jobs(db, skip=skip, limit=limit, search_params=search_params)
    return jobs


@router.post("/", response_model=JobResponse)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new job.
    """
    job = JobService.create_job(db=db, job_in=job_in)
    return job


@router.get("/{job_id}", response_model=JobResponse)
def read_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get job by ID.
    """
    job = JobService.get_job(db=db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update job.
    """
    job = JobService.update_job(db=db, job_id=job_id, job_in=job_in)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete job.
    """
    success = JobService.delete_job(db=db, job_id=job_id)
    if not success:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"message": "Job deleted successfully"}


@router.get("/{job_id}/match/{user_id}")
def get_job_match_score(
    job_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get match score between a job and a user.
    """
    # Users can only check their own match scores
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    job = JobService.get_job(db=db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Extract user skills from preferences or resume
    user_skills = []
    if user.preferences and "skills" in user.preferences:
        user_skills = user.preferences["skills"]
    
    # For now, use a placeholder experience level
    user_experience = "mid"  # This should come from user profile
    
    match_score = JobService.calculate_match_score(
        db=db,
        job=job,
        user_skills=user_skills,
        user_experience=user_experience
    )
    
    # Update job's match score for this user (optional)
    job.match_score = match_score
    db.add(job)
    db.commit()
    
    return {"job_id": job_id, "user_id": user_id, "match_score": match_score}
