import os
import sys

# Set Python path to backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.database import SessionLocal
from app.models import Email, Task, AIAction, EventDeadline

def deduplicate():
    db = SessionLocal()
    try:
        print("\n" + "="*70)
        print("  CLEANING UP AND DEDUPLICATING DATABASE RECORDS")
        print("="*70)

        # 1. Deduplicate AIActions per email
        actions = db.query(AIAction).order_by(AIAction.email_id, AIAction.id).all()
        seen_email_actions = set()
        deleted_actions = 0

        for a in actions:
            if a.email_id in seen_email_actions:
                db.delete(a)
                deleted_actions += 1
            else:
                seen_email_actions.add(a.email_id)

        db.commit()
        print(f"  Cleaned up {deleted_actions} duplicate AI Action rows.")

        # 2. Count current records
        email_count = db.query(Email).count()
        task_count = db.query(Task).count()
        action_count = db.query(AIAction).count()
        deadline_count = db.query(EventDeadline).count()

        print(f" • Total Clean Emails:    {email_count}")
        print(f" • Total Clean Tasks:     {task_count}")
        print(f" • Total Clean Actions:   {action_count}")
        print(f" • Total Clean Deadlines: {deadline_count}")
        print("="*70 + "\n")

    finally:
        db.close()

if __name__ == "__main__":
    deduplicate()
