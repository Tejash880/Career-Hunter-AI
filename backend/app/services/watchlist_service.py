"""
Watchlist service layer.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistCreate, WatchlistUpdate
from app.models.company import Company
from app.models.job import Job


class WatchlistService:
    @staticmethod
    def get_watchlist(db: Session, watchlist_id: int) -> Optional[Watchlist]:
        return db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()

    @staticmethod
    def get_watchlists_by_user(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Watchlist]:
        return (
            db.query(Watchlist)
            .filter(Watchlist.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_watchlist(db: Session, watchlist_in: WatchlistCreate, user_id: int) -> Watchlist:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        watchlist_data = watchlist_in.dict()
        watchlist_data["user_id"] = user_id
        watchlist = Watchlist(**watchlist_data)
        db.add(watchlist)
        db.commit()
        db.refresh(watchlist)
        return watchlist

    @staticmethod
    def update_watchlist(
        db: Session, 
        watchlist_id: int, 
        watchlist_in: WatchlistUpdate
    ) -> Optional[Watchlist]:
        watchlist = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
        if not watchlist:
            return None
        
        update_data = watchlist_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(watchlist, field, value)
        
        db.add(watchlist)
        db.commit()
        db.refresh(watchlist)
        return watchlist

    @staticmethod
    def delete_watchlist(db: Session, watchlist_id: int) -> bool:
        watchlist = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
        if not watchlist:
            return False
        
        db.delete(watchlist)
        db.commit()
        return True

    @staticmethod
    def get_watchlist_jobs(
        db: Session, 
        watchlist_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Job]:
        """
        Get jobs from companies in a watchlist.
        """
        watchlist = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
        if not watchlist:
            return []
        
        # Get company IDs from watchlist
        company_ids = watchlist.company_ids or []
        
        # Get jobs from those companies
        jobs = (
            db.query(Job)
            .filter(Job.company_id.in_(company_ids))
            .filter(Job.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        return jobs
