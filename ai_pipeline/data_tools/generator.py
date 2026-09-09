import json
import os
from datetime import datetime, timedelta

def build_benchmark_dataset():
    base_time = datetime(2026, 8, 23, 9, 0, 0)
    
    emails = [
        # 1. Work - Urgent Task with Tight Deadline
        {
            "email_id": "email_001",
            "timestamp": (base_time).isoformat(),
            "sender": "sarah.jenkins@techcorp.io",
            "sender_name": "Sarah Jenkins",
            "recipient": "alex.dev@techcorp.io",
            "subject": "URGENT: Q3 Financial Report Review by Tomorrow 4 PM",
            "body": "Hi Alex,\n\nWe need to finalize the Q3 Financial Report before the board meeting. Could you please review slides 12 through 25, verify the EBITDA numbers, and send me your feedback by tomorrow at 4:00 PM?\n\nThis is critical for Wednesday's presentation.\n\nThanks,\nSarah",
            "ground_truth": {
                "is_spam": False,
                "category": "work",
                "importance": "high",
                "is_actionable": True,
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
                    },
                    {
                        "type": "event",
                        "raw_text": "Wednesday",
                        "normalized_datetime": "2026-08-26T09:00:00",
                        "description": "Board meeting presentation"
                    }
                ],
                "priority": "High",
                "recommended_action": {
                    "action_type": "create_task_and_reminder",
                    "requires_human_approval": True,
                    "draft_reply": "Hi Sarah,\n\nI will review slides 12-25 and verify the EBITDA figures, then get back to you with my notes before 4:00 PM tomorrow.\n\nBest,\nAlex"
                }
            }
        },
        # 2. Work - Multiple Action Items & Meeting Scheduling
        {
            "email_id": "email_002",
            "timestamp": (base_time + timedelta(hours=1)).isoformat(),
            "sender": "david.ross@clientpartner.com",
            "sender_name": "David Ross",
            "recipient": "alex.dev@techcorp.io",
            "subject": "API Integration Feedback & Sync Request",
            "body": "Hello Alex,\n\nOur engineering team tested the new webhook endpoints. Overall it looks great, but we found a timeout issue on the /v1/payments endpoint. \n\nPlease look into the timeout issue and update the API documentation accordingly by Friday at 5 PM.\n\nAlso, let's schedule a 30-minute sync on Thursday, Aug 27 at 2:30 PM to discuss the rollout.\n\nRegards,\nDavid Ross",
            "ground_truth": {
                "is_spam": False,
                "category": "work",
                "importance": "high",
                "is_actionable": True,
                "tasks": [
                    {
                        "title": "Investigate /v1/payments webhook timeout issue",
                        "description": "Debug timeout issue on webhook endpoints reported by David's team",
                        "assignee": "user",
                        "status": "pending"
                    },
                    {
                        "title": "Update API documentation for webhooks",
                        "description": "Update API docs for webhook endpoints by Friday 5 PM",
                        "assignee": "user",
                        "status": "pending"
                    }
                ],
                "events_deadlines": [
                    {
                        "type": "deadline",
                        "raw_text": "Friday at 5 PM",
                        "normalized_datetime": "2026-08-28T17:00:00",
                        "description": "Update API documentation"
                    },
                    {
                        "type": "meeting",
                        "raw_text": "Thursday, Aug 27 at 2:30 PM",
                        "normalized_datetime": "2026-08-27T14:30:00",
                        "description": "30-minute sync with David Ross on API rollout"
                    }
                ],
                "priority": "High",
                "recommended_action": {
                    "action_type": "create_task_and_reminder",
                    "requires_human_approval": True,
                    "draft_reply": "Hi David,\n\nThanks for the feedback. I am investigating the /v1/payments timeout and will have the documentation updated by Friday 5 PM. Thursday at 2:30 PM works for the sync.\n\nBest,\nAlex"
                }
            }
        },
        # 3. Spam / Phishing - Unsolicited Prize / Fraud
        {
            "email_id": "email_003",
            "timestamp": (base_time + timedelta(hours=2)).isoformat(),
            "sender": "rewards@claim-crypto-bonus-now.xyz",
            "sender_name": "Global Reward Center",
            "recipient": "alex.dev@techcorp.io",
            "subject": "CONGRATULATIONS! You have won $5,000 in Bitcoin! Claim within 24 hours!",
            "body": "Dear valued customer,\n\nYour email address has been selected as the 1st prize winner of 0.15 BTC ($5,000 USD). \n\nClick the link below immediately to connect your wallet and withdraw your prize:\nhttp://claim-crypto-bonus-now.xyz/claim?id=99283\n\nFailure to claim within 24 hours will forfeit your rewards.",
            "ground_truth": {
                "is_spam": True,
                "category": "spam",
                "importance": "low",
                "is_actionable": False,
                "tasks": [],
                "events_deadlines": [],
                "priority": "Low",
                "recommended_action": {
                    "action_type": "archive_label",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        },
        # 4. Promotional - Marketing Newsletter / Discount
        {
            "email_id": "email_004",
            "timestamp": (base_time + timedelta(hours=3)).isoformat(),
            "sender": "news@cloudhosting.net",
            "sender_name": "CloudHosting Pro",
            "recipient": "alex.dev@techcorp.io",
            "subject": "Flash Sale: 50% Off All Dedicated Cloud Instances This Weekend!",
            "body": "Hi Alex,\n\nUpgrade your infrastructure today! For the next 48 hours only, get 50% off our Enterprise NVMe dedicated cloud servers. Use promo code FLASH50 at checkout.\n\nOffer ends Sunday midnight.\n\nUnsubscribe from these emails anytime by clicking here.",
            "ground_truth": {
                "is_spam": False,
                "category": "promotional",
                "importance": "low",
                "is_actionable": False,
                "tasks": [],
                "events_deadlines": [
                    {
                        "type": "event",
                        "raw_text": "Sunday midnight",
                        "normalized_datetime": "2026-08-30T23:59:59",
                        "description": "Flash sale promo code FLASH50 expiration"
                    }
                ],
                "priority": "Low",
                "recommended_action": {
                    "action_type": "archive_label",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        },
        # 5. Notification - System Alert / Non-actionable info
        {
            "email_id": "email_005",
            "timestamp": (base_time + timedelta(hours=4)).isoformat(),
            "sender": "no-reply@github.com",
            "sender_name": "GitHub Notifications",
            "recipient": "alex.dev@techcorp.io",
            "subject": "[GitHub] Run Succeeded: Deploy to Production #142",
            "body": "GitHub Actions workflow 'Production Deployment' has completed successfully.\n\nCommit: a8f9b1c (Merge pull request #89 from techcorp/feature-auth)\nBranch: main\nDuration: 4m 12s\n\nView build logs: https://github.com/techcorp/backend/actions/runs/142",
            "ground_truth": {
                "is_spam": False,
                "category": "notification",
                "importance": "medium",
                "is_actionable": False,
                "tasks": [],
                "events_deadlines": [],
                "priority": "Low",
                "recommended_action": {
                    "action_type": "archive_label",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        },
        # 6. Personal - Family / Social Request with Event
        {
            "email_id": "email_006",
            "timestamp": (base_time + timedelta(hours=5)).isoformat(),
            "sender": "emma.sister@gmail.com",
            "sender_name": "Emma Wilson",
            "recipient": "alex.dev@techcorp.io",
            "subject": "Mom's Birthday Dinner this Saturday at 7 PM",
            "body": "Hey Alex,\n\nWe are organizing Mom's surprise birthday dinner this Saturday at 7:00 PM at Olive Garden downtown. Can you please bring the birthday cake from Bella's Bakery? Make sure to pick it up by 5:30 PM before they close.\n\nLet me know if that works for you!\n\nLove,\nEmma",
            "ground_truth": {
                "is_spam": False,
                "category": "personal",
                "importance": "high",
                "is_actionable": True,
                "tasks": [
                    {
                        "title": "Pick up Mom's birthday cake from Bella's Bakery",
                        "description": "Pick up birthday cake by 5:30 PM this Saturday for surprise dinner",
                        "assignee": "user",
                        "status": "pending"
                    }
                ],
                "events_deadlines": [
                    {
                        "type": "deadline",
                        "raw_text": "Saturday by 5:30 PM",
                        "normalized_datetime": "2026-08-29T17:30:00",
                        "description": "Pick up cake from bakery before closing"
                    },
                    {
                        "type": "event",
                        "raw_text": "this Saturday at 7:00 PM",
                        "normalized_datetime": "2026-08-29T19:00:00",
                        "description": "Mom's surprise birthday dinner at Olive Garden"
                    }
                ],
                "priority": "Medium",
                "recommended_action": {
                    "action_type": "create_task_and_reminder",
                    "requires_human_approval": True,
                    "draft_reply": "Hey Emma,\n\nSounds great! I'll order and pick up the cake from Bella's Bakery before 5:30 PM on Saturday and see you all at 7 PM.\n\nLove,\nAlex"
                }
            }
        },
        # 7. Work - Low Priority / Routine Task with Relaxed Deadline
        {
            "email_id": "email_007",
            "timestamp": (base_time + timedelta(hours=6)).isoformat(),
            "sender": "hr@techcorp.io",
            "sender_name": "TechCorp People Operations",
            "recipient": "alex.dev@techcorp.io",
            "subject": "Annual Cybersecurity Awareness Training - Due Sept 15",
            "body": "Dear Employee,\n\nAs part of our compliance standards, all staff members are required to complete the 2026 Annual Cybersecurity Training module.\n\nThe course takes approximately 45 minutes to complete.\n\nPlease log in to the portal and finish the module by September 15, 2026, 6:00 PM.\n\nLink: https://learning.techcorp.io/course/sec-2026\n\nThank you,\nPeople Operations",
            "ground_truth": {
                "is_spam": False,
                "category": "work",
                "importance": "medium",
                "is_actionable": True,
                "tasks": [
                    {
                        "title": "Complete Annual Cybersecurity Awareness Training",
                        "description": "Finish 45-min online training module on learning portal",
                        "assignee": "user",
                        "status": "pending"
                    }
                ],
                "events_deadlines": [
                    {
                        "type": "deadline",
                        "raw_text": "September 15, 2026, 6:00 PM",
                        "normalized_datetime": "2026-09-15T18:00:00",
                        "description": "Cybersecurity compliance training due date"
                    }
                ],
                "priority": "Low",
                "recommended_action": {
                    "action_type": "create_task_and_reminder",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        },
        # 8. Work - Urgent Critical Production Incident (Highest Priority)
        {
            "email_id": "email_008",
            "timestamp": (base_time + timedelta(hours=7)).isoformat(),
            "sender": "ops-alerts@techcorp.io",
            "sender_name": "DevOps Incident Response",
            "recipient": "alex.dev@techcorp.io",
            "subject": "CRITICAL P0 INCIDENT: Database Connection Pool Exhausted in US-East",
            "body": "ALERT: P0 Incident #8892 opened.\n\nImpact: 35% of incoming API requests are failing with HTTP 500 error.\nService: Payment Gateway & User Auth.\n\nAction Required: Alex, please join the incident bridge war room immediately at https://meet.techcorp.io/war-room-p0 and deploy the hotfix within 1 hour.\n\nIncident Commander: Marcus Vance",
            "ground_truth": {
                "is_spam": False,
                "category": "work",
                "importance": "high",
                "is_actionable": True,
                "tasks": [
                    {
                        "title": "Join P0 incident war room and deploy database connection hotfix",
                        "description": "Investigate connection pool exhaustion in US-East and deploy hotfix within 1 hour",
                        "assignee": "user",
                        "status": "pending"
                    }
                ],
                "events_deadlines": [
                    {
                        "type": "deadline",
                        "raw_text": "within 1 hour",
                        "normalized_datetime": "2026-08-23T17:00:00",
                        "description": "Deploy database hotfix to restore US-East cluster"
                    },
                    {
                        "type": "meeting",
                        "raw_text": "immediately",
                        "normalized_datetime": "2026-08-23T16:00:00",
                        "description": "Incident bridge war room"
                    }
                ],
                "priority": "High",
                "recommended_action": {
                    "action_type": "escalate",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        },
        # 9. Work - Vendor Invoice & Payment Approval
        {
            "email_id": "email_009",
            "timestamp": (base_time + timedelta(hours=8)).isoformat(),
            "sender": "billing@cloudservices.com",
            "sender_name": "CloudServices Billing",
            "recipient": "alex.dev@techcorp.io",
            "subject": "Invoice INV-2026-881 for August Services Due in 10 Days",
            "body": "Dear Alex,\n\nPlease find attached Invoice #INV-2026-881 for the period Aug 1 - Aug 23, 2026, totaling $3,450.00.\n\nPlease approve and remit payment by September 2, 2026 to avoid late fees.\n\nPayment Portal: https://billing.cloudservices.com/pay/881\n\nThank you for your business.",
            "ground_truth": {
                "is_spam": False,
                "category": "work",
                "importance": "medium",
                "is_actionable": True,
                "tasks": [
                    {
                        "title": "Approve and process payment for Invoice #INV-2026-881 ($3,450.00)",
                        "description": "Review CloudServices August invoice and submit for accounts payable",
                        "assignee": "user",
                        "status": "pending"
                    }
                ],
                "events_deadlines": [
                    {
                        "type": "deadline",
                        "raw_text": "September 2, 2026",
                        "normalized_datetime": "2026-09-02T17:00:00",
                        "description": "Payment due date for invoice INV-2026-881"
                    }
                ],
                "priority": "Medium",
                "recommended_action": {
                    "action_type": "create_task_and_reminder",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        },
        # 10. Spam - Phishing Account Verification
        {
            "email_id": "email_010",
            "timestamp": (base_time + timedelta(hours=9)).isoformat(),
            "sender": "security-alert@service-paypal-verify.net",
            "sender_name": "PayPal Security",
            "recipient": "alex.dev@techcorp.io",
            "subject": "Account Suspended: Verify your identity immediately",
            "body": "We detected unauthorized login attempts from IP 192.168.4.12. Your account has been temporarily restricted.\n\nTo restore your account access, click here: http://service-paypal-verify.net/restore\n\nIf you do not verify within 12 hours, your account will be permanently closed.",
            "ground_truth": {
                "is_spam": True,
                "category": "spam",
                "importance": "low",
                "is_actionable": False,
                "tasks": [],
                "events_deadlines": [],
                "priority": "Low",
                "recommended_action": {
                    "action_type": "archive_label",
                    "requires_human_approval": False,
                    "draft_reply": None
                }
            }
        }
    ]

    # Additional systematic real-world scenarios across all categories
    templates = [
        # Work Sprint / Planning
        (
            "rachel.pm@techcorp.io", "Rachel Green (Product)", "Sprint 42 Backlog Grooming Action Items",
            "Hi Alex,\n\nFollowing our grooming session, please estimate story points for tickets TECH-401 through TECH-410 by tomorrow at 2:00 PM. Also, please review the PR from backend team before end of day Wednesday.\n\nThanks,\nRachel",
            "work", "high", True,
            [
                {"title": "Estimate story points for tickets TECH-401 to TECH-410", "description": "Add estimates in Jira by tomorrow 2 PM", "assignee": "user", "status": "pending"},
                {"title": "Review backend team Pull Request", "description": "Review PR before end of day Wednesday", "assignee": "user", "status": "pending"}
            ],
            [
                {"type": "deadline", "raw_text": "tomorrow at 2:00 PM", "normalized_datetime": "2026-08-24T14:00:00", "description": "Jira ticket point estimations"},
                {"type": "deadline", "raw_text": "end of day Wednesday", "normalized_datetime": "2026-08-26T18:00:00", "description": "Backend PR review"}
            ],
            "High", "create_task_and_reminder", True, "Hi Rachel, I'll finish the story point estimates by 2 PM tomorrow and review the PR by Wednesday. Thanks!"
        ),
        # Legal / NDA
        (
            "sam.legal@techcorp.io", "Samira Legal", "NDA Signature Required for Partner Alpha",
            "Hi Alex,\n\nAttached is the non-disclosure agreement for our upcoming partnership with Partner Alpha. Please sign and return the executed PDF by Thursday at 12:00 PM.\n\nBest,\nSamira",
            "work", "medium", True,
            [{"title": "Sign and return Partner Alpha NDA PDF", "description": "Sign executed NDA and email back to Samira by Thursday noon", "assignee": "user", "status": "pending"}],
            [{"type": "deadline", "raw_text": "Thursday at 12:00 PM", "normalized_datetime": "2026-08-27T12:00:00", "description": "Signed NDA due to Legal"}],
            "Medium", "create_task_and_reminder", True, "Hi Samira, received. I will sign and return the NDA before Thursday 12:00 PM."
        ),
        # Promotional / Sales
        (
            "deals@techgear.shop", "TechGear Shop", "Back to School Tech Deals - Up to 40% Off Laptops & Monitors",
            "Don't miss our biggest tech sale of the summer! Get top-tier 4K monitors, mechanical keyboards, and noise-canceling headphones at unbeatable prices.\n\nShop now: https://techgear.shop/deals\n\nSale expires Monday, Aug 31 at 11:59 PM.",
            "promotional", "low", False, [],
            [{"type": "event", "raw_text": "Monday, Aug 31 at 11:59 PM", "normalized_datetime": "2026-08-31T23:59:00", "description": "TechGear sale expiration"}],
            "Low", "archive_label", False, None
        ),
        # Notification / Receipts
        (
            "service@uber.com", "Uber Receipts", "Your Sunday evening trip with Uber",
            "Total: $24.80\nDate: Aug 23, 2026\nDriver: Carlos\nPickup: 5th Avenue\nDropoff: Market Street\n\nThanks for riding with Uber. You can view your invoice anytime in the app.",
            "notification", "low", False, [], [],
            "Low", "archive_label", False, None
        ),
        # Spam / Nigerian Prince / Crypto Scam
        (
            "dr.john.okoro@nigerian-oil-board.org", "Barrister John Okoro", "Confidential Business Proposal: Transfer of $18.5M USD",
            "Dear Respected Friend,\n\nI am the personal attorney to a deceased expatriate who left funds totaling $18.5M USD with no beneficiary. I seek your partnership to claim these funds legally. You will receive 30% of total sum.\n\nPlease reply immediately with your passport copy.",
            "spam", "low", False, [], [],
            "Low", "archive_label", False, None
        ),
        # Personal / Vacation
        (
            "michael.friend@gmail.com", "Michael Chang", "Camping Trip Planning for Next Weekend",
            "Hey Alex,\n\nAre we still on for Yosemite next weekend (Sept 5-7)? Let me know if you can book the campsite by this Friday night, otherwise all spots will be taken!\n\nCheers,\nMike",
            "personal", "medium", True,
            [{"title": "Book Yosemite campsite for Sept 5-7 trip", "description": "Reserve campsite online before Friday night", "assignee": "user", "status": "pending"}],
            [{"type": "deadline", "raw_text": "this Friday night", "normalized_datetime": "2026-08-28T22:00:00", "description": "Reserve Yosemite campsite"}],
            "Medium", "create_task_and_reminder", True, "Hey Mike, yes I'm in! I'll book the campsite tonight and share the reservation details with you."
        ),
        # Work Client Contract
        (
            "elena.client@globalfirm.org", "Elena Rostova", "Contract Renewal Q4 & Feedback Form",
            "Dear Alex,\n\nWe are preparing the Q4 service contract renewal. Please complete the attached vendor feedback form and submit it to our procurement team by August 31, 2026 at 5:00 PM.\n\nKind regards,\nElena",
            "work", "high", True,
            [{"title": "Complete and submit vendor feedback form for Q4 renewal", "description": "Fill out attached procurement form and email to Elena by Aug 31", "assignee": "user", "status": "pending"}],
            [{"type": "deadline", "raw_text": "August 31, 2026 at 5:00 PM", "normalized_datetime": "2026-08-31T17:00:00", "description": "Submit vendor feedback form"}],
            "High", "create_task_and_reminder", True, "Dear Elena, thank you. I will complete the feedback form and submit it before August 31, 5:00 PM."
        ),
        # Notification CI/CD Alert
        (
            "alerts@datadog.com", "Datadog Alert", "[Warn] Memory usage > 85% on prod-worker-04",
            "Datadog Monitor Alert:\nHost: prod-worker-04\nMetric: system.mem.used > 85% for 15 mins.\nStatus: Warning\nDashboard: https://app.datadoghq.com/monitors/88219",
            "notification", "medium", False, [], [],
            "Medium", "archive_label", False, None
        ),
        # Spam Loan Offer
        (
            "fast-cash@instant-loans-preapproved.biz", "Fast Cash Loans", "Pre-approved: $50,000 Unsecured Business Loan at 0% Interest!",
            "Congratulations! You qualify for our instant pre-approved $50,000 credit line with zero collateral required. Click here now to claim your cash before the end of the day: http://instant-loans-preapproved.biz/apply",
            "spam", "low", False, [], [],
            "Low", "archive_label", False, None
        ),
        # Personal Medical Appointment
        (
            "reception@cityhealthclinic.com", "City Health Clinic", "Appointment Confirmation & Pre-visit Form",
            "Hello Alex,\n\nThis is a reminder for your annual physical exam scheduled for Thursday, September 3 at 11:00 AM.\n\nPlease complete your online medical history intake form at least 24 hours in advance by Sept 2 at 11:00 AM.\n\nClinic Staff",
            "personal", "high", True,
            [{"title": "Fill out medical history intake form for annual physical", "description": "Complete clinic intake form online 24h prior to appointment", "assignee": "user", "status": "pending"}],
            [
                {"type": "deadline", "raw_text": "Sept 2 at 11:00 AM", "normalized_datetime": "2026-09-02T11:00:00", "description": "Complete clinic pre-visit intake form"},
                {"type": "event", "raw_text": "Thursday, September 3 at 11:00 AM", "normalized_datetime": "2026-09-03T11:00:00", "description": "Annual physical appointment"}
            ],
            "High", "create_task_and_reminder", False, None
        )
    ]

    # Generate 50 items total by systematically permuting realistic business, personal, notification, and spam scenarios
    idx = 11
    while len(emails) < 50:
        for t in templates:
            sender, name, subj, body, cat, imp, is_act, tasks, deadlines, prio, act_type, req_app, draft = t
            item_time = base_time + timedelta(hours=idx, minutes=(idx * 7) % 60)
            
            is_spam = (cat == "spam")
            email_entry = {
                "email_id": f"email_{idx:03d}",
                "timestamp": item_time.isoformat(),
                "sender": sender,
                "sender_name": name,
                "recipient": "alex.dev@techcorp.io",
                "subject": f"[{cat.upper()}] {subj} #{idx}",
                "body": body,
                "ground_truth": {
                    "is_spam": is_spam,
                    "category": cat,
                    "importance": imp,
                    "is_actionable": is_act,
                    "tasks": tasks,
                    "events_deadlines": deadlines,
                    "priority": prio,
                    "recommended_action": {
                        "action_type": act_type,
                        "requires_human_approval": req_app,
                        "draft_reply": draft
                    }
                }
            }
            emails.append(email_entry)
            idx += 1
            if len(emails) >= 50:
                break
                
    return emails

if __name__ == "__main__":
    data_dir = r"C:\Users\Administrator\.gemini\antigravity\scratch\ai-email-task-assistant\dataset"
    os.makedirs(data_dir, exist_ok=True)
    
    dataset = build_benchmark_dataset()
    output_path = os.path.join(data_dir, "email_unified_benchmark.json")
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
        
    print(f"SUCCESS: Generated {len(dataset)} emails in {output_path}")
