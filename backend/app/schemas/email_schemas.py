from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TaskSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    assignee: str = "user"
    status: str = "pending"
    priority: str = "Medium"
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class DeadlineSchema(BaseModel):
    id: Optional[int] = None
    event_type: str = "deadline"
    raw_text: str
    normalized_datetime: Optional[datetime] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class ActionSchema(BaseModel):
    id: Optional[int] = None
    action_type: str
    status: str = "pending_approval"
    requires_human_approval: bool = False
    draft_reply: Optional[str] = None

    class Config:
        from_attributes = True

class AttachmentSchema(BaseModel):
    id: Optional[int] = None
    filename: str
    file_type: str
    file_size_bytes: int
    cloudinary_url: str
    cloudinary_public_id: str
    uploaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EmailResponse(BaseModel):
    id: int
    email_id: str
    timestamp: datetime
    sender: str
    sender_name: Optional[str] = None
    recipient: str
    subject: str
    body: str
    is_spam: bool
    category: str
    importance: str
    is_actionable: bool
    priority: str
    draft_reply: Optional[str] = None
    created_at: datetime
    tasks: List[TaskSchema] = []
    deadlines: List[DeadlineSchema] = []
    actions: List[ActionSchema] = []
    attachments: List[AttachmentSchema] = []

    class Config:
        from_attributes = True

class EmailProcessRequest(BaseModel):
    sender: str = Field(..., example="sarah.jenkins@techcorp.io")
    sender_name: Optional[str] = Field("Sarah Jenkins", example="Sarah Jenkins")
    recipient: str = Field("alex.dev@techcorp.io", example="alex.dev@techcorp.io", description="Recipient email address")
    subject: str = Field(..., example="URGENT: Q3 Financial Report Review by Tomorrow 4 PM")
    body: str = Field(..., example="Hi Alex, please review slides 12-25, verify EBITDA figures, and send notes before 4 PM tomorrow.")
    timestamp: Optional[str] = Field(None, example="2026-08-25T09:00:00")

class EmailProcessResponse(BaseModel):
    success: bool
    email: EmailResponse
    ai_decision_summary: str

    class Config:
        from_attributes = True
