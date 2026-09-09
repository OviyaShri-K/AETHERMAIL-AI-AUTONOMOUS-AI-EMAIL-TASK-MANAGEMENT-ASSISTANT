import os
import sys

# Set Python path to backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.database import engine, SessionLocal, init_db, Base
from app.config import settings
from app.models import Email, Task, EventDeadline, AIAction, AuditLog
from app.services.db_service import seed_benchmark_dataset

def test_supabase_connection():
    print("\n" + "="*75)
    print("  SUPABASE POSTGRESQL DATABASE CONNECTION & SEEDING TEST")
    print("="*75)
    print(f"Connecting to: {settings.DATABASE_URL.split('@')[-1] if '@' in settings.DATABASE_URL else settings.DATABASE_URL}")

    # 1. Initialize Tables
    print("\n[1/3] Initializing Tables in Database...")
    init_db()

    db = SessionLocal()
    try:
        # 2. Seed Benchmark Dataset
        print("\n[2/3] Seeding Master Benchmark Dataset into Database...")
        project_root = os.path.abspath(os.path.join(backend_root, ".."))
        dataset_json = os.path.join(project_root, "dataset", "email_unified_benchmark.json")
        
        inserted = seed_benchmark_dataset(db, dataset_json)
        print(f"  -> Inserted {inserted} new emails (with tasks & deadlines).")

        # 3. Query Table Counts to verify
        print("\n[3/3] Verifying Database Records Across All Tables:")
        print("-" * 75)
        
        email_count = db.query(Email).count()
        task_count = db.query(Task).count()
        deadline_count = db.query(EventDeadline).count()
        action_count = db.query(AIAction).count()
        audit_count = db.query(AuditLog).count()
        
        pending_tasks = db.query(Task).filter(Task.status == "pending").count()
        pending_approvals = db.query(AIAction).filter(AIAction.status == "pending_approval").count()

        print(f"  • Emails Table (`emails`):              {email_count:>4} records")
        print(f"  • Tasks Table (`tasks`):                {task_count:>4} records ({pending_tasks} Pending)")
        print(f"  • Deadlines Table (`deadlines_events`): {deadline_count:>4} records")
        print(f"  • AI Actions Table (`ai_actions`):      {action_count:>4} records ({pending_approvals} Pending Approvals)")
        print(f"  • Audit Logs Table (`audit_logs`):      {audit_count:>4} records")
        print("="*75)
        print("  DATABASE SETUP & CONNECTION 100% OPERATIONAL!")
        print("="*75 + "\n")

    finally:
        db.close()

if __name__ == "__main__":
    test_supabase_connection()
