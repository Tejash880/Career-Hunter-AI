"""
Resume endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.resume import Resume
from app.schemas.resume import ResumeResponse, ResumeCreate, ResumeUpdate, ResumeAnalysisRequest, ResumeAnalysisResponse
from app.services.resume_service import ResumeService
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ResumeResponse])
def read_resumes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve current user's resumes.
    """
    resumes = ResumeService.get_resumes_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return resumes


@router.post("/", response_model=ResumeResponse)
def create_resume(
    resume_in: ResumeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new resume.
    """
    try:
        resume = ResumeService.create_resume(
            db=db, resume_in=resume_in, user_id=current_user.id
        )
        return resume
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{resume_id}", response_model=ResumeResponse)
def read_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get resume by ID.
    """
    resume = ResumeService.get_resume(db=db, resume_id=resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user owns this resume
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return resume


@router.put("/{resume_id}", response_model=ResumeResponse)
def update_resume(
    resume_id: int,
    resume_in: ResumeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update resume.
    """
    resume = ResumeService.get_resume(db=db, resume_id=resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user owns this resume
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_resume = ResumeService.update_resume(
        db=db, resume_id=resume_id, resume_in=resume_in
    )
    return updated_resume


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete resume.
    """
    resume = ResumeService.get_resume(db=db, resume_id=resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check if user owns this resume
    if resume.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = ResumeService.delete_resume(db=db, resume_id=resume_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete resume")
    
    return {"message": "Resume deleted successfully"}


@router.post("/analyze", response_model=ResumeAnalysisResponse)
def analyze_resume(
    analysis_request: ResumeAnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Analyze resume against job description.
    """
    analysis = ResumeService.analyze_resume(
        db=db, analysis_request=analysis_request
    )
    return analysis
