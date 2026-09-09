import json
import os
import sys
from collections import Counter

# Set standard output to UTF-8
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def analyze_dataset(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    total_emails = len(data)
    spam_count = sum(1 for d in data if d["ground_truth"]["is_spam"])
    ham_count = total_emails - spam_count
    
    categories = Counter(d["ground_truth"]["category"] for d in data)
    priorities = Counter(d["ground_truth"]["priority"] for d in data)
    actionable_count = sum(1 for d in data if d["ground_truth"]["is_actionable"])
    
    total_tasks = sum(len(d["ground_truth"].get("tasks", [])) for d in data)
    total_deadlines = sum(len(d["ground_truth"].get("events_deadlines", [])) for d in data)
    approval_required = sum(1 for d in data if d["ground_truth"]["recommended_action"]["requires_human_approval"])
    
    print("\n" + "="*60)
    print(" UNIFIED DATASET SUMMARY & METRICS")
    print("="*60)
    print(f"Total Emails in Benchmark:       {total_emails}")
    print(f"Spam vs Legitimate (Ham):        {spam_count} Spam | {ham_count} Ham")
    print(f"Actionable Emails:               {actionable_count} ({actionable_count/total_emails*100:.1f}%)")
    print(f"Total Actionable Tasks Extracted:{total_tasks}")
    print(f"Total Events & Deadlines Mapped: {total_deadlines}")
    print(f"Human-in-the-Loop Required:      {approval_required} ({approval_required/total_emails*100:.1f}%)")
    print("-" * 60)
    print("Category Breakdown:")
    for cat, count in categories.items():
        print(f"  * {cat.capitalize():<15}: {count} ({count/total_emails*100:.1f}%)")
    print("-" * 60)
    print("Priority Breakdown:")
    for prio, count in priorities.items():
        print(f"  * {prio:<15}: {count} ({count/total_emails*100:.1f}%)")
    print("="*60 + "\n")

if __name__ == "__main__":
    path = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset\email_unified_benchmark.json"
    analyze_dataset(path)
