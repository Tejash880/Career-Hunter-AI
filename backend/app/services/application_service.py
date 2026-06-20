"""
Application service layer.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.application import Application, ApplicationStatus
from app.schemas.application import ApplicationCreate, ApplicationUpdate
from app.models.job import Job
from app.models.user import User


class ApplicationService:
    @staticmethod
    def get_application(db: Session, application_id: int) -> Optional[Application]:
        return db.query(Application).filter(Application.id == application_id).first()

    @staticmethod
    def get_applications_by_user(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Application]:
        return (
            db.query(Application)
            .filter(Application.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_applications_by_job(
        db: Session, 
        job_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Application]:
        return (
            db.query(Application)
            .filter(Application.job_id == job_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_application(db: Session, application_in: ApplicationCreate, user_id: int) -> Application:
        # Verify job exists
        job = db.query(Job).filter(Job.id == application_in.job_id).first()
        if not job:
            raise ValueError("Job not found")
        
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        application_data = application_in.dict()
        application_data["user_id"] = user_id
        application = Application(**application_data)
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def update_application(
        db: Session, 
        application_id: int, 
        application_in: ApplicationUpdate
    ) -> Optional[Application]:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            return None
        
        update_data = application_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(application, field, value)
        
        db.add(application)
        db.commit()
        db.refresh(application)
        return application

    @staticmethod
    def delete_application(db: Session, application_id: int) -> bool:
        application = db.query(Application).filter(Application.id == application_id).first()
        if not application:
            return False
        
        db.delete(application)
        db.commit()
        return True

    @staticmethod
    def get_application_stats(db: Session, user_id: int) -> dict:
        """
        Get application statistics for a user.
        """
        applications = db.query(Application).filter(Application.user_id == user_id).all()
        
        total = len(applications)
        oa_received = len([a for a in applications if a.status == ApplicationStatus.OA_RECEIVED])
        interviews_scheduled = len([a for a in applications if a.status == ApplicationStatus.INTERVIEW_SCHEDULED])
        offers_received = len([a for a in applications if a.status == ApplicationStatus.OFFER_RECEIVED])
        acceptances = len([a for a in applications if a.status == ApplicationStatus.ACCEPTED])
        
        oa_conversion_rate = (oa_received / total * 100) if total > 0 else 0
        offer_rate = (offers_received / total * 100) if total > 0 else 0
        
        return {
            "total_applications": total,
            "oa_received": oa_received,
            "interviews_scheduled": interviews_scheduled,
            "offers_received": offers_received,
            "acceptances": acceptances,
            "oa_conversion_rate": round(oa_conversion_rate, 2),
            "offer_rate": round(offer_rate, 2)
        }
