import json
import csv
import os

def export_to_csv(json_path, csv_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    fieldnames = [
        "email_id",
        "timestamp",
        "sender",
        "sender_name",
        "subject",
        "body",
        "is_spam",
        "category",
        "importance",
        "is_actionable",
        "tasks_count",
        "tasks_summary",
        "deadlines_count",
        "deadlines_summary",
        "priority",
        "action_type",
        "requires_human_approval",
        "draft_reply"
    ]
    
    rows = []
    for item in data:
        gt = item["ground_truth"]
        tasks = gt.get("tasks", [])
        deadlines = gt.get("events_deadlines", [])
        
        task_str = " | ".join([f"{t['title']} ({t.get('description', '')})" for t in tasks]) if tasks else "None"
        deadline_str = " | ".join([f"{d['raw_text']} -> {d.get('normalized_datetime')} [{d.get('description', '')}]" for d in deadlines]) if deadlines else "None"
        
        rec_action = gt.get("recommended_action", {})
        draft = rec_action.get("draft_reply", "")
        if draft:
            draft = draft.replace("\r\n", " \\n ").replace("\n", " \\n ")
        else:
            draft = ""
            
        clean_body = item["body"].replace("\r\n", " \\n ").replace("\n", " \\n ")
        
        row = {
            "email_id": item["email_id"],
            "timestamp": item["timestamp"],
            "sender": item["sender"],
            "sender_name": item.get("sender_name", ""),
            "subject": item["subject"],
            "body": clean_body,
            "is_spam": "TRUE" if gt["is_spam"] else "FALSE",
            "category": gt["category"],
            "importance": gt["importance"],
            "is_actionable": "TRUE" if gt["is_actionable"] else "FALSE",
            "tasks_count": len(tasks),
            "tasks_summary": task_str,
            "deadlines_count": len(deadlines),
            "deadlines_summary": deadline_str,
            "priority": gt["priority"],
            "action_type": rec_action.get("action_type", "none"),
            "requires_human_approval": "TRUE" if rec_action.get("requires_human_approval", False) else "FALSE",
            "draft_reply": draft
        }
        rows.append(row)
        
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"SUCCESS: Exported clean single-line CSV with {len(rows)} records to: {csv_path}")

if __name__ == "__main__":
    json_p = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset\email_unified_benchmark.json"
    csv_p = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset\email_unified_benchmark.csv"
    export_to_csv(json_p, csv_p)
