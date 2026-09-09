import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.database import SessionLocal
from app.models import Email, Task, EventDeadline, AIAction, Attachment

def view_database(user_email=None):
    db = SessionLocal()
    
    print("\n" + "="*95)
    print(" 🗄️  POSTGRESQL DATABASE RECORDS VIEWER")
    print("="*95)

    email_query = db.query(Email)
    if user_email and user_email.strip():
        u = user_email.strip().lower()
        email_query = email_query.filter((Email.recipient == u) | (Email.sender == u))

    emails = email_query.order_by(Email.id.desc()).all()
    print(f"\n📬 1. 'emails' Table ({len(emails)} records found):")
    print(f"{'ID':<5} | {'Recipient':<26} | {'Category':<10} | {'Priority':<8} | {'Subject'}")
    print("-" * 95)
    for e in emails[:15]:
        subj = (e.subject[:40] + "...") if len(e.subject) > 40 else e.subject
        rec = (e.recipient[:24] + "..") if len(e.recipient) > 24 else e.recipient
        print(f"#{e.id:<4} | {rec:<26} | {e.category:<10} | {e.priority:<8} | {subj}")

    tasks = db.query(Task).order_by(Task.id.desc()).all()
    print(f"\n📋 2. 'tasks' Table ({len(tasks)} records found):")
    print(f"{'ID':<5} | {'Email ID':<8} | {'Status':<12} | {'Assignee':<24} | {'Task Title'}")
    print("-" * 95)
    for t in tasks[:15]:
        tit = (t.title[:38] + "...") if len(t.title) > 38 else t.title
        ass = (t.assignee[:22] + "..") if len(t.assignee) > 22 else t.assignee
        print(f"#{t.id:<4} | #{t.email_id:<7} | {t.status:<12} | {ass:<24} | {tit}")

    actions = db.query(AIAction).order_by(AIAction.id.desc()).all()
    print(f"\n🛡️  3. 'ai_actions' Table ({len(actions)} records found):")
    print(f"{'ID':<5} | {'Email ID':<8} | {'Status':<18} | {'Action Type':<24} | {'Draft Reply Preview'}")
    print("-" * 95)
    for a in actions[:10]:
        draft = (a.draft_reply[:35] + "...") if a.draft_reply else "None"
        draft = draft.replace("\n", " ")
        print(f"#{a.id:<4} | #{a.email_id:<7} | {a.status:<18} | {a.action_type:<24} | {draft}")

    deadlines = db.query(EventDeadline).order_by(EventDeadline.id.desc()).all()
    print(f"\n⏰ 4. 'deadlines_events' Table ({len(deadlines)} records found):")
    print(f"{'ID':<5} | {'Email ID':<8} | {'Normalized Datetime':<20} | {'Raw Extracted Text'}")
    print("-" * 95)
    for d in deadlines[:10]:
        norm = str(d.normalized_datetime) if d.normalized_datetime else "N/A"
        print(f"#{d.id:<4} | #{d.email_id:<7} | {norm:<20} | {d.raw_text}")

    print("\n" + "="*95)
    print(" 🎯 ALL RECORDS ARE STORED DIRECTLY IN YOUR POSTGRESQL DATABASE!")
    print("="*95 + "\n")
    db.close()

if __name__ == "__main__":
    filter_email = sys.argv[1] if len(sys.argv) > 1 else None
    view_database(filter_email)
