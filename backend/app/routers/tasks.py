from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Task, Email, EventDeadline, AuditLog
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

def format_task_response(task: Task, db: Session) -> TaskResponse:
    """Enriches a Task ORM object with its linked deadline."""
    deadline_str = None
    deadline_obj = db.query(EventDeadline).filter(
        or_(EventDeadline.task_id == task.id, EventDeadline.email_id == task.email_id)
    ).first()
    
    if deadline_obj:
        if deadline_obj.normalized_datetime:
            deadline_str = deadline_obj.normalized_datetime.isoformat()
        else:
            deadline_str = deadline_obj.raw_text
    else:
        desc_lower = (task.description or "").lower()
        if "tomorrow" in desc_lower:
            deadline_str = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%dT16:00:00")
        elif "hour" in desc_lower:
            deadline_str = (datetime.utcnow() + timedelta(hours=4)).strftime("%Y-%m-%dT%H:00:00")
        else:
            deadline_str = (task.created_at + timedelta(days=2)).strftime("%Y-%m-%dT17:00:00")

    return TaskResponse(
        id=task.id,
        email_id=task.email_id,
        title=task.title,
        description=task.description,
        assignee=task.assignee,
        status=task.status,
        priority=task.priority,
        deadline=deadline_str,
        created_at=task.created_at,
        updated_at=task.updated_at
    )

def normalize_status_filter(status: str) -> Optional[str]:
    s = status.strip().lower()
    if s in ["all", "*", ""]:
        return None
    if s in ["in_progress", "in progress", "inprogress", "in-progress", "progress", "active"]:
        return "in_progress"
    if s in ["completed", "done", "finished", "complete"]:
        return "completed"
    if s in ["pending", "todo", "to_do", "to-do", "open"]:
        return "pending"
    return s

def normalize_priority_filter(priority: str) -> Optional[str]:
    p = priority.strip().lower()
    if p in ["all", "*", ""]:
        return None
    if p in ["high", "hi", "urgent", "p0", "p1"]:
        return "high"
    if p in ["medium", "med", "mid", "normal", "p2"]:
        return "medium"
    if p in ["low", "lo", "minor", "p3"]:
        return "low"
    return p

@router.get("", response_model=List[TaskResponse])
def get_tasks(
    user_email: Optional[str] = Query(None, description="Filter tasks for a specific user email ID (e.g. sarah.jenkins@techcorp.io)"),
    status: Optional[str] = Query(None, description="Filter by status: 'pending', 'in_progress', 'completed' (or leave blank for ALL)"),
    priority: Optional[str] = Query(None, description="Filter by priority: 'High', 'Medium', 'Low' (or leave blank for ALL)"),
    db: Session = Depends(get_db)
):
    """
    Retrieve tasks with multi-user filtering, case-insensitive status and priority matching.
    """
    query = db.query(Task)
    
    # 1. Multi-User Filter
    if user_email and user_email.strip():
        u_clean = user_email.strip().lower()
        if u_clean not in ["all", "*"]:
            # Match directly on assignee or parent email recipient
            query = query.join(Email, Task.email_id == Email.id, isouter=True).filter(
                or_(
                    func.lower(Task.assignee) == u_clean,
                    func.lower(Email.recipient) == u_clean,
                    func.lower(Email.sender) == u_clean
                )
            )

    # 2. Status Filter
    if status and status.strip():
        norm_status = normalize_status_filter(status)
        if norm_status:
            query = query.filter(func.lower(Task.status) == norm_status)
        
    # 3. Priority Filter
    if priority and priority.strip():
        norm_prio = normalize_priority_filter(priority)
        if norm_prio:
            query = query.filter(func.lower(Task.priority) == norm_prio)
        
    tasks = query.order_by(Task.created_at.desc(), Task.id.desc()).all()
    
    seen_ids = set()
    unique_tasks = []
    for t in tasks:
        if t.id not in seen_ids:
            seen_ids.add(t.id)
            unique_tasks.append(format_task_response(t, db))
            
    return unique_tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by ID with its deadline."""
    task_obj = db.query(Task).filter(Task.id == task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    return format_task_response(task_obj, db)

@router.post("", response_model=TaskResponse)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task with email_id, description, and optional recipient mail ID.
    """
    email_obj = None
    if payload.email_id:
        email_obj = db.query(Email).filter(Email.id == payload.email_id).first()
        
    if not email_obj:
        email_obj = db.query(Email).first()
    
    email_id = email_obj.id if email_obj else 1
    assignee = payload.recipient or (email_obj.recipient if email_obj else os.getenv("GMAIL_USER", "alex.miller@innovatetech.io"))
    
    desc_clean = payload.description.strip()
    title = desc_clean.split("\n")[0][:60]
    if len(desc_clean) > 60:
        title += "..."

    task_obj = Task(
        email_id=email_id,
        title=title,
        description=desc_clean,
        assignee=assignee,
        status="pending",
        priority=email_obj.priority if email_obj else "Medium"
    )
    db.add(task_obj)
    db.flush()

    # Determine deadline
    desc_lower = desc_clean.lower()
    if "tomorrow" in desc_lower:
        norm_dt = datetime.utcnow() + timedelta(days=1)
        raw_text = "Tomorrow at 4:00 PM"
    elif "hour" in desc_lower:
        norm_dt = datetime.utcnow() + timedelta(hours=4)
        raw_text = "In 4 hours"
    else:
        norm_dt = datetime.utcnow() + timedelta(days=2)
        raw_text = "In 2 days"

    deadline_obj = EventDeadline(
        email_id=email_id,
        task_id=task_obj.id,
        event_type="deadline",
        raw_text=raw_text,
        normalized_datetime=norm_dt,
        description=f"Due date for: {title}"
    )
    db.add(deadline_obj)

    audit = AuditLog(
        entity_type="TASK",
        entity_id=str(task_obj.id),
        action="CREATED_MANUALLY",
        performed_by="USER",
        details=f"Created task '{title}' for {assignee}"
    )
    db.add(audit)
    db.commit()
    db.refresh(task_obj)
    
    return format_task_response(task_obj, db)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, payload: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update task status, priority, or details.
    """
    task_obj = db.query(Task).filter(Task.id == task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    old_status = task_obj.status
    if payload.title is not None:
        task_obj.title = payload.title
    if payload.description is not None:
        task_obj.description = payload.description
    if payload.assignee is not None:
        task_obj.assignee = payload.assignee
    if payload.status is not None:
        st = payload.status.lower().strip()
        if st in ["in progress", "inprogress", "in-progress"]:
            st = "in_progress"
        task_obj.status = st
    if payload.priority is not None:
        task_obj.priority = payload.priority.capitalize()

    task_obj.updated_at = datetime.utcnow()

    if payload.status and payload.status != old_status:
        audit = AuditLog(
            entity_type="TASK",
            entity_id=str(task_id),
            action="STATUS_UPDATED",
            performed_by="USER",
            details=f"Status changed from {old_status} to {task_obj.status}"
        )
        db.add(audit)

    db.commit()
    db.refresh(task_obj)
    return format_task_response(task_obj, db)

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task by ID."""
    task_obj = db.query(Task).filter(Task.id == task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()
    return {"success": True, "message": f"Task {task_id} deleted successfully"}
