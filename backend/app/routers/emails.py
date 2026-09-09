from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from app.database import get_db
from app.models import Email, AIAction
from app.schemas.email_schemas import EmailResponse, EmailProcessRequest, EmailProcessResponse
from app.services.ai_inference_service import process_and_store_email

router = APIRouter(prefix="/api/emails", tags=["Emails"])

def ensure_draft_reply(email_obj: Email, db: Session) -> str:
    """Ensures every email has a high-quality, contextual draft reply."""
    for action in email_obj.actions:
        if action.draft_reply:
            return action.draft_reply

    sender_name = email_obj.sender_name or email_obj.sender.split("@")[0]
    subject = email_obj.subject
    cat = email_obj.category.lower()
    body_lower = email_obj.body.lower()

    if "invoice" in body_lower or "invoice" in subject.lower():
        draft = f"Hi {sender_name},\n\nThank you for providing the invoice regarding '{subject}'. I have received the attached document, verified the billing details, and submitted it for payment processing before the due date.\n\nBest regards,\nAlex"
    elif cat == "work":
        draft = f"Hi {sender_name.split()[0]},\n\nThank you for following up regarding '{subject}'. I have reviewed the details and will complete the necessary action items as requested.\n\nBest regards,\nAlex"
    elif cat == "personal":
        draft = f"Hi {sender_name.split()[0]},\n\nThanks for reaching out! Regarding '{subject}', that sounds great and I have added it to my schedule. Looking forward to it!\n\nBest,\nAlex"
    elif cat == "spam" or email_obj.is_spam:
        draft = "No reply needed. This message was flagged as unsolicited promotional or phishing content."
    elif cat == "notification":
        draft = f"Acknowledged automated notification regarding '{subject}'. Logged in system."
    else:
        draft = f"Hi {sender_name.split()[0]},\n\nThank you for reaching out regarding '{subject}'. I have received your email and will get back to you soon.\n\nBest,\nAlex"

    new_action = AIAction(
        email_id=email_obj.id,
        action_type="draft_reply" if not email_obj.is_spam else "archive_label",
        status="pending_approval" if email_obj.is_actionable else "executed",
        requires_human_approval=email_obj.is_actionable,
        draft_reply=draft
    )
    db.add(new_action)
    db.commit()
    db.refresh(email_obj)
    return draft

def format_email_response(email_obj: Email, db: Session) -> EmailResponse:
    """Formats an Email ORM object into an EmailResponse with populated draft_reply."""
    draft = ensure_draft_reply(email_obj, db)
    res = EmailResponse.model_validate(email_obj)
    res.draft_reply = draft
    return res

@router.get("", response_model=List[EmailResponse])
def get_emails(
    user_email: Optional[str] = Query(None, description="Filter by user email ID / recipient (e.g. sarah.jenkins@techcorp.io)"),
    category: Optional[str] = Query(None, description="Filter by category (work, personal, promotional, notification, spam)"),
    is_spam: Optional[bool] = Query(None, description="Filter spam status: true (only spam) or false (only non-spam)"),
    priority: Optional[str] = Query(None, description="Filter by priority: High, Medium, Low"),
    db: Session = Depends(get_db)
):
    """
    Retrieve emails with strict, case-insensitive multi-user filters.
    If `user_email` is provided, fetches only emails for that specific mail ID.
    """
    query = db.query(Email)
    
    # 1. Multi-User Email Filter
    if user_email and user_email.strip():
        u_clean = user_email.strip().lower()
        if u_clean not in ["all", "*"]:
            query = query.filter(
                or_(
                    func.lower(Email.recipient) == u_clean,
                    func.lower(Email.sender) == u_clean
                )
            )

    # 2. Spam Filter (Strict Boolean Match)
    if is_spam is not None:
        query = query.filter(Email.is_spam == is_spam)

    # 3. Category Filter (Case-Insensitive)
    if category and category.strip():
        cat_clean = category.strip().lower()
        if cat_clean in ["spam", "phishing"]:
            query = query.filter(Email.is_spam == True)
        elif cat_clean not in ["all", "*"]:
            query = query.filter(func.lower(Email.category) == cat_clean)
        
    # 4. Priority Filter (Case-Insensitive)
    if priority and priority.strip():
        prio_clean = priority.strip().lower()
        if prio_clean not in ["all", "*"]:
            query = query.filter(func.lower(Email.priority) == prio_clean)
        
    emails = query.order_by(Email.timestamp.desc(), Email.id.desc()).all()
    
    # Deduplicate in Python to guarantee 0 repeated emails
    seen_ids = set()
    unique_emails = []
    for e in emails:
        if e.id not in seen_ids:
            seen_ids.add(e.id)
            unique_emails.append(format_email_response(e, db))
            
    return unique_emails

@router.get("/{email_id}", response_model=EmailResponse)
def get_email_by_id(email_id: str, db: Session = Depends(get_db)):
    """
    Retrieve a single email by its database integer ID (e.g. 1) or string ID (e.g. email_001).
    Guarantees a complete draft reply and Cloudinary attachments are returned.
    """
    email_obj = None
    
    if email_id.isdigit():
        email_obj = db.query(Email).filter(Email.id == int(email_id)).first()
        
    if not email_obj:
        email_obj = db.query(Email).filter(Email.email_id == email_id).first()
        
    if not email_obj:
        raise HTTPException(status_code=404, detail=f"Email with ID '{email_id}' not found.")
        
    return format_email_response(email_obj, db)

@router.post("/process-new", response_model=EmailProcessResponse)
def process_new_email(payload: EmailProcessRequest, db: Session = Depends(get_db)):
    """
    Ingests any new raw email for ANY mail ID, runs it through the AI agent pipeline,
    extracts tasks and deadlines, scores priority, and saves to database.
    """
    email_obj, ai_output = process_and_store_email(
        db=db,
        sender=payload.sender,
        sender_name=payload.sender_name,
        recipient=payload.recipient or os.getenv("GMAIL_USER", "alex.miller@innovatetech.io"),
        subject=payload.subject,
        body=payload.body,
        timestamp_str=payload.timestamp
    )
    
    formatted_email = format_email_response(email_obj, db)
    summary = f"Processed email '{payload.subject}' for {email_obj.recipient}. Category: {ai_output['category']}, Tasks Extracted: {len(ai_output.get('tasks', []))}, Priority: {ai_output['priority']}"
    
    return EmailProcessResponse(
        success=True,
        email=formatted_email,
        ai_decision_summary=summary
    )
