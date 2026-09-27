"""Workflow model"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from synthos_database.session import Base


class Workflow(Base):
    """Workflow entity for multi-step orchestration"""

    __tablename__ = "workflows"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    goal = Column(Text, nullable=False)
    state = Column(String, default="draft", nullable=False, index=True)
    approval_state = Column(String, default="none", nullable=False)
    steps = Column(Text)
    context = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime)
    metadata = Column(Text)

    # Relationships
    user = relationship("User", back_populates="workflows")
    tasks = relationship("Task", back_populates="workflow", cascade="all, delete-orphan")
