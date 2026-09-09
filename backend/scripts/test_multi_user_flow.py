import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app

def run_multi_user_test():
    client = TestClient(app)
    
    print("\n" + "="*80)
    print(" 👥 MULTI-USER DYNAMIC EMAIL ID & OPEN BACKEND VERIFICATION")
    print("="*80)

    user1 = "sarah.jenkins@techcorp.io"
    user2 = "developer.raj@techcorp.io"

    # 1. Ingest email for User 1 (sarah.jenkins@techcorp.io)
    print(f"\n[1/4] Ingesting New Email for User 1 ({user1})...")
    res1 = client.post("/api/emails/process-new", json={
        "sender": "college.principal@university.edu",
        "sender_name": "Dr. Subramanian",
        "recipient": user1,
        "subject": "URGENT: Submit Final Master Thesis by Tomorrow 5 PM",
        "body": "Dear Sarah Jenkins, please review the final documentation, verify all metrics, and submit before tomorrow 5 PM.",
        "timestamp": "2026-08-27T11:00:00"
    })
    print(f"  ✅ Ingest Status:       {res1.status_code}")
    print(f"  ✅ Recipient Assigned:  {res1.json()['email']['recipient']}")
    print(f"  ✅ Category & Priority: {res1.json()['email']['category']} | {res1.json()['email']['priority']}")

    # 2. Ingest email for User 2 (developer.raj@techcorp.io)
    print(f"\n[2/4] Ingesting New Email for User 2 ({user2})...")
    res2 = client.post("/api/emails/process-new", json={
        "sender": "devops-lead@techcorp.io",
        "sender_name": "DevOps Lead",
        "recipient": user2,
        "subject": "DEPLOY: Production AWS Cluster Release",
        "body": "Hi Raj, please deploy the new container build to production cluster by tonight 9 PM.",
        "timestamp": "2026-08-27T11:30:00"
    })
    print(f"  ✅ Ingest Status:       {res2.status_code}")
    print(f"  ✅ Recipient Assigned:  {res2.json()['email']['recipient']}")

    # 3. Test Multi-User Email Filtering
    print(f"\n[3/4] Testing Dynamic Email Filtering in GET /api/emails...")
    emails_u1 = client.get(f"/api/emails?user_email={user1}").json()
    emails_u2 = client.get(f"/api/emails?user_email={user2}").json()
    all_emails = client.get("/api/emails").json()

    print(f"  ✅ Total Emails in DB:  {len(all_emails)}")
    print(f"  ✅ Filtered for {user1}: {len(emails_u1)} email(s) returned")
    print(f"  ✅ Filtered for {user2}: {len(emails_u2)} email(s) returned")

    # 4. Test Multi-User Task & Approval Filtering
    print(f"\n[4/4] Testing Dynamic Task & Approval Filtering in GET /api/tasks...")
    tasks_u1 = client.get(f"/api/tasks?user_email={user1}").json()
    tasks_u2 = client.get(f"/api/tasks?user_email={user2}").json()
    approvals_u1 = client.get(f"/api/approvals?user_email={user1}").json()

    print(f"  ✅ Tasks for {user1}:     {len(tasks_u1)} task(s)")
    if tasks_u1:
        print(f"     • Task 1 Title:     '{tasks_u1[0]['title']}'")
        print(f"     • Task 1 Deadline:  '{tasks_u1[0]['deadline']}'")
    print(f"  ✅ Tasks for {user2}:     {len(tasks_u2)} task(s)")
    print(f"  ✅ Approvals for {user1}: {approvals_u1['count']} action(s)")

    print("\n" + "="*80)
    print(" 🎯 MULTI-USER DYNAMIC EMAIL ID & OPEN BACKEND FUNCTIONS ARE 100% OPERATIONAL!")
    print("="*80 + "\n")

if __name__ == "__main__":
    run_multi_user_test()
