"""
Watchlist model.
"""
from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel


class Watchlist(BaseModel):
    """Watchlist model."""
    __tablename__ = "watchlists"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    company_ids = Column(JSON)  # List of company IDs
    location_filter = Column(String(255))
    role_filter = Column(String(255))
    is_active = Column(Integer, default=1)  # 1 for active, 0 for archived

    # Relationships
    user = relationship("User", back_populates="watchlists")