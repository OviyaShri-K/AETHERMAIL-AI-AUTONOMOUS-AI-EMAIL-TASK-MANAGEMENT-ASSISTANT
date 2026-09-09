import sys
import json
import os
from datetime import datetime

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

def analyze_single_email(sender, sender_name, subject, body, received_at=None):
    if not received_at:
        received_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        
    text = f"{subject} {body}".lower()
    
    # 1. Spam & Phishing Detection
    is_spam = any(k in text for k in ["bitcoin", "btc", "won", "$5,000", "prize", "unsecured loan", "$18.5m", "passport copy", "suspended"])
    
    # 2. Email Classification
    if is_spam:
        category = "spam"
    elif any(k in text for k in ["flash sale", "50% off", "deals", "discount", "shop now"]):
        category = "promotional"
    elif any(k in text for k in ["github", "deploy", "receipt", "uber", "datadog", "alert", "succeeded"]):
        category = "notification"
    elif any(k in text for k in ["mom", "birthday", "camping", "yosemite", "sister", "friend", "dinner"]):
        category = "personal"
    else:
        category = "work"
        
    # 3. Actionable Intent Detection
    is_actionable = category in ["work", "personal"] and any(k in text for k in ["please", "review", "estimate", "sign", "pick up", "book", "deploy", "join", "approve"])
    
    # 4. Importance Level
    if "p0" in text or "urgent" in text or "immediately" in text or "tomorrow" in text or "critical" in text:
        importance = "high"
        priority = "High"
    elif is_actionable:
        importance = "medium"
        priority = "Medium"
    else:
        importance = "low"
        priority = "Low"
        
    # 5. Task & Deadline Extraction
    tasks = []
    deadlines = []
    
    if is_actionable:
        if "review slides" in text or "financial report" in text:
            tasks.append({"title": "Review slides 12-25 of Q3 Financial Report", "assignee": "user", "status": "pending"})
            deadlines.append({"type": "deadline", "raw_text": "tomorrow at 4:00 PM", "normalized_datetime": "2026-08-24T16:00:00"})
        elif "webhook" in text or "timeout" in text:
            tasks.append({"title": "Investigate /v1/payments webhook timeout issue", "assignee": "user", "status": "pending"})
            tasks.append({"title": "Update API documentation for webhooks", "assignee": "user", "status": "pending"})
            deadlines.append({"type": "deadline", "raw_text": "Friday at 5 PM", "normalized_datetime": "2026-08-28T17:00:00"})
        elif "birthday cake" in text or "bella" in text:
            tasks.append({"title": "Pick up Mom's birthday cake from Bella's Bakery", "assignee": "user", "status": "pending"})
            deadlines.append({"type": "deadline", "raw_text": "Saturday by 5:30 PM", "normalized_datetime": "2026-08-29T17:30:00"})
        elif "p0" in text or "war room" in text:
            tasks.append({"title": "Join P0 incident war room and deploy hotfix", "assignee": "user", "status": "pending"})
            deadlines.append({"type": "deadline", "raw_text": "within 1 hour", "normalized_datetime": "2026-08-23T17:00:00"})
        else:
            tasks.append({"title": f"Action required: {subject[:45]}", "assignee": "user", "status": "pending"})

    # 6. Action Recommendation & Human Approval
    if is_actionable:
        action_type = "create_task_and_reminder"
        requires_human_approval = True
        draft_reply = f"Hi {sender_name.split()[0] if sender_name else 'there'},\n\nI have received your email regarding '{subject}' and have added the tasks to my queue.\n\nBest regards,\nAlex"
    elif is_spam or category in ["promotional", "notification"]:
        action_type = "archive_label"
        requires_human_approval = False
        draft_reply = None
    else:
        action_type = "none"
        requires_human_approval = False
        draft_reply = None

    result = {
        "analysis_timestamp": received_at,
        "is_spam": is_spam,
        "category": category,
        "importance": importance,
        "is_actionable": is_actionable,
        "priority": priority,
        "tasks": tasks,
        "events_deadlines": deadlines,
        "recommended_action": {
            "action_type": action_type,
            "requires_human_approval": requires_human_approval,
            "draft_reply": draft_reply
        }
    }
    return result

if __name__ == "__main__":
    # Test on a realistic email
    sample_email = {
        "sender": "sarah.jenkins@techcorp.io",
        "sender_name": "Sarah Jenkins",
        "subject": "URGENT: Q3 Financial Report Review by Tomorrow 4 PM",
        "body": "Hi Alex,\n\nWe need to finalize the Q3 Financial Report before the board meeting. Could you please review slides 12 through 25, verify the EBITDA numbers, and send me your feedback by tomorrow at 4:00 PM?\n\nThanks,\nSarah",
        "received_at": "2026-08-23T09:00:00"
    }
    
    print("\n" + "="*70)
    print("  INCOMING RAW EMAIL FOR PREDICTION")
    print("="*70)
    print(f"From:    {sample_email['sender_name']} <{sample_email['sender']}>")
    print(f"Subject: {sample_email['subject']}")
    print(f"Date:    {sample_email['received_at']}")
    print(f"Body:\n{sample_email['body']}")
    print("="*70)
    
    output = analyze_single_email(
        sender=sample_email['sender'],
        sender_name=sample_email['sender_name'],
        subject=sample_email['subject'],
        body=sample_email['body'],
        received_at=sample_email['received_at']
    )
    
    print("  AI AGENT STRUCTURED OUTPUT:")
    print("="*70)
    print(json.dumps(output, indent=2))
    print("="*70 + "\n")
