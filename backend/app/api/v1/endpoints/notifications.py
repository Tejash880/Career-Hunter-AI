"""
Notification endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.notification import Notification
from app.schemas.notification import NotificationResponse, NotificationCreate, NotificationUpdate
from app.services.notification_service import NotificationService
from app.core.security import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=List[NotificationResponse])
def read_notifications(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve current user's notifications.
    """
    notifications = NotificationService.get_notifications_by_user(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return notifications


@router.post("/", response_model=NotificationResponse)
def create_notification(
    notification_in: NotificationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create new notification.
    """
    try:
        notification = NotificationService.create_notification(
            db=db, notification_in=notification_in, user_id=current_user.id
        )
        return notification
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{notification_id}", response_model=NotificationResponse)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get notification by ID.
    """
    notification = NotificationService.get_notification(db=db, notification_id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Check if user owns this notification
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return notification


@router.put("/{notification_id}", response_model=NotificationResponse)
def update_notification(
    notification_id: int,
    notification_in: NotificationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update notification.
    """
    notification = NotificationService.get_notification(db=db, notification_id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Check if user owns this notification
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    updated_notification = NotificationService.update_notification(
        db=db, notification_id=notification_id, notification_in=notification_in
    )
    return updated_notification


@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete notification.
    """
    notification = NotificationService.get_notification(db=db, notification_id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    # Check if user owns this notification
    if notification.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    success = NotificationService.delete_notification(db=db, notification_id=notification_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete notification")
    
    return {"message": "Notification deleted successfully"}


@router.post("/send")
def send_notification(
    notification_type: str,
    content: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send a notification to the current user.
    """
    try:
        # Convert string to enum
        notification_type_enum = NotificationType(notification_type)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid notification type")
    
    notification = NotificationService.send_notification(
        db=db,
        user_id=current_user.id,
        notification_type=notification_type_enum,
        content=content
    )
    
    return {"message": "Notification sent successfully", "notification_id": notification.id}
