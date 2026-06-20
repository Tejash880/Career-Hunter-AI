"""
Notification service layer.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification, NotificationType, NotificationStatus
from app.schemas.notification import NotificationCreate, NotificationUpdate
from app.models.user import User


class NotificationService:
    @staticmethod
    def get_notification(db: Session, notification_id: int) -> Optional[Notification]:
        return db.query(Notification).filter(Notification.id == notification_id).first()

    @staticmethod
    def get_notifications_by_user(
        db: Session, 
        user_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Notification]:
        return (
            db.query(Notification)
            .filter(Notification.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create_notification(db: Session, notification_in: NotificationCreate, user_id: int) -> Notification:
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        notification_data = notification_in.dict()
        notification_data["user_id"] = user_id
        notification = Notification(**notification_data)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def update_notification(
        db: Session, 
        notification_id: int, 
        notification_in: NotificationUpdate
    ) -> Optional[Notification]:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return None
        
        update_data = notification_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(notification, field, value)
        
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def delete_notification(db: Session, notification_id: int) -> bool:
        notification = db.query(Notification).filter(Notification.id == notification_id).first()
        if not notification:
            return False
        
        db.delete(notification)
        db.commit()
        return True

    @staticmethod
    def send_notification(
        db: Session,
        user_id: int,
        notification_type: NotificationType,
        content: str
    ) -> Notification:
        """
        Send a notification to a user.
        In a real implementation, this would integrate with email/SMS/push providers.
        """
        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")
        
        notification_data = {
            "user_id": user_id,
            "type": notification_type,
            "content": content,
            "status": NotificationStatus.PENDING
        }
        
        notification = Notification(**notification_data)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        
        # Here you would integrate with actual notification providers
        # For now, we'll just mark as sent
        notification.status = NotificationStatus.SENT
        # In reality, you'd have actual provider logic here
        # notification.provider_message_id = "msg_12345"  # Example
        
        db.add(notification)
        db.commit()
        return notification
