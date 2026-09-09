from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import AIAction, Email, AuditLog
from app.schemas.task_schemas import ActionResponse, ApprovalDecisionRequest, ApprovalsListResponse
from app.services.gmail_service import send_approved_email_reply

router = APIRouter(prefix="/api/approvals", tags=["Human-in-the-Loop Approvals"])

def format_action_response(action: AIAction, db: Session) -> ActionResponse:
    """Enriches an AIAction with parent email context and ensures draft reply."""
    email = db.query(Email).filter(Email.id == action.email_id).first()
    
    draft = action.draft_reply
    if not draft and email:
        sender_first = (email.sender_name or email.sender.split("@")[0]).split()[0]
        if email.category == "work":
            draft = f"Hi {sender_first},\n\nThank you for following up regarding '{email.subject}'. I have reviewed the details and will complete the necessary action items as requested.\n\nBest regards,\nAlex"
        elif email.category == "personal":
            draft = f"Hi {sender_first},\n\nThanks for reaching out! Sounds great regarding '{email.subject}', and I have added it to my schedule.\n\nBest,\nAlex"
        else:
            draft = f"Hi {sender_first},\n\nThank you for your email regarding '{email.subject}'. I have received it and will follow up shortly.\n\nBest,\nAlex"
        action.draft_reply = draft
        db.commit()

    return ActionResponse(
        id=action.id,
        email_id=action.email_id,
        email_subject=email.subject if email else "N/A",
        sender=email.sender if email else "N/A",
        category=email.category if email else "N/A",
        action_type=action.action_type,
        status=action.status,
        requires_human_approval=action.requires_human_approval,
        draft_reply=draft,
        created_at=action.created_at,
        executed_at=action.executed_at
    )

@router.get("", response_model=ApprovalsListResponse)
def get_pending_approvals(
    user_email: Optional[str] = Query(None, description="Filter approvals for a specific user email ID (e.g. sarah.jenkins@techcorp.io)"),
    status: Optional[str] = Query(None, description="Filter status: 'pending_approval' (or 'pending'), 'approved', 'rejected', 'executed', or leave blank for ALL"),
    db: Session = Depends(get_db)
):
    """
    Retrieve AI actions along with the exact count for the selected status filter and multi-user email filter.
    """
    query = db.query(AIAction)
    
    # 1. Multi-User Filter
    if user_email and user_email.strip():
        u_clean = user_email.strip().lower()
        if u_clean not in ["all", "*"]:
            query = query.join(Email, AIAction.email_id == Email.id).filter(
                or_(
                    func.lower(Email.recipient) == u_clean,
                    func.lower(Email.sender) == u_clean
                )
            )

    total_db_count = query.count()
    active_filter_label = "all"
    
    if status and status.strip():
        s = status.strip().lower()
        if s not in ["all", "*"]:
            if s in ["pending", "pending_approval", "pending approval"]:
                active_filter_label = "pending_approval"
                query = query.filter(func.lower(AIAction.status) == "pending_approval")
            elif s in ["approved", "approve"]:
                active_filter_label = "approved"
                query = query.filter(func.lower(AIAction.status) == "approved")
            elif s in ["rejected", "reject"]:
                active_filter_label = "rejected"
                query = query.filter(func.lower(AIAction.status) == "rejected")
            elif s in ["executed", "done"]:
                active_filter_label = "executed"
                query = query.filter(func.lower(AIAction.status) == "executed")
            else:
                active_filter_label = s
                query = query.filter(func.lower(AIAction.status) == s)
                
    actions = query.order_by(AIAction.created_at.desc(), AIAction.id.desc()).all()
    formatted_actions = [format_action_response(a, db) for a in actions]

    return ApprovalsListResponse(
        status_filter=active_filter_label,
        count=len(formatted_actions),
        total_in_db=total_db_count,
        actions=formatted_actions
    )

@router.post("/{action_id}/decide", response_model=ActionResponse)
def decide_approval(action_id: int, payload: ApprovalDecisionRequest, db: Session = Depends(get_db)):
    """
    Decide on an AI Action.
    Provide ONLY your decision in the request:
    {"decision": "approve"} or {"decision": "reject"}.
    On approval, automatically executes the reply and delivers it to recipient.
    """
    action_obj = db.query(AIAction).filter(AIAction.id == action_id).first()
    if not action_obj:
        raise HTTPException(status_code=404, detail=f"AI Action #{action_id} not found")

    decision = payload.decision.lower().strip()
    if decision not in ["approve", "approved", "reject", "rejected"]:
        raise HTTPException(status_code=400, detail="Decision must be 'approve' or 'reject'")

    format_action_response(action_obj, db)

    if decision in ["approve", "approved"]:
        # Execute reply delivery and update status
        send_approved_email_reply(db=db, action_id=action_id)
        action_obj.status = "approved"
        action_obj.executed_at = datetime.utcnow()
            
        audit = AuditLog(
            entity_type="ACTION",
            entity_id=str(action_id),
            action="APPROVED_AND_EXECUTED",
            performed_by="USER",
            details=f"User approved AI action '{action_obj.action_type}'"
        )
        db.add(audit)
    else:
        action_obj.status = "rejected"
        audit = AuditLog(
            entity_type="ACTION",
            entity_id=str(action_id),
            action="REJECTED",
            performed_by="USER",
            details=f"User rejected AI action '{action_obj.action_type}'"
        )
        db.add(audit)

    db.commit()
    db.refresh(action_obj)
    return format_action_response(action_obj, db)
