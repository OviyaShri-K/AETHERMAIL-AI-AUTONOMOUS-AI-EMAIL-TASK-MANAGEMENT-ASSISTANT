import os
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

from app.database import engine, Base, SessionLocal
import app.models
from app.models import Email, Task, EventDeadline, AIAction, Attachment, AuditLog
from app.services.db_service import seed_database_if_empty

def setup_postgres():
    print("\n" + "="*80)
    print(" 🚀 INITIALIZING LOCAL POSTGRESQL TABLES & DATA")
    print("="*80)
    
    print("Creating all tables in PostgreSQL (emails, tasks, deadlines_events, ai_actions, attachments, audit_logs)...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

    db = SessionLocal()
    seed_database_if_empty(db)
    
    # Ensure all records have user email
    target_email = "sarah.jenkins@techcorp.io"
    db.query(Email).update({Email.recipient: target_email})
    db.query(Task).update({Task.assignee: target_email})
    db.commit()
    
    total_emails = db.query(Email).count()
    print(f"✅ Local PostgreSQL Database Ready with {total_emails} records for '{target_email}'!")
    print("="*80 + "\n")
    db.close()

if __name__ == "__main__":
    setup_postgres()
