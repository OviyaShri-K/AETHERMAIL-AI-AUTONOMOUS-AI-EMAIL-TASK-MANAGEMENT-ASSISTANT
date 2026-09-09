import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

def setup_local_postgres(password="admin"):
    print("\n" + "="*80)
    print(" 🐘 SETTING UP LOCAL POSTGRESQL FOR PGADMIN 4")
    print("="*80)

    # 1. Connect to PostgreSQL server
    print(f"\n[1/4] Connecting to Local PostgreSQL Server (localhost:5432) with user 'postgres'...")
    try:
        conn = psycopg2.connect(host="localhost", port=5432, user="postgres", password=password, database="postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print("  ✅ Connected to PostgreSQL Server successfully!")
    except Exception as e:
        print(f"  ❌ Connection failed with password '{password}': {e}")
        print("\n  💡 TIP: If your password in pgAdmin is different, run:")
        print(f"     python scripts/setup_pgadmin_db.py YOUR_PGADMIN_PASSWORD\n")
        return False

    # 2. Create Database 'ai_email_db'
    print("\n[2/4] Creating database 'ai_email_db' in PostgreSQL...")
    try:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='ai_email_db';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE ai_email_db;")
            print("  ✅ Database 'ai_email_db' created successfully!")
        else:
            print("  ✅ Database 'ai_email_db' already exists.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"  ⚠️ Note on database creation: {e}")

    # 3. Update .env
    print("\n[3/4] Updating backend/.env with Local PostgreSQL Connection String...")
    pg_url = f"postgresql://postgres:{password}@localhost:5432/ai_email_db"
    env_path = os.path.join(backend_root, ".env")
    try:
        lines = []
        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        
        filtered = [l for l in lines if not l.startswith("DATABASE_URL=")]
        filtered.append(f"DATABASE_URL={pg_url}\n")
        
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(filtered)
        print(f"  ✅ Saved DATABASE_URL={pg_url}")
    except Exception as e:
        print(f"  ⚠️ Failed to update .env: {e}")

    # 4. Initialize Tables & Data
    print("\n[4/4] Creating Tables and Seeding Records with 'sarah.jenkins@techcorp.io'...")
    from sqlalchemy import create_engine
    from app.database import Base, SessionLocal
    import app.models
    from app.models import Email, Task, EventDeadline, AIAction, Attachment, AuditLog
    from app.services.db_service import seed_database_if_empty

    pg_engine = create_engine(pg_url)
    Base.metadata.create_all(bind=pg_engine)
    print("  ✅ Tables created in PostgreSQL: emails, tasks, deadlines_events, ai_actions, attachments, audit_logs")

    from sqlalchemy.orm import sessionmaker
    PgSession = sessionmaker(bind=pg_engine)
    db = PgSession()
    
    seed_database_if_empty(db)
    
    # Ensure all records have user's email
    target_email = "sarah.jenkins@techcorp.io"
    updated_emails = db.query(Email).update({Email.recipient: target_email})
    updated_tasks = db.query(Task).update({Task.assignee: target_email})
    db.commit()
    
    total = db.query(Email).count()
    print(f"  ✅ Imported {total} email records and {db.query(Task).count()} tasks into PostgreSQL for '{target_email}'!")
    db.close()

    print("\n" + "="*80)
    print(" 🎉 LOCAL POSTGRESQL & PGADMIN SETUP 100% COMPLETE!")
    print(f" 📂 Database Name:  ai_email_db")
    print(f" 👤 User:           postgres")
    print(f" 🔑 Password:       {password}")
    print(f" 📬 User Email:     sarah.jenkins@techcorp.io")
    print("="*80 + "\n")
    return True

if __name__ == "__main__":
    pwd = sys.argv[1] if len(sys.argv) > 1 else "admin"
    setup_local_postgres(pwd)
