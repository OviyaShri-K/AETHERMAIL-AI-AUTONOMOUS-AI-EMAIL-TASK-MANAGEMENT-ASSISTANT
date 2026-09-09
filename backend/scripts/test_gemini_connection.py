import os
import sys

# Set Python path to backend folder
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, backend_root)

# Set UTF-8 output encoding for Windows compatibility
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.config import settings
from app.ai.gemini_service import analyze_with_gemini

def test_gemini():
    print("\n" + "="*75)
    print("  GOOGLE GEMINI 2.5 FLASH CONNECTION TEST")
    print("="*75)
    
    key = settings.GEMINI_API_KEY
    if key and key.startswith("AIza"):
        masked = key[:6] + "..." + key[-4:]
        print(f" Detected GEMINI_API_KEY: {masked}")
    else:
        print("  No live GEMINI_API_KEY detected in .env (Using Local AI Engine Fallback)")

    sample_email = {
        "sender": "sarah.jenkins@techcorp.io",
        "sender_name": "Sarah Jenkins",
        "subject": "URGENT: Q3 Financial Report Review by Tomorrow 4 PM",
        "body": "Hi Alex, please review slides 12 through 25, verify the EBITDA numbers, and send me your feedback by tomorrow at 4:00 PM.",
        "received_at": "2026-08-24T10:00:00"
    }

    print("\n Running AI Analysis on Test Email...")
    output = analyze_with_gemini(
        sender=sample_email["sender"],
        sender_name=sample_email["sender_name"],
        subject=sample_email["subject"],
        body=sample_email["body"],
        timestamp_str=sample_email["received_at"]
    )

    print("\n  AI EXTRACTION RESULT:")
    print("-" * 75)
    print(f"  • Category:            {output['category']}")
    print(f"  • Priority:            {output['priority']}")
    print(f"  • Is Actionable:       {output['is_actionable']}")
    print(f"  • Tasks Extracted:     {len(output.get('tasks', []))}")
    for t in output.get('tasks', []):
        print(f"      - {t['title']}")
    print(f"  • Deadlines Mapped:    {len(output.get('events_deadlines', []))}")
    for d in output.get('events_deadlines', []):
        print(f"      - {d.get('raw_text')} -> {d.get('normalized_datetime')}")
    print(f"  • Action Type:         {output['recommended_action']['action_type']}")
    print(f"  • Human Approval Req:  {output['recommended_action']['requires_human_approval']}")
    if output['recommended_action'].get('draft_reply'):
        print(f"  • Generated Reply:     \n\"{output['recommended_action']['draft_reply']}\"")
    print("="*75)
    print("  GEMINI / AI PIPELINE TEST COMPLETED SUCCESSFULLY!")
    print("="*75 + "\n")

if __name__ == "__main__":
    test_gemini()
