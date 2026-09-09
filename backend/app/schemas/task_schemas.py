from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class TaskCreate(BaseModel):
    email_id: Optional[int] = Field(1, description="Associated Email ID (e.g. 1, 2, 9)", example=1)
    recipient: Optional[str] = Field(None, description="User mail ID / Assignee", example="sarah.jenkins@techcorp.io")
    description: str = Field(..., description="Task instructions or description", example="Review Q3 financial numbers, check EBITDA figures, and update slides before tomorrow 4 PM")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee: Optional[str] = None
    status: Optional[str] = None # pending, in_progress, completed, cancelled
    priority: Optional[str] = None # High, Medium, Low

class TaskResponse(BaseModel):
    id: int
    email_id: int
    title: str
    description: Optional[str] = None
    assignee: str
    status: str
    priority: str
    deadline: Optional[str] = Field(None, description="Extracted ISO-8601 deadline date and time", example="2026-08-28T16:00:00")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ApprovalDecisionRequest(BaseModel):
    decision: str = Field("approve", description="Provide only your decision: 'approve' or 'reject'")

class ActionResponse(BaseModel):
    id: int
    email_id: int
    email_subject: Optional[str] = None
    sender: Optional[str] = None
    category: Optional[str] = None
    action_type: str
    status: str
    requires_human_approval: bool
    draft_reply: Optional[str] = None
    created_at: datetime
    executed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ApprovalsListResponse(BaseModel):
    status_filter: str = Field("all", description="Current status filter applied")
    count: int = Field(..., description="Count of actions matching the selected status filter")
    total_in_db: int = Field(..., description="Total actions in database across all statuses")
    actions: List[ActionResponse] = Field(..., description="List of action records")

    class Config:
        from_attributes = True
