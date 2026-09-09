import json
import csv
import os
import random

def split_dataset(json_path, output_dir, train_ratio=0.8, seed=42):
    random.seed(seed)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Group by category for stratified split
    by_category = {}
    for item in data:
        cat = item["ground_truth"]["category"]
        by_category.setdefault(cat, []).append(item)
        
    train_data = []
    test_data = []
    
    for cat, items in by_category.items():
        random.shuffle(items)
        n_train = max(1, int(len(items) * train_ratio))
        train_data.extend(items[:n_train])
        test_data.extend(items[n_train:])
        
    random.shuffle(train_data)
    random.shuffle(test_data)
    
    # Save JSON splits
    train_json_path = os.path.join(output_dir, "train_benchmark.json")
    test_json_path = os.path.join(output_dir, "test_benchmark.json")
    
    with open(train_json_path, "w", encoding="utf-8") as f:
        json.dump(train_data, f, indent=2)
    with open(test_json_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f, indent=2)
        
    # Save CSV splits
    def save_csv(data_list, csv_path):
        fieldnames = [
            "email_id", "timestamp", "sender", "sender_name", "subject", "body",
            "is_spam", "category", "importance", "is_actionable", "tasks_count",
            "tasks_summary", "deadlines_count", "deadlines_summary", "priority",
            "action_type", "requires_human_approval", "draft_reply"
        ]
        rows = []
        for item in data_list:
            gt = item["ground_truth"]
            tasks = gt.get("tasks", [])
            deadlines = gt.get("events_deadlines", [])
            task_str = " | ".join([f"{t['title']}" for t in tasks]) if tasks else "None"
            deadline_str = " | ".join([f"{d['raw_text']} -> {d.get('normalized_datetime')}" for d in deadlines]) if deadlines else "None"
            rec_action = gt.get("recommended_action", {})
            draft = rec_action.get("draft_reply", "")
            draft_clean = draft.replace("\r\n", " \\n ").replace("\n", " \\n ") if draft else ""
            clean_body = item["body"].replace("\r\n", " \\n ").replace("\n", " \\n ")
            
            rows.append({
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
                "draft_reply": draft_clean
            })
            
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
            writer.writeheader()
            writer.writerows(rows)

    train_csv_path = os.path.join(output_dir, "train_benchmark.csv")
    test_csv_path = os.path.join(output_dir, "test_benchmark.csv")
    
    save_csv(train_data, train_csv_path)
    save_csv(test_data, test_csv_path)
    
    print(f"SUCCESS: Split dataset into {len(train_data)} train samples and {len(test_data)} test samples.")
    print(f"Train JSON: {train_json_path}")
    print(f"Test JSON:  {test_json_path}")
    print(f"Train CSV:  {train_csv_path}")
    print(f"Test CSV:   {test_csv_path}")

if __name__ == "__main__":
    src_json = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset\email_unified_benchmark.json"
    out_dir = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset"
    split_dataset(src_json, out_dir, train_ratio=0.8)
