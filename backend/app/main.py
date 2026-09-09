import os
import sys

# Ensure UTF-8 stdout on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.services.scheduler_service import start_background_scheduler, stop_background_scheduler
from app.routers import (
    emails_router,
    tasks_router,
    approvals_router,
    analytics_router,
    attachments_router,
    gmail_router,
    users_router
)

# Initialize FastAPI App
app = FastAPI(
    title="Autonomous AI Email & Task Management Assistant API",
    description="Backend REST APIs for Multi-User AI email analysis, task management, Human-in-the-Loop approvals, PostgreSQL (pgAdmin 4), and Cloudinary Media storage.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for Next.js 14 Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(users_router)
app.include_router(emails_router)
app.include_router(tasks_router)
app.include_router(approvals_router)
app.include_router(attachments_router)
app.include_router(gmail_router)
app.include_router(analytics_router)

@app.on_event("startup")
def on_startup():
    """Auto-initialize database tables and start background scheduler."""
    print(" Starting FastAPI Server & checking PostgreSQL connection...")
    init_db()
    # Start Autonomous Background Email Poller (Runs every 20 seconds)
    start_background_scheduler(interval_seconds=20)

@app.on_event("shutdown")
def on_shutdown():
    """Stop scheduler on shutdown."""
    stop_background_scheduler()

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Autonomous AI Email & Task Management Assistant API",
        "documentation": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "storage": "Cloudinary Ready",
        "gmail_sync": "Autonomous Poller Active"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
