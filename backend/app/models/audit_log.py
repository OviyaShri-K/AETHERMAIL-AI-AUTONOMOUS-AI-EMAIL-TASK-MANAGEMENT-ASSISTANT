from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    entity_type = Column(String(50), nullable=False) # EMAIL, TASK, ACTION, APPROVAL
    entity_id = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False) # CREATED, UPDATED, APPROVED, REJECTED, EXECUTED
    performed_by = Column(String(50), default="AI_AGENT", nullable=False) # AI_AGENT, USER
    details = Column(Text, nullable=True) # JSON or descriptive string
    
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
