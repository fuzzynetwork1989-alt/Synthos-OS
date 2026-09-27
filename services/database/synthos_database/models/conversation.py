"""Conversation model"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from synthos_database.session import Base


class Conversation(Base):
    """Conversation entity for user interactions"""

    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow(), nullable=False)
    metadata = Column(Text)

    # Relationships
    user = relationship("User", back_populates="conversations")
