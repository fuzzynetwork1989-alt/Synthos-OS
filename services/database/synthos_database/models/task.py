"""Task model"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from synthos_database.session import Base


class Task(Base):
    """Task entity for workflow execution"""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    workflow_id = Column(String, ForeignKey("workflows.id"), nullable=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default="pending", nullable=False, index=True)
    layer = Column(String)
    priority = Column(Integer, default=0)
    result = Column(Text)
    error = Column(Text)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    created_at = Column(DateTime, default=lambda: datetime.utcnow(), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.utcnow(), onupdate=lambda: datetime.utcnow(), nullable=False)
    metadata = Column(Text)

    # Relationships
    user = relationship("User", back_populates="tasks")
    workflow = relationship("Workflow", back_populates="tasks", backref="workflow_tasks")
