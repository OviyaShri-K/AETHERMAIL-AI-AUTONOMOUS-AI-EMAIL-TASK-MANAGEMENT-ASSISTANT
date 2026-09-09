import os
from typing import Optional
from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import UserAccount, Email
from app.services.gmail_service import sync_user_live_inbox

scheduler = BackgroundScheduler()

def scheduled_email_sync_job():
    """Background autonomous task that polls for new incoming emails periodically across all accounts."""
    db = SessionLocal()
    try:
        # Collect target user emails to sync
        target_accounts = []
        
        # 1. Accounts in database
        db_accounts = db.query(UserAccount).filter(UserAccount.is_active == True).all()
        for acc in db_accounts:
            target_accounts.append((acc.email, acc.app_password))

        # 2. System environment user if not already in list
        env_user = os.getenv("GMAIL_USER")
        if env_user and not any(a[0].lower() == env_user.lower() for a in target_accounts):
            target_accounts.append((env_user, os.getenv("GMAIL_APP_PASSWORD")))

        # 3. Default demo accounts
        for fallback in ["jordan.lee@enterprise.ai", "developer@aethermail.ai"]:
            if not any(a[0].lower() == fallback.lower() for a in target_accounts):
                target_accounts.append((fallback, None))

        for email_addr, pwd in target_accounts:
            try:
                res = sync_user_live_inbox(db=db, user_email=email_addr, password=pwd, max_results=10)
                if res.get("new_emails_processed", 0) > 0:
                    print(f" [AUTONOMOUS SYNC] Ingested {res['new_emails_processed']} new emails for {email_addr}!")
            except Exception as acc_err:
                pass

    except Exception as e:
        print(f" [SCHEDULER] Periodic sync warning: {e}")
    finally:
        db.close()

def start_background_scheduler(interval_seconds: int = 25, interval_minutes: Optional[int] = None):
    """Starts the APScheduler background job if not already running."""
    sec = interval_minutes * 60 if interval_minutes else interval_seconds
    if not scheduler.running:
        scheduler.add_job(
            scheduled_email_sync_job,
            "interval",
            seconds=sec,
            id="autonomous_email_sync_job",
            replace_existing=True
        )
        scheduler.start()
        print(f" [SCHEDULER] Autonomous Live Background Poller started (interval: every {sec}s).")


def stop_background_scheduler():
    """Stops the scheduler on server shutdown."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        print(" [SCHEDULER] Autonomous Background Poller stopped.")

