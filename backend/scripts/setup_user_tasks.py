import os
import sys

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

from app.database import SessionLocal
from app.models import Email, Task, EventDeadline, AIAction, AuditLog
from app.services.ai_inference_service import process_and_store_email

def setup_tasks_for_user(target_email="developer@aethermail.ai"):
    print("\n" + "="*85)
    print(f" 🎯 CONFIGURING & MANAGING TASKS FOR: {target_email}")
    print("="*85)

    db = SessionLocal()
    
    # 1. Update existing database records
    updated_emails = db.query(Email).update({Email.recipient: target_email})
    updated_tasks = db.query(Task).update({Task.assignee: target_email})
    db.commit()
    print(f"\n[1/4] Updated {updated_emails} emails and {updated_tasks} tasks to assignee '{target_email}'.")

    # 2. Ingest 3 specific high-priority actionable emails for developer@aethermail.ai
    print("\n[2/4] Ingesting New Real-World Academic & Work Emails with AI Task Extraction...")
    sample_emails = [
        {
            "sender": "engineering.lead@techcorp.io",
            "sender_name": "Dr. K. Sathish (Project Guide)",
            "subject": "URGENT: Submit Final AI Project Architecture & Swagger API Specs by Tomorrow 4 PM",
            "body": f"Dear Candidate ({target_email}), please verify all FastAPI endpoints, verify database tables in pgAdmin, and submit the complete project documentation before tomorrow at 4:00 PM.",
            "timestamp": "2026-08-31T10:00:00"
        },
        {
            "sender": "exam.controller@enterprise.ai",
            "sender_name": "Office of Controller of Examinations",
            "subject": "Notification: Project Viva Voce Examination Schedule Verification",
            "body": f"Dear Student ({target_email}), verify your project repository, ensure Cloudinary attachments and ML models are loaded, and confirm your attendance for the upcoming review viva.",
            "timestamp": "2026-08-31T11:30:00"
        },
        {
            "sender": "recruiter@tcs-careers.com",
            "sender_name": "TCS Campus Hiring",
            "subject": "Action Required: Complete Technical Assessment and Coding Round by Friday 6 PM",
            "body": f"Hi ({target_email}), you have been shortlisted for the Advanced AI Engineer role. Please complete the coding assessment before Friday at 6:00 PM.",
            "timestamp": "2026-08-31T14:00:00"
        }
    ]

    for em in sample_emails:
        existing = db.query(Email).filter(Email.subject == em["subject"], Email.recipient == target_email).first()
        if not existing:
            process_and_store_email(
                db=db,
                sender=em["sender"],
                sender_name=em["sender_name"],
                recipient=target_email,
                subject=em["subject"],
                body=em["body"],
                timestamp_str=em["timestamp"]
            )
            print(f"  ✅ Ingested: '{em['subject'][:55]}...'")

    # 3. Retrieve and Manage Tasks for developer@aethermail.ai
    print(f"\n[3/4] Current Active Tasks for {target_email}:")
    tasks = db.query(Task).filter(Task.assignee == target_email).order_by(Task.id.desc()).all()
    print(f"{'Task ID':<8} | {'Status':<14} | {'Priority':<10} | {'Task Title'}")
    print("-" * 85)
    for t in tasks[:10]:
        print(f"#{t.id:<7} | {t.status:<14} | {t.priority:<10} | {t.title[:45]}")

    # 4. Demonstrate Task Management Status Transitions
    if tasks:
        # Move first task to in_progress
        t1 = tasks[0]
        t1.status = "in_progress"
        # Move second task to completed
        if len(tasks) > 1:
            t2 = tasks[1]
            t2.status = "completed"
        db.commit()
        print(f"\n[4/4] Task Status Updates Applied:")
        print(f"  ✅ Task #{t1.id} -> Status moved to 'in_progress'")
        if len(tasks) > 1:
            print(f"  ✅ Task #{t2.id} -> Status moved to 'completed'")

    print("\n" + "="*85)
    print(f" 🎉 ALL TASKS ARE CONFIGURED & FULLY MANAGED FOR '{target_email}'!")
    print("="*85 + "\n")
    db.close()

if __name__ == "__main__":
    setup_tasks_for_user()
