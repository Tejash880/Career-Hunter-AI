"""
Application endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.application import Application
from app.schemas.application import ApplicationResponse, ApplicationCreate, ApplicationUpdate, ApplicationWithJob, ApplicationStats
from app.services.application_service import ApplicationService
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[ApplicationResponse])
def read_applications(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve current user's applications.
    """
    applications = ApplicationService.get_applications_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return applications


@router.post("/", response_model=ApplicationResponse)
def create_application(
    application_in: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new application.
    """
    try:
        application = ApplicationService.create_application(
            db=db, application_in=application_in, user_id=current_user.id
        )
        return application
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{application_id}", response_model=ApplicationWithJob)
def read_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get application by ID with job details.
    """
    application = ApplicationService.get_application(db=db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if user owns this application
    if application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get job details
    job = db.query(Application.Job).filter(Application.Job.id == application.job_id).first()
    
    # Convert to dict for response
    application_dict = ApplicationResponse.from_orm(application).dict()
    application_dict["job"] = job
    
    return application_dict


@router.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_in: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update application.
    """
    application = ApplicationService.get_application(db=db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if user owns this application
    if application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_application = ApplicationService.update_application(
        db=db, application_id=application_id, application_in=application_in
    )
    return updated_application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete application.
    """
    application = ApplicationService.get_application(db=db, application_id=application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if user owns this application
    if application.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = ApplicationService.delete_application(db=db, application_id=application_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete application")
    
    return {"message": "Application deleted successfully"}


@router.get("/me/stats", response_model=ApplicationStats)
def get_application_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's application statistics.
    """
    stats = ApplicationService.get_application_stats(db=db, user_id=current_user.id)
    return stats
