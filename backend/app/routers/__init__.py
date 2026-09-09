from app.routers.emails import router as emails_router
from app.routers.tasks import router as tasks_router
from app.routers.approvals import router as approvals_router
from app.routers.analytics import router as analytics_router
from app.routers.attachments import router as attachments_router
from app.routers.gmail import router as gmail_router
from app.routers.users import router as users_router

__all__ = [
    "emails_router",
    "tasks_router",
    "approvals_router",
    "analytics_router",
    "attachments_router",
    "gmail_router",
    "users_router"
]
