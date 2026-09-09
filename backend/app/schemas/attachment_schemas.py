from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AttachmentResponse(BaseModel):
    id: int
    email_id: Optional[int] = None
    task_id: Optional[int] = None
    filename: str
    file_type: str
    file_size_bytes: int
    cloudinary_url: str
    cloudinary_public_id: str
    uploaded_at: datetime

    class Config:
        from_attributes = True

class AttachmentUploadResponse(BaseModel):
    success: bool
    message: str
    attachment: AttachmentResponse
