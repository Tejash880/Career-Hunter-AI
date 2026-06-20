"""
Notification model.
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum


class NotificationType(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Notification(BaseModel):
    """Notification model."""
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(Enum(NotificationType), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.PENDING)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime)
    provider_message_id = Column(String(255))  # ID from email/SMS provider

    # Relationships
    user = relationship("User")