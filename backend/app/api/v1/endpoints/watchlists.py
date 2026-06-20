"""
Watchlist endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.watchlist import Watchlist
from app.schemas.watchlist import WatchlistResponse, WatchlistCreate, WatchlistUpdate, WatchlistWithJobs
from app.services.watchlist_service import WatchlistService
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[WatchlistResponse])
def read_watchlists(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve current user's watchlists.
    """
    watchlists = WatchlistService.get_watchlists_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return watchlists


@router.post("/", response_model=WatchlistResponse)
def create_watchlist(
    watchlist_in: WatchlistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new watchlist.
    """
    try:
        watchlist = WatchlistService.create_watchlist(
            db=db, watchlist_in=watchlist_in, user_id=current_user.id
        )
        return watchlist
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{watchlist_id}", response_model=WatchlistWithJobs)
def read_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get watchlist by ID with associated jobs.
    """
    watchlist = WatchlistService.get_watchlist(db=db, watchlist_id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Check if user owns this watchlist
    if watchlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Get jobs for this watchlist
    jobs = WatchlistService.get_watchlist_jobs(
        db=db, watchlist_id=watchlist_id
    )
    
    # Convert to dict for response
    watchlist_dict = WatchlistResponse.from_orm(watchlist).dict()
    watchlist_dict["jobs"] = jobs
    
    return watchlist_dict


@router.put("/{watchlist_id}", response_model=WatchlistResponse)
def update_watchlist(
    watchlist_id: int,
    watchlist_in: WatchlistUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update watchlist.
    """
    watchlist = WatchlistService.get_watchlist(db=db, watchlist_id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Check if user owns this watchlist
    if watchlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_watchlist = WatchlistService.update_watchlist(
        db=db, watchlist_id=watchlist_id, watchlist_in=watchlist_in
    )
    return updated_watchlist


@router.delete("/{watchlist_id}")
def delete_watchlist(
    watchlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete watchlist.
    """
    watchlist = WatchlistService.get_watchlist(db=db, watchlist_id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Check if user owns this watchlist
    if watchlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = WatchlistService.delete_watchlist(db=db, watchlist_id=watchlist_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete watchlist")
    
    return {"message": "Watchlist deleted successfully"}


@router.get("/{watchlist_id}/jobs", response_model=List[dict])
def get_watchlist_jobs(
    watchlist_id: int,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Get jobs from companies in a watchlist.
    """
    watchlist = WatchlistService.get_watchlist(db=db, watchlist_id=watchlist_id)
    if not watchlist:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    
    # Check if user owns this watchlist
    if watchlist.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    jobs = WatchlistService.get_watchlist_jobs(
        db=db, watchlist_id=watchlist_id, skip=skip, limit=limit
    )
    return jobs
