from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AIAction(Base):
    __tablename__ = "ai_actions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=False)
    
    action_type = Column(String(100), default="none", nullable=False) # create_task_and_reminder, archive_label, escalate, draft_reply
    status = Column(String(50), default="pending_approval", nullable=False) # pending_approval, approved, rejected, executed
    requires_human_approval = Column(Boolean, default=False, nullable=False)
    draft_reply = Column(Text, nullable=True) # Pre-generated reply
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    executed_at = Column(DateTime, nullable=True)

    # Relationships
    email = relationship("Email", back_populates="actions")
