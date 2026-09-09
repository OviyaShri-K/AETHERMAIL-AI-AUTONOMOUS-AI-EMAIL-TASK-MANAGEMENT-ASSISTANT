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
from app.models import Task, Email, AIAction

def balance_tasks_and_emails():
    db = SessionLocal()
    try:
        print("\n" + "="*70)
        print(" ⚖️ BALANCING TASK STATUSES & PRIORITIES IN DATABASE")
        print("="*70)

        tasks = db.query(Task).order_by(Task.id).all()
        print(f" Found {len(tasks)} total tasks.")

        # Balance statuses: ~50% pending, ~25% in_progress, ~25% completed
        # Balance priorities: ~40% High, ~35% Medium, ~25% Low
        statuses_cycle = ["pending", "in_progress", "completed", "pending", "in_progress", "pending"]
        priorities_cycle = ["High", "Medium", "Low", "High", "Medium", "Low", "High"]

        for i, t in enumerate(tasks):
            t.status = statuses_cycle[i % len(statuses_cycle)]
            t.priority = priorities_cycle[i % len(priorities_cycle)]

        db.commit()

        # Audit new distribution
        status_counts = {}
        for t in db.query(Task).all():
            status_counts[t.status] = status_counts.get(t.status, 0) + 1

        prio_counts = {}
        for t in db.query(Task).all():
            prio_counts[t.priority] = prio_counts.get(t.priority, 0) + 1

        print("\n  NEW BALANCED TASK STATUSES:")
        for s, c in status_counts.items():
            print(f"   • {s.ljust(15)}: {c} tasks")

        print("\n  NEW BALANCED TASK PRIORITIES:")
        for p, c in prio_counts.items():
            print(f"   • {p.ljust(15)}: {c} tasks")

        print("="*70 + "\n")

    finally:
        db.close()

if __name__ == "__main__":
    balance_tasks_and_emails()
