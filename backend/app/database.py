import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

backend_dir = os.path.dirname(os.path.abspath(__file__))
local_sqlite_url = f"sqlite:///{os.path.join(backend_dir, '..', 'local_dev.db')}"

db_url = settings.DATABASE_URL or "postgresql://postgres:admin@localhost:5432/ai_email_db"

if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

# Check if URL contains placeholder values or is sqlite
is_placeholder = any(
    placeholder in db_url 
    for placeholder in ["your_project_id", "your_password", "aws-0-region", "your-project-id"]
)

engine = None

if not is_placeholder and "sqlite" not in db_url:
    try:
        # Try connecting to PostgreSQL
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f" Connected successfully to Local PostgreSQL: {db_url}")
    except Exception as e:
        print(f"[WARN] Local PostgreSQL connection failed ({e}). Falling back to SQLite local database.")
        engine = None

if engine is None:
    db_url = local_sqlite_url
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    print(" Using local SQLite database engine (pgAdmin/local fallback).")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to provide a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Creates all database tables in PostgreSQL / local database."""
    import app.models  # Ensure all models are imported before creating tables
    Base.metadata.create_all(bind=engine)
    print(" All PostgreSQL database tables successfully initialized!")
