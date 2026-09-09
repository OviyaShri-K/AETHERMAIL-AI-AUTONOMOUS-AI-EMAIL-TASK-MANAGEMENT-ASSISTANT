# 📧 Unified AI Email & Task Management Benchmark Dataset

This unified dataset replaces multiple disconnected datasets with a single **comprehensive ground-truth benchmark**. Each email is annotated simultaneously across all 6 core functional modules.

---

## 🗂️ File Location
- **JSON File**: `dataset/email_unified_benchmark.json`
- **Generator Script**: `dataset_generator.py`
- **Stats & Metrics Script**: `dataset_stats.py`

---

## 📊 Dataset Breakdown & Metrics

| Metric | Count / Distribution | Description |
| :--- | :--- | :--- |
| **Total Benchmark Samples** | 50 samples | Full multi-task annotated emails |
| **Spam vs Legitimate (Ham)** | 9 Spam (18%) \| 41 Ham (82%) | Realistic real-world inbox ratio |
| **Actionable Emails** | 35 emails (70%) | Emails containing user requests/tasks |
| **Non-Actionable Emails**| 15 emails (30%) | Newsletters, notifications, logs, spam |
| **Total Actionable Tasks** | 47 Tasks | Imperative, structured task definitions |
| **Deadlines & Events** | 42 Dates/Times | Normalized ISO-8601 timestamps |
| **Human-in-the-Loop** | 33 cases (66%) | Requiring explicit user approval |

### Category Breakdown
* **Work (`work`)**: 25 emails (50%)
* **Personal (`personal`)**: 9 emails (18%)
* **Notification (`notification`)**: 7 emails (14%)
* **Spam (`spam`)**: 9 emails (18%)
* **Promotional (`promotional`)**: 7 emails (14%)

### Priority Breakdown
* **High**: 20 emails (40%) - Urgent, tight deadlines (<48h), P0 alerts
* **Medium**: 15 emails (30%) - Standard tasks, meetings, 3-7 day turnaround
* **Low**: 15 emails (30%) - Notifications, newsletters, spam, distant tasks

---

## 📋 JSON Record Schema

```json
{
  "email_id": "email_001",
  "timestamp": "2026-08-23T09:00:00",
  "sender": "sarah.jenkins@techcorp.io",
  "sender_name": "Sarah Jenkins",
  "recipient": "alex.dev@techcorp.io",
  "subject": "URGENT: Q3 Financial Report Review by Tomorrow 4 PM",
  "body": "Hi Alex,\n\nWe need to finalize the Q3 Financial Report...",
  "ground_truth": {
    "is_spam": false,
    "category": "work",
    "importance": "high",
    "is_actionable": true,
    "tasks": [
      {
        "title": "Review slides 12-25 of Q3 Financial Report",
        "description": "Review slides 12 through 25, verify EBITDA numbers, and send feedback to Sarah",
        "assignee": "user",
        "status": "pending"
      }
    ],
    "events_deadlines": [
      {
        "type": "deadline",
        "raw_text": "tomorrow at 4:00 PM",
        "normalized_datetime": "2026-08-24T16:00:00",
        "description": "Send feedback on Q3 Financial Report to Sarah"
      }
    ],
    "priority": "High",
    "recommended_action": {
      "action_type": "create_task_and_reminder",
      "requires_human_approval": true,
      "draft_reply": "Hi Sarah,\n\nI will review slides 12-25..."
    }
  }
}
```
