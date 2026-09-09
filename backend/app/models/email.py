from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_id = Column(String(100), unique=True, index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    sender = Column(String(255), index=True, nullable=False)
    sender_name = Column(String(255), nullable=True)
    recipient = Column(String(255), default="user@company.com", nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    
    # AI Classification & Source Attributes
    source = Column(String(50), default="LIVE_GMAIL", nullable=False) # 'LIVE_GMAIL' vs 'BENCHMARK_DATASET'
    is_spam = Column(Boolean, default=False, nullable=False)
    category = Column(String(50), default="work", nullable=False)
    importance = Column(String(50), default="medium", nullable=False)
    is_actionable = Column(Boolean, default=False, nullable=False)
    priority = Column(String(50), default="Medium", nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="email", cascade="all, delete-orphan")
    deadlines = relationship("EventDeadline", back_populates="email", cascade="all, delete-orphan")
    actions = relationship("AIAction", back_populates="email", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="email", cascade="all, delete-orphan")
