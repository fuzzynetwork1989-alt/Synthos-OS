"""Document model"""

from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from synthos_database.session import Base


class Document(Base):
    """Document entity for ingested content"""

    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    owner_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    content_hash = Column(String, nullable=False, index=True)
    mime_type = Column(String)
    file_size = Column(Integer)
    source_uri = Column(String)
    access_classification = Column(String, default="private", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    metadata = Column(Text)

    # Relationships
    owner = relationship("User", back_populates="documents")
