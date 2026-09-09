import os
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

from app.database import SessionLocal
from app.models import Email, Task

def update_all_to_user():
    db = SessionLocal()
    target_email = "sarah.jenkins@techcorp.io"
    
    # 1. Update all emails
    updated_emails = db.query(Email).update({Email.recipient: target_email})
    
    # 2. Update all tasks
    updated_tasks = db.query(Task).update({Task.assignee: target_email})
    
    db.commit()
    print(f"Successfully updated {updated_emails} emails and {updated_tasks} tasks to recipient/assignee: '{target_email}'!")
    db.close()

if __name__ == "__main__":
    update_all_to_user()
