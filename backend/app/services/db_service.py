import json
import os
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Email, Task, EventDeadline, AIAction, AuditLog

def seed_benchmark_dataset(db: Session, json_path: str):
    """
    Seeds the PostgreSQL database with the single unified benchmark dataset.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Benchmark JSON not found at: {json_path}")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    inserted_count = 0
    for item in data:
        existing = db.query(Email).filter(Email.email_id == item["email_id"]).first()
        if existing:
            continue

        gt = item["ground_truth"]
        
        try:
            ts = datetime.fromisoformat(item["timestamp"])
        except Exception:
            ts = datetime.utcnow()

        # 1. Create Email
        email_obj = Email(
            email_id=item["email_id"],
            timestamp=ts,
            sender=item["sender"],
            sender_name=item.get("sender_name", ""),
            recipient=item.get("recipient", "sarah.jenkins@techcorp.io"),
            subject=item["subject"],
            body=item["body"],
            is_spam=gt["is_spam"],
            category=gt["category"],
            importance=gt["importance"],
            is_actionable=gt["is_actionable"],
            priority=gt["priority"]
        )
        db.add(email_obj)
        db.flush()

        # 2. Create Tasks
        created_task_ids = []
        for t in gt.get("tasks", []):
            task_obj = Task(
                email_id=email_obj.id,
                title=t["title"],
                description=t.get("description", ""),
                assignee=t.get("assignee", "sarah.jenkins@techcorp.io"),
                status=t.get("status", "pending"),
                priority=gt["priority"]
            )
            db.add(task_obj)
            db.flush()
            created_task_ids.append(task_obj.id)

        # 3. Create Deadlines & Events
        for d in gt.get("events_deadlines", []):
            norm_dt = None
            if d.get("normalized_datetime"):
                try:
                    norm_dt = datetime.fromisoformat(d["normalized_datetime"])
                except Exception:
                    norm_dt = None

            deadline_obj = EventDeadline(
                email_id=email_obj.id,
                task_id=created_task_ids[0] if created_task_ids else None,
                event_type=d.get("type", "deadline"),
                raw_text=d.get("raw_text", ""),
                normalized_datetime=norm_dt,
                description=d.get("description", "")
            )
            db.add(deadline_obj)

        # 4. Create AI Actions
        rec_action = gt.get("recommended_action", {})
        action_obj = AIAction(
            email_id=email_obj.id,
            action_type=rec_action.get("action_type", "none"),
            status="pending_approval" if rec_action.get("requires_human_approval") else "executed",
            requires_human_approval=rec_action.get("requires_human_approval", False),
            draft_reply=rec_action.get("draft_reply", None),
            executed_at=datetime.utcnow() if not rec_action.get("requires_human_approval") else None
        )
        db.add(action_obj)

        # 5. Create Audit Log
        audit_obj = AuditLog(
            entity_type="EMAIL",
            entity_id=item["email_id"],
            action="INGESTED_AND_ANALYZED",
            performed_by="AI_AGENT",
            details=f"Classified as {gt['category']}, Priority: {gt['priority']}, Tasks: {len(gt.get('tasks', []))}"
        )
        db.add(audit_obj)
        inserted_count += 1

    db.commit()
    return inserted_count

def seed_database_if_empty(db: Session):
    """Auto-seeds database if emails table is empty."""
    current_count = db.query(Email).count()
    if current_count == 0:
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        json_path = os.path.join(backend_dir, "..", "dataset", "email_unified_benchmark.json")
        if not os.path.exists(json_path):
            json_path = os.path.join(backend_dir, "dataset", "email_unified_benchmark.json")
        if not os.path.exists(json_path):
            json_path = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset\email_unified_benchmark.json"
            
        if os.path.exists(json_path):
            seed_benchmark_dataset(db, json_path)
            print(f" Database successfully seeded with benchmark data from: {json_path}")
