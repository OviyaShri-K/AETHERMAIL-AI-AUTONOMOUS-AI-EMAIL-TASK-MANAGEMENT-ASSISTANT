from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email_id = Column(Integer, ForeignKey("emails.id", ondelete="CASCADE"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True)
    
    filename = Column(String(255), nullable=False)
    file_type = Column(String(100), default="application/octet-stream", nullable=False) # e.g. application/pdf, image/png
    file_size_bytes = Column(Integer, default=0, nullable=False)
    
    # Cloudinary Cloud Asset Details
    cloudinary_url = Column(String(1000), nullable=False) # Secure CDN URL
    cloudinary_public_id = Column(String(255), nullable=False) # Asset ID for management/deletion
    
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    email = relationship("Email", back_populates="attachments")
    task = relationship("Task", back_populates="attachments")
