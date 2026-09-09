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
from app.models import Email, Attachment
from app.services.cloudinary_service import upload_file_bytes

def seed_email_attachments():
    db = SessionLocal()
    try:
        print("\n" + "="*70)
        print(" 📎 SEEDING SAMPLE CLOUDINARY ATTACHMENTS TO EMAILS")
        print("="*70)

        # 1. Attach Invoice PDF to Email #9 (CloudServices Billing)
        email_9 = db.query(Email).filter(Email.email_id == "email_009").first()
        if email_9:
            # Check if attachment already exists
            existing = db.query(Attachment).filter(Attachment.email_id == email_9.id).first()
            if not existing:
                res_inv = upload_file_bytes(
                    file_bytes=b"%PDF-1.4 Invoice INV-2026-881 Amount: $3450.00 Due: Sept 2",
                    filename="Invoice_INV_2026_881.pdf",
                    folder="ai_email_assistant/invoices"
                )
                att_inv = Attachment(
                    email_id=email_9.id,
                    filename="Invoice_INV_2026_881.pdf",
                    file_type="application/pdf",
                    file_size_bytes=res_inv["file_size_bytes"],
                    cloudinary_url=res_inv["cloudinary_url"],
                    cloudinary_public_id=res_inv["cloudinary_public_id"]
                )
                db.add(att_inv)
                print(f" [ATTACHED] Invoice_INV_2026_881.pdf -> Email #9 ({email_9.subject[:35]}...)")

        # 2. Attach Architecture Diagram PNG to Email #2 (David Ross API Integration)
        email_2 = db.query(Email).filter(Email.email_id == "email_002").first()
        if email_2:
            existing = db.query(Attachment).filter(Attachment.email_id == email_2.id).first()
            if not existing:
                res_diag = upload_file_bytes(
                    file_bytes=b"\x89PNG\r\n\x1a\n Mock API Architecture Diagram",
                    filename="Webhook_Timeout_Trace_Log.png",
                    folder="ai_email_assistant/traces"
                )
                att_diag = Attachment(
                    email_id=email_2.id,
                    filename="Webhook_Timeout_Trace_Log.png",
                    file_type="image/png",
                    file_size_bytes=res_diag["file_size_bytes"],
                    cloudinary_url=res_diag["cloudinary_url"],
                    cloudinary_public_id=res_diag["cloudinary_public_id"]
                )
                db.add(att_diag)
                print(f" [ATTACHED] Webhook_Timeout_Trace_Log.png -> Email #2 ({email_2.subject[:35]}...)")

        db.commit()
        print("="*70)
        print("  CLOUDINARY ATTACHMENTS LINKED TO EMAILS SUCCESSFULLY!")
        print("="*70 + "\n")

    finally:
        db.close()

if __name__ == "__main__":
    seed_email_attachments()
