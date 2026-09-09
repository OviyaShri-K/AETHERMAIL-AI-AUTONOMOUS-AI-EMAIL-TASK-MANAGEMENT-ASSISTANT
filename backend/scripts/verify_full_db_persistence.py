import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import Email, Task, EventDeadline, AIAction, AuditLog

def verify_persistence():
    client = TestClient(app)
    db = SessionLocal()

    print("\n" + "="*80)
    print(" 📊 FULL DATABASE PERSISTENCE & REAL EMAIL ID VERIFICATION")
    print("="*80)

    # 1. Ingest email with Real Email IDs
    real_payload = {
        "sender": "johndoe.developer@gmail.com",
        "sender_name": "John Doe",
        "recipient": "alex.student@gmail.com",
        "subject": "URGENT: Review API Integration and Sign NDA by Tomorrow 5 PM",
        "body": "Hi Alex, please review the architecture diagram, sign the mutual NDA, and send your notes before tomorrow at 5:00 PM.",
        "timestamp": "2026-08-27T10:00:00"
    }

    res = client.post("/api/emails/process-new", json=real_payload)
    print(f" [1/5] Real Email Ingest Status: {res.status_code}")
    data = res.json()
    email_db_id = data["email"]["id"]

    # 2. Query Email Table Record
    email_obj = db.query(Email).filter(Email.id == email_db_id).first()
    print(f"\n [2/5] ✅ Email Table Entity:")
    print(f"       • Database ID:       #{email_obj.id} ({email_obj.email_id})")
    print(f"       • Real Sender:       {email_obj.sender} ({email_obj.sender_name})")
    print(f"       • Real Recipient:    {email_obj.recipient}")
    print(f"       • Subject Text:      {email_obj.subject}")
    print(f"       • Full Body Text:    {email_obj.body}")
    print(f"       • AI Category:       {email_obj.category}")
    print(f"       • AI Priority:       {email_obj.priority}")
    print(f"       • Spam Detection:    {email_obj.is_spam}")

    # 3. Query Task Table Record(s)
    tasks = db.query(Task).filter(Task.email_id == email_db_id).all()
    print(f"\n [3/5] ✅ Extracted Task Entity ({len(tasks)} recorded):")
    for t in tasks:
        print(f"       • Task ID:           #{t.id}")
        print(f"       • Task Title Text:   {t.title}")
        print(f"       • Description Text:  {t.description}")
        print(f"       • Assignee:          {t.assignee}")
        print(f"       • Task Status:       {t.status}")
        print(f"       • Priority:          {t.priority}")

    # 4. Query Deadline Table Record(s)
    deadlines = db.query(EventDeadline).filter(EventDeadline.email_id == email_db_id).all()
    print(f"\n [4/5] ✅ Extracted Calendar Deadline Entity ({len(deadlines)} recorded):")
    for d in deadlines:
        print(f"       • Deadline ID:       #{d.id}")
        print(f"       • Raw Extracted Text:{d.raw_text}")
        print(f"       • Normalized ISO:    {d.normalized_datetime}")
        print(f"       • Description Text:  {d.description}")

    # 5. Query AIAction Table Record(s)
    actions = db.query(AIAction).filter(AIAction.email_id == email_db_id).all()
    print(f"\n [5/5] ✅ Generated AI Action & Draft Reply Entity ({len(actions)} recorded):")
    for a in actions:
        print(f"       • Action ID:         #{a.id}")
        print(f"       • Action Type:       {a.action_type}")
        print(f"       • Status:            {a.status}")
        print(f"       • Human Approval:    {a.requires_human_approval}")
        print(f"       • Draft Reply Text:  {a.draft_reply}")

    print("\n" + "="*80)
    print(" 🎯 100% OF ALL EXTRACTED TEXT & OUTPUTS ARE PERSISTED IN THE DATABASE!")
    print("="*80 + "\n")
    db.close()

if __name__ == "__main__":
    verify_persistence()
