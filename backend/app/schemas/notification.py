"""
Notification schemas.
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.notification import NotificationType, NotificationStatus


class NotificationBase(BaseModel):
    type: NotificationType
    content: str


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    status: Optional[NotificationStatus] = None


class NotificationInDBBase(NotificationBase):
    id: int
    user_id: int
    status: NotificationStatus
    sent_at: Optional[datetime] = None
    provider_message_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class NotificationResponse(NotificationInDBBase):
    pass
