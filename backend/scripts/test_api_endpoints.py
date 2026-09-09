import os
import sys

# Set Python path to backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from app.main import app

def run_api_tests():
    client = TestClient(app)

    print("\n" + "="*75)
    print("  RUNNING FULL FASTAPI & CLOUDINARY REST API ENDPOINT TESTS")
    print("="*75)

    # 1. Health Endpoint
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    print(f" [PASS] GET  /api/health                     Status: {res_health.status_code} | {res_health.json()}")

    # 2. Get Emails with Strict Filters (is_spam=true)
    res_spam = client.get("/api/emails?is_spam=true")
    assert res_spam.status_code == 200
    spams = res_spam.json()
    assert all(e["is_spam"] == True for e in spams)
    print(f" [PASS] GET  /api/emails?is_spam=true        -> Found {len(spams)} spam emails (100% verified spam!)")

    # 3. Get Emails with Work + High Priority
    res_work_high = client.get("/api/emails?category=work&priority=high")
    assert res_work_high.status_code == 200
    work_emails = res_work_high.json()
    print(f" [PASS] GET  /api/emails?category=work&priority=high -> Found {len(work_emails)} high-priority work emails!")

    # 4. Get Email by Numeric ID (9) & verify draft_reply + Cloudinary attachment
    res_email_9 = client.get("/api/emails/9")
    assert res_email_9.status_code == 200
    e9 = res_email_9.json()
    assert e9.get("draft_reply") is not None
    assert len(e9.get("attachments", [])) > 0
    print(f" [PASS] GET  /api/emails/9                   Draft Reply: \"{e9['draft_reply'][:40]}...\" | Attachments: {len(e9['attachments'])}")

    # 5. Get Tasks with case-insensitive filters
    res_tasks = client.get("/api/tasks?status=Pending&priority=high")
    assert res_tasks.status_code == 200
    tasks = res_tasks.json()
    print(f" [PASS] GET  /api/tasks?status=Pending&priority=high -> Found {len(tasks)} tasks!")

    # 6. Cloudinary Status & File Upload Test
    res_cloud_status = client.get("/api/attachments/status")
    assert res_cloud_status.status_code == 200
    print(f" [PASS] GET  /api/attachments/status         Status: {res_cloud_status.status_code} | Provider: {res_cloud_status.json()['provider']}")

    # 7. Upload Attachment to Cloudinary
    file_payload = ("test_receipt.pdf", b"%PDF-1.4 Mock Receipt...", "application/pdf")
    res_upload = client.post("/api/attachments/upload", files={"file": file_payload}, data={"email_id": 1})
    assert res_upload.status_code == 200
    upload_data = res_upload.json()
    assert upload_data["success"] == True
    print(f" [PASS] POST /api/attachments/upload         Cloudinary URL: {upload_data['attachment']['cloudinary_url'][:45]}...")

    # 8. Get Dashboard Metrics
    res_metrics = client.get("/api/analytics/metrics")
    assert res_metrics.status_code == 200
    metrics = res_metrics.json()
    print(f" [PASS] GET  /api/analytics/metrics          Total Emails: {metrics['overview']['total_emails']} | Accuracy: {metrics['ai_benchmark_accuracy']['overall_accuracy']}%")

    print("="*75)
    print("  ALL FASTAPI & CLOUDINARY ENDPOINTS ARE 100% OPERATIONAL!")
    print("="*75 + "\n")

if __name__ == "__main__":
    run_api_tests()
