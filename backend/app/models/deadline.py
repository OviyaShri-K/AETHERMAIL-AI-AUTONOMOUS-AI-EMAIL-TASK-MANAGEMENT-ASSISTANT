from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class EventDeadline(Base):
    __tablename__ = "deadlines_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    
    event_type = Column(String(50), default="deadline", nullable=False) # deadline, event, meeting, reminder
    raw_text = Column(String(255), nullable=False) # e.g. "tomorrow at 4:00 PM"
    normalized_datetime = Column(DateTime, nullable=True) # Normalized ISO-8601 timestamp
    description = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    email = relationship("Email", back_populates="deadlines")
    task = relationship("Task", back_populates="deadlines")
