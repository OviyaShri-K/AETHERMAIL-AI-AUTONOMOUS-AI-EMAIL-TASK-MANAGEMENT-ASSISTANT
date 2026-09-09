-- ====================================================================
-- SEED DATA: 50 BENCHMARK EMAILS, TASKS, DEADLINES & AI ACTIONS
-- ====================================================================

BEGIN;

INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (1, 'email_001', '2026-08-23T09:00:00', 'sarah.jenkins@techcorp.io', 'Sarah Jenkins', 'alex.dev@techcorp.io', 'URGENT: Q3 Financial Report Review by Tomorrow 4 PM', 'Hi Alex,

We need to finalize the Q3 Financial Report before the board meeting. Could you please review slides 12 through 25, verify the EBITDA numbers, and send me your feedback by tomorrow at 4:00 PM?

This is critical for Wednesday''s presentation.

Thanks,
Sarah', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (1, 'Review slides 12-25 of Q3 Financial Report', 'Review slides 12 through 25, verify EBITDA numbers, and send feedback to Sarah', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (1, 'deadline', 'tomorrow at 4:00 PM', '2026-08-24T16:00:00', 'Send feedback on Q3 Financial Report to Sarah');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (1, 'event', 'Wednesday', '2026-08-26T09:00:00', 'Board meeting presentation');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (1, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Sarah,

I will review slides 12-25 and verify the EBITDA figures, then get back to you with my notes before 4:00 PM tomorrow.

Best,
Alex');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_001', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: URGENT: Q3 Financial Report Review by Tomorrow 4 PM | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (2, 'email_002', '2026-08-23T10:00:00', 'david.ross@clientpartner.com', 'David Ross', 'alex.dev@techcorp.io', 'API Integration Feedback & Sync Request', 'Hello Alex,

Our engineering team tested the new webhook endpoints. Overall it looks great, but we found a timeout issue on the /v1/payments endpoint. 

Please look into the timeout issue and update the API documentation accordingly by Friday at 5 PM.

Also, let''s schedule a 30-minute sync on Thursday, Aug 27 at 2:30 PM to discuss the rollout.

Regards,
David Ross', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (2, 'Investigate /v1/payments webhook timeout issue', 'Debug timeout issue on webhook endpoints reported by David''s team', 'user', 'pending', 'High');
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (2, 'Update API documentation for webhooks', 'Update API docs for webhook endpoints by Friday 5 PM', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (2, 'deadline', 'Friday at 5 PM', '2026-08-28T17:00:00', 'Update API documentation');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (2, 'meeting', 'Thursday, Aug 27 at 2:30 PM', '2026-08-27T14:30:00', '30-minute sync with David Ross on API rollout');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (2, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi David,

Thanks for the feedback. I am investigating the /v1/payments timeout and will have the documentation updated by Friday 5 PM. Thursday at 2:30 PM works for the sync.

Best,
Alex');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_002', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: API Integration Feedback & Sync Request | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (3, 'email_003', '2026-08-23T11:00:00', 'rewards@claim-crypto-bonus-now.xyz', 'Global Reward Center', 'alex.dev@techcorp.io', 'CONGRATULATIONS! You have won $5,000 in Bitcoin! Claim within 24 hours!', 'Dear valued customer,

Your email address has been selected as the 1st prize winner of 0.15 BTC ($5,000 USD). 

Click the link below immediately to connect your wallet and withdraw your prize:
http://claim-crypto-bonus-now.xyz/claim?id=99283

Failure to claim within 24 hours will forfeit your rewards.', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (3, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_003', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: CONGRATULATIONS! You have won $5,000 in Bitcoin! Claim within 24 hours! | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (4, 'email_004', '2026-08-23T12:00:00', 'news@cloudhosting.net', 'CloudHosting Pro', 'alex.dev@techcorp.io', 'Flash Sale: 50% Off All Dedicated Cloud Instances This Weekend!', 'Hi Alex,

Upgrade your infrastructure today! For the next 48 hours only, get 50% off our Enterprise NVMe dedicated cloud servers. Use promo code FLASH50 at checkout.

Offer ends Sunday midnight.

Unsubscribe from these emails anytime by clicking here.', FALSE, 'promotional', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (4, 'event', 'Sunday midnight', '2026-08-30T23:59:59', 'Flash sale promo code FLASH50 expiration');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (4, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_004', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: Flash Sale: 50% Off All Dedicated Cloud Instances This Weekend! | Category: promotional | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (5, 'email_005', '2026-08-23T13:00:00', 'no-reply@github.com', 'GitHub Notifications', 'alex.dev@techcorp.io', '[GitHub] Run Succeeded: Deploy to Production #142', 'GitHub Actions workflow ''Production Deployment'' has completed successfully.

Commit: a8f9b1c (Merge pull request #89 from techcorp/feature-auth)
Branch: main
Duration: 4m 12s

View build logs: https://github.com/techcorp/backend/actions/runs/142', FALSE, 'notification', 'medium', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (5, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_005', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [GitHub] Run Succeeded: Deploy to Production #142 | Category: notification | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (6, 'email_006', '2026-08-23T14:00:00', 'emma.sister@gmail.com', 'Emma Wilson', 'alex.dev@techcorp.io', 'Mom''s Birthday Dinner this Saturday at 7 PM', 'Hey Alex,

We are organizing Mom''s surprise birthday dinner this Saturday at 7:00 PM at Olive Garden downtown. Can you please bring the birthday cake from Bella''s Bakery? Make sure to pick it up by 5:30 PM before they close.

Let me know if that works for you!

Love,
Emma', FALSE, 'personal', 'high', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (6, 'Pick up Mom''s birthday cake from Bella''s Bakery', 'Pick up birthday cake by 5:30 PM this Saturday for surprise dinner', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (6, 'deadline', 'Saturday by 5:30 PM', '2026-08-29T17:30:00', 'Pick up cake from bakery before closing');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (6, 'event', 'this Saturday at 7:00 PM', '2026-08-29T19:00:00', 'Mom''s surprise birthday dinner at Olive Garden');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (6, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hey Emma,

Sounds great! I''ll order and pick up the cake from Bella''s Bakery before 5:30 PM on Saturday and see you all at 7 PM.

Love,
Alex');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_006', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: Mom''s Birthday Dinner this Saturday at 7 PM | Category: personal | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (7, 'email_007', '2026-08-23T15:00:00', 'hr@techcorp.io', 'TechCorp People Operations', 'alex.dev@techcorp.io', 'Annual Cybersecurity Awareness Training - Due Sept 15', 'Dear Employee,

As part of our compliance standards, all staff members are required to complete the 2026 Annual Cybersecurity Training module.

The course takes approximately 45 minutes to complete.

Please log in to the portal and finish the module by September 15, 2026, 6:00 PM.

Link: https://learning.techcorp.io/course/sec-2026

Thank you,
People Operations', FALSE, 'work', 'medium', TRUE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (7, 'Complete Annual Cybersecurity Awareness Training', 'Finish 45-min online training module on learning portal', 'user', 'pending', 'Low');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (7, 'deadline', 'September 15, 2026, 6:00 PM', '2026-09-15T18:00:00', 'Cybersecurity compliance training due date');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (7, 'create_task_and_reminder', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_007', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: Annual Cybersecurity Awareness Training - Due Sept 15 | Category: work | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (8, 'email_008', '2026-08-23T16:00:00', 'ops-alerts@techcorp.io', 'DevOps Incident Response', 'alex.dev@techcorp.io', 'CRITICAL P0 INCIDENT: Database Connection Pool Exhausted in US-East', 'ALERT: P0 Incident #8892 opened.

Impact: 35% of incoming API requests are failing with HTTP 500 error.
Service: Payment Gateway & User Auth.

Action Required: Alex, please join the incident bridge war room immediately at https://meet.techcorp.io/war-room-p0 and deploy the hotfix within 1 hour.

Incident Commander: Marcus Vance', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (8, 'Join P0 incident war room and deploy database connection hotfix', 'Investigate connection pool exhaustion in US-East and deploy hotfix within 1 hour', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (8, 'deadline', 'within 1 hour', '2026-08-23T17:00:00', 'Deploy database hotfix to restore US-East cluster');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (8, 'meeting', 'immediately', '2026-08-23T16:00:00', 'Incident bridge war room');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (8, 'escalate', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_008', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: CRITICAL P0 INCIDENT: Database Connection Pool Exhausted in US-East | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (9, 'email_009', '2026-08-23T17:00:00', 'billing@cloudservices.com', 'CloudServices Billing', 'alex.dev@techcorp.io', 'Invoice INV-2026-881 for August Services Due in 10 Days', 'Dear Alex,

Please find attached Invoice #INV-2026-881 for the period Aug 1 - Aug 23, 2026, totaling $3,450.00.

Please approve and remit payment by September 2, 2026 to avoid late fees.

Payment Portal: https://billing.cloudservices.com/pay/881

Thank you for your business.', FALSE, 'work', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (9, 'Approve and process payment for Invoice #INV-2026-881 ($3,450.00)', 'Review CloudServices August invoice and submit for accounts payable', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (9, 'deadline', 'September 2, 2026', '2026-09-02T17:00:00', 'Payment due date for invoice INV-2026-881');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (9, 'create_task_and_reminder', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_009', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: Invoice INV-2026-881 for August Services Due in 10 Days | Category: work | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (10, 'email_010', '2026-08-23T18:00:00', 'security-alert@service-paypal-verify.net', 'PayPal Security', 'alex.dev@techcorp.io', 'Account Suspended: Verify your identity immediately', 'We detected unauthorized login attempts from IP 192.168.4.12. Your account has been temporarily restricted.

To restore your account access, click here: http://service-paypal-verify.net/restore

If you do not verify within 12 hours, your account will be permanently closed.', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (10, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_010', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: Account Suspended: Verify your identity immediately | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (11, 'email_011', '2026-08-23T20:17:00', 'rachel.pm@techcorp.io', 'Rachel Green (Product)', 'alex.dev@techcorp.io', '[WORK] Sprint 42 Backlog Grooming Action Items #11', 'Hi Alex,

Following our grooming session, please estimate story points for tickets TECH-401 through TECH-410 by tomorrow at 2:00 PM. Also, please review the PR from backend team before end of day Wednesday.

Thanks,
Rachel', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (11, 'Estimate story points for tickets TECH-401 to TECH-410', 'Add estimates in Jira by tomorrow 2 PM', 'user', 'pending', 'High');
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (11, 'Review backend team Pull Request', 'Review PR before end of day Wednesday', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (11, 'deadline', 'tomorrow at 2:00 PM', '2026-08-24T14:00:00', 'Jira ticket point estimations');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (11, 'deadline', 'end of day Wednesday', '2026-08-26T18:00:00', 'Backend PR review');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (11, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Rachel, I''ll finish the story point estimates by 2 PM tomorrow and review the PR by Wednesday. Thanks!');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_011', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Sprint 42 Backlog Grooming Action Items #11 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (12, 'email_012', '2026-08-23T21:24:00', 'sam.legal@techcorp.io', 'Samira Legal', 'alex.dev@techcorp.io', '[WORK] NDA Signature Required for Partner Alpha #12', 'Hi Alex,

Attached is the non-disclosure agreement for our upcoming partnership with Partner Alpha. Please sign and return the executed PDF by Thursday at 12:00 PM.

Best,
Samira', FALSE, 'work', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (12, 'Sign and return Partner Alpha NDA PDF', 'Sign executed NDA and email back to Samira by Thursday noon', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (12, 'deadline', 'Thursday at 12:00 PM', '2026-08-27T12:00:00', 'Signed NDA due to Legal');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (12, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Samira, received. I will sign and return the NDA before Thursday 12:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_012', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] NDA Signature Required for Partner Alpha #12 | Category: work | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (13, 'email_013', '2026-08-23T22:31:00', 'deals@techgear.shop', 'TechGear Shop', 'alex.dev@techcorp.io', '[PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #13', 'Don''t miss our biggest tech sale of the summer! Get top-tier 4K monitors, mechanical keyboards, and noise-canceling headphones at unbeatable prices.

Shop now: https://techgear.shop/deals

Sale expires Monday, Aug 31 at 11:59 PM.', FALSE, 'promotional', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (13, 'event', 'Monday, Aug 31 at 11:59 PM', '2026-08-31T23:59:00', 'TechGear sale expiration');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (13, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_013', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #13 | Category: promotional | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (14, 'email_014', '2026-08-23T23:38:00', 'service@uber.com', 'Uber Receipts', 'alex.dev@techcorp.io', '[NOTIFICATION] Your Sunday evening trip with Uber #14', 'Total: $24.80
Date: Aug 23, 2026
Driver: Carlos
Pickup: 5th Avenue
Dropoff: Market Street

Thanks for riding with Uber. You can view your invoice anytime in the app.', FALSE, 'notification', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (14, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_014', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] Your Sunday evening trip with Uber #14 | Category: notification | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (15, 'email_015', '2026-08-24T00:45:00', 'dr.john.okoro@nigerian-oil-board.org', 'Barrister John Okoro', 'alex.dev@techcorp.io', '[SPAM] Confidential Business Proposal: Transfer of $18.5M USD #15', 'Dear Respected Friend,

I am the personal attorney to a deceased expatriate who left funds totaling $18.5M USD with no beneficiary. I seek your partnership to claim these funds legally. You will receive 30% of total sum.

Please reply immediately with your passport copy.', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (15, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_015', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Confidential Business Proposal: Transfer of $18.5M USD #15 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (16, 'email_016', '2026-08-24T01:52:00', 'michael.friend@gmail.com', 'Michael Chang', 'alex.dev@techcorp.io', '[PERSONAL] Camping Trip Planning for Next Weekend #16', 'Hey Alex,

Are we still on for Yosemite next weekend (Sept 5-7)? Let me know if you can book the campsite by this Friday night, otherwise all spots will be taken!

Cheers,
Mike', FALSE, 'personal', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (16, 'Book Yosemite campsite for Sept 5-7 trip', 'Reserve campsite online before Friday night', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (16, 'deadline', 'this Friday night', '2026-08-28T22:00:00', 'Reserve Yosemite campsite');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (16, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hey Mike, yes I''m in! I''ll book the campsite tonight and share the reservation details with you.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_016', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Camping Trip Planning for Next Weekend #16 | Category: personal | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (17, 'email_017', '2026-08-24T02:59:00', 'elena.client@globalfirm.org', 'Elena Rostova', 'alex.dev@techcorp.io', '[WORK] Contract Renewal Q4 & Feedback Form #17', 'Dear Alex,

We are preparing the Q4 service contract renewal. Please complete the attached vendor feedback form and submit it to our procurement team by August 31, 2026 at 5:00 PM.

Kind regards,
Elena', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (17, 'Complete and submit vendor feedback form for Q4 renewal', 'Fill out attached procurement form and email to Elena by Aug 31', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (17, 'deadline', 'August 31, 2026 at 5:00 PM', '2026-08-31T17:00:00', 'Submit vendor feedback form');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (17, 'create_task_and_reminder', 'pending_approval', TRUE, 'Dear Elena, thank you. I will complete the feedback form and submit it before August 31, 5:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_017', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Contract Renewal Q4 & Feedback Form #17 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (18, 'email_018', '2026-08-24T03:06:00', 'alerts@datadog.com', 'Datadog Alert', 'alex.dev@techcorp.io', '[NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #18', 'Datadog Monitor Alert:
Host: prod-worker-04
Metric: system.mem.used > 85% for 15 mins.
Status: Warning
Dashboard: https://app.datadoghq.com/monitors/88219', FALSE, 'notification', 'medium', FALSE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (18, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_018', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #18 | Category: notification | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (19, 'email_019', '2026-08-24T04:13:00', 'fast-cash@instant-loans-preapproved.biz', 'Fast Cash Loans', 'alex.dev@techcorp.io', '[SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #19', 'Congratulations! You qualify for our instant pre-approved $50,000 credit line with zero collateral required. Click here now to claim your cash before the end of the day: http://instant-loans-preapproved.biz/apply', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (19, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_019', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #19 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (20, 'email_020', '2026-08-24T05:20:00', 'reception@cityhealthclinic.com', 'City Health Clinic', 'alex.dev@techcorp.io', '[PERSONAL] Appointment Confirmation & Pre-visit Form #20', 'Hello Alex,

This is a reminder for your annual physical exam scheduled for Thursday, September 3 at 11:00 AM.

Please complete your online medical history intake form at least 24 hours in advance by Sept 2 at 11:00 AM.

Clinic Staff', FALSE, 'personal', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (20, 'Fill out medical history intake form for annual physical', 'Complete clinic intake form online 24h prior to appointment', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (20, 'deadline', 'Sept 2 at 11:00 AM', '2026-09-02T11:00:00', 'Complete clinic pre-visit intake form');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (20, 'event', 'Thursday, September 3 at 11:00 AM', '2026-09-03T11:00:00', 'Annual physical appointment');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (20, 'create_task_and_reminder', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_020', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Appointment Confirmation & Pre-visit Form #20 | Category: personal | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (21, 'email_021', '2026-08-24T06:27:00', 'rachel.pm@techcorp.io', 'Rachel Green (Product)', 'alex.dev@techcorp.io', '[WORK] Sprint 42 Backlog Grooming Action Items #21', 'Hi Alex,

Following our grooming session, please estimate story points for tickets TECH-401 through TECH-410 by tomorrow at 2:00 PM. Also, please review the PR from backend team before end of day Wednesday.

Thanks,
Rachel', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (21, 'Estimate story points for tickets TECH-401 to TECH-410', 'Add estimates in Jira by tomorrow 2 PM', 'user', 'pending', 'High');
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (21, 'Review backend team Pull Request', 'Review PR before end of day Wednesday', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (21, 'deadline', 'tomorrow at 2:00 PM', '2026-08-24T14:00:00', 'Jira ticket point estimations');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (21, 'deadline', 'end of day Wednesday', '2026-08-26T18:00:00', 'Backend PR review');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (21, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Rachel, I''ll finish the story point estimates by 2 PM tomorrow and review the PR by Wednesday. Thanks!');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_021', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Sprint 42 Backlog Grooming Action Items #21 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (22, 'email_022', '2026-08-24T07:34:00', 'sam.legal@techcorp.io', 'Samira Legal', 'alex.dev@techcorp.io', '[WORK] NDA Signature Required for Partner Alpha #22', 'Hi Alex,

Attached is the non-disclosure agreement for our upcoming partnership with Partner Alpha. Please sign and return the executed PDF by Thursday at 12:00 PM.

Best,
Samira', FALSE, 'work', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (22, 'Sign and return Partner Alpha NDA PDF', 'Sign executed NDA and email back to Samira by Thursday noon', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (22, 'deadline', 'Thursday at 12:00 PM', '2026-08-27T12:00:00', 'Signed NDA due to Legal');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (22, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Samira, received. I will sign and return the NDA before Thursday 12:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_022', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] NDA Signature Required for Partner Alpha #22 | Category: work | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (23, 'email_023', '2026-08-24T08:41:00', 'deals@techgear.shop', 'TechGear Shop', 'alex.dev@techcorp.io', '[PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #23', 'Don''t miss our biggest tech sale of the summer! Get top-tier 4K monitors, mechanical keyboards, and noise-canceling headphones at unbeatable prices.

Shop now: https://techgear.shop/deals

Sale expires Monday, Aug 31 at 11:59 PM.', FALSE, 'promotional', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (23, 'event', 'Monday, Aug 31 at 11:59 PM', '2026-08-31T23:59:00', 'TechGear sale expiration');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (23, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_023', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #23 | Category: promotional | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (24, 'email_024', '2026-08-24T09:48:00', 'service@uber.com', 'Uber Receipts', 'alex.dev@techcorp.io', '[NOTIFICATION] Your Sunday evening trip with Uber #24', 'Total: $24.80
Date: Aug 23, 2026
Driver: Carlos
Pickup: 5th Avenue
Dropoff: Market Street

Thanks for riding with Uber. You can view your invoice anytime in the app.', FALSE, 'notification', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (24, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_024', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] Your Sunday evening trip with Uber #24 | Category: notification | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (25, 'email_025', '2026-08-24T10:55:00', 'dr.john.okoro@nigerian-oil-board.org', 'Barrister John Okoro', 'alex.dev@techcorp.io', '[SPAM] Confidential Business Proposal: Transfer of $18.5M USD #25', 'Dear Respected Friend,

I am the personal attorney to a deceased expatriate who left funds totaling $18.5M USD with no beneficiary. I seek your partnership to claim these funds legally. You will receive 30% of total sum.

Please reply immediately with your passport copy.', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (25, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_025', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Confidential Business Proposal: Transfer of $18.5M USD #25 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (26, 'email_026', '2026-08-24T11:02:00', 'michael.friend@gmail.com', 'Michael Chang', 'alex.dev@techcorp.io', '[PERSONAL] Camping Trip Planning for Next Weekend #26', 'Hey Alex,

Are we still on for Yosemite next weekend (Sept 5-7)? Let me know if you can book the campsite by this Friday night, otherwise all spots will be taken!

Cheers,
Mike', FALSE, 'personal', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (26, 'Book Yosemite campsite for Sept 5-7 trip', 'Reserve campsite online before Friday night', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (26, 'deadline', 'this Friday night', '2026-08-28T22:00:00', 'Reserve Yosemite campsite');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (26, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hey Mike, yes I''m in! I''ll book the campsite tonight and share the reservation details with you.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_026', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Camping Trip Planning for Next Weekend #26 | Category: personal | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (27, 'email_027', '2026-08-24T12:09:00', 'elena.client@globalfirm.org', 'Elena Rostova', 'alex.dev@techcorp.io', '[WORK] Contract Renewal Q4 & Feedback Form #27', 'Dear Alex,

We are preparing the Q4 service contract renewal. Please complete the attached vendor feedback form and submit it to our procurement team by August 31, 2026 at 5:00 PM.

Kind regards,
Elena', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (27, 'Complete and submit vendor feedback form for Q4 renewal', 'Fill out attached procurement form and email to Elena by Aug 31', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (27, 'deadline', 'August 31, 2026 at 5:00 PM', '2026-08-31T17:00:00', 'Submit vendor feedback form');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (27, 'create_task_and_reminder', 'pending_approval', TRUE, 'Dear Elena, thank you. I will complete the feedback form and submit it before August 31, 5:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_027', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Contract Renewal Q4 & Feedback Form #27 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (28, 'email_028', '2026-08-24T13:16:00', 'alerts@datadog.com', 'Datadog Alert', 'alex.dev@techcorp.io', '[NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #28', 'Datadog Monitor Alert:
Host: prod-worker-04
Metric: system.mem.used > 85% for 15 mins.
Status: Warning
Dashboard: https://app.datadoghq.com/monitors/88219', FALSE, 'notification', 'medium', FALSE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (28, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_028', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #28 | Category: notification | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (29, 'email_029', '2026-08-24T14:23:00', 'fast-cash@instant-loans-preapproved.biz', 'Fast Cash Loans', 'alex.dev@techcorp.io', '[SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #29', 'Congratulations! You qualify for our instant pre-approved $50,000 credit line with zero collateral required. Click here now to claim your cash before the end of the day: http://instant-loans-preapproved.biz/apply', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (29, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_029', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #29 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (30, 'email_030', '2026-08-24T15:30:00', 'reception@cityhealthclinic.com', 'City Health Clinic', 'alex.dev@techcorp.io', '[PERSONAL] Appointment Confirmation & Pre-visit Form #30', 'Hello Alex,

This is a reminder for your annual physical exam scheduled for Thursday, September 3 at 11:00 AM.

Please complete your online medical history intake form at least 24 hours in advance by Sept 2 at 11:00 AM.

Clinic Staff', FALSE, 'personal', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (30, 'Fill out medical history intake form for annual physical', 'Complete clinic intake form online 24h prior to appointment', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (30, 'deadline', 'Sept 2 at 11:00 AM', '2026-09-02T11:00:00', 'Complete clinic pre-visit intake form');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (30, 'event', 'Thursday, September 3 at 11:00 AM', '2026-09-03T11:00:00', 'Annual physical appointment');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (30, 'create_task_and_reminder', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_030', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Appointment Confirmation & Pre-visit Form #30 | Category: personal | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (31, 'email_031', '2026-08-24T16:37:00', 'rachel.pm@techcorp.io', 'Rachel Green (Product)', 'alex.dev@techcorp.io', '[WORK] Sprint 42 Backlog Grooming Action Items #31', 'Hi Alex,

Following our grooming session, please estimate story points for tickets TECH-401 through TECH-410 by tomorrow at 2:00 PM. Also, please review the PR from backend team before end of day Wednesday.

Thanks,
Rachel', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (31, 'Estimate story points for tickets TECH-401 to TECH-410', 'Add estimates in Jira by tomorrow 2 PM', 'user', 'pending', 'High');
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (31, 'Review backend team Pull Request', 'Review PR before end of day Wednesday', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (31, 'deadline', 'tomorrow at 2:00 PM', '2026-08-24T14:00:00', 'Jira ticket point estimations');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (31, 'deadline', 'end of day Wednesday', '2026-08-26T18:00:00', 'Backend PR review');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (31, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Rachel, I''ll finish the story point estimates by 2 PM tomorrow and review the PR by Wednesday. Thanks!');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_031', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Sprint 42 Backlog Grooming Action Items #31 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (32, 'email_032', '2026-08-24T17:44:00', 'sam.legal@techcorp.io', 'Samira Legal', 'alex.dev@techcorp.io', '[WORK] NDA Signature Required for Partner Alpha #32', 'Hi Alex,

Attached is the non-disclosure agreement for our upcoming partnership with Partner Alpha. Please sign and return the executed PDF by Thursday at 12:00 PM.

Best,
Samira', FALSE, 'work', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (32, 'Sign and return Partner Alpha NDA PDF', 'Sign executed NDA and email back to Samira by Thursday noon', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (32, 'deadline', 'Thursday at 12:00 PM', '2026-08-27T12:00:00', 'Signed NDA due to Legal');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (32, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Samira, received. I will sign and return the NDA before Thursday 12:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_032', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] NDA Signature Required for Partner Alpha #32 | Category: work | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (33, 'email_033', '2026-08-24T18:51:00', 'deals@techgear.shop', 'TechGear Shop', 'alex.dev@techcorp.io', '[PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #33', 'Don''t miss our biggest tech sale of the summer! Get top-tier 4K monitors, mechanical keyboards, and noise-canceling headphones at unbeatable prices.

Shop now: https://techgear.shop/deals

Sale expires Monday, Aug 31 at 11:59 PM.', FALSE, 'promotional', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (33, 'event', 'Monday, Aug 31 at 11:59 PM', '2026-08-31T23:59:00', 'TechGear sale expiration');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (33, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_033', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #33 | Category: promotional | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (34, 'email_034', '2026-08-24T19:58:00', 'service@uber.com', 'Uber Receipts', 'alex.dev@techcorp.io', '[NOTIFICATION] Your Sunday evening trip with Uber #34', 'Total: $24.80
Date: Aug 23, 2026
Driver: Carlos
Pickup: 5th Avenue
Dropoff: Market Street

Thanks for riding with Uber. You can view your invoice anytime in the app.', FALSE, 'notification', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (34, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_034', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] Your Sunday evening trip with Uber #34 | Category: notification | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (35, 'email_035', '2026-08-24T20:05:00', 'dr.john.okoro@nigerian-oil-board.org', 'Barrister John Okoro', 'alex.dev@techcorp.io', '[SPAM] Confidential Business Proposal: Transfer of $18.5M USD #35', 'Dear Respected Friend,

I am the personal attorney to a deceased expatriate who left funds totaling $18.5M USD with no beneficiary. I seek your partnership to claim these funds legally. You will receive 30% of total sum.

Please reply immediately with your passport copy.', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (35, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_035', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Confidential Business Proposal: Transfer of $18.5M USD #35 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (36, 'email_036', '2026-08-24T21:12:00', 'michael.friend@gmail.com', 'Michael Chang', 'alex.dev@techcorp.io', '[PERSONAL] Camping Trip Planning for Next Weekend #36', 'Hey Alex,

Are we still on for Yosemite next weekend (Sept 5-7)? Let me know if you can book the campsite by this Friday night, otherwise all spots will be taken!

Cheers,
Mike', FALSE, 'personal', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (36, 'Book Yosemite campsite for Sept 5-7 trip', 'Reserve campsite online before Friday night', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (36, 'deadline', 'this Friday night', '2026-08-28T22:00:00', 'Reserve Yosemite campsite');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (36, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hey Mike, yes I''m in! I''ll book the campsite tonight and share the reservation details with you.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_036', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Camping Trip Planning for Next Weekend #36 | Category: personal | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (37, 'email_037', '2026-08-24T22:19:00', 'elena.client@globalfirm.org', 'Elena Rostova', 'alex.dev@techcorp.io', '[WORK] Contract Renewal Q4 & Feedback Form #37', 'Dear Alex,

We are preparing the Q4 service contract renewal. Please complete the attached vendor feedback form and submit it to our procurement team by August 31, 2026 at 5:00 PM.

Kind regards,
Elena', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (37, 'Complete and submit vendor feedback form for Q4 renewal', 'Fill out attached procurement form and email to Elena by Aug 31', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (37, 'deadline', 'August 31, 2026 at 5:00 PM', '2026-08-31T17:00:00', 'Submit vendor feedback form');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (37, 'create_task_and_reminder', 'pending_approval', TRUE, 'Dear Elena, thank you. I will complete the feedback form and submit it before August 31, 5:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_037', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Contract Renewal Q4 & Feedback Form #37 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (38, 'email_038', '2026-08-24T23:26:00', 'alerts@datadog.com', 'Datadog Alert', 'alex.dev@techcorp.io', '[NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #38', 'Datadog Monitor Alert:
Host: prod-worker-04
Metric: system.mem.used > 85% for 15 mins.
Status: Warning
Dashboard: https://app.datadoghq.com/monitors/88219', FALSE, 'notification', 'medium', FALSE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (38, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_038', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #38 | Category: notification | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (39, 'email_039', '2026-08-25T00:33:00', 'fast-cash@instant-loans-preapproved.biz', 'Fast Cash Loans', 'alex.dev@techcorp.io', '[SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #39', 'Congratulations! You qualify for our instant pre-approved $50,000 credit line with zero collateral required. Click here now to claim your cash before the end of the day: http://instant-loans-preapproved.biz/apply', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (39, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_039', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #39 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (40, 'email_040', '2026-08-25T01:40:00', 'reception@cityhealthclinic.com', 'City Health Clinic', 'alex.dev@techcorp.io', '[PERSONAL] Appointment Confirmation & Pre-visit Form #40', 'Hello Alex,

This is a reminder for your annual physical exam scheduled for Thursday, September 3 at 11:00 AM.

Please complete your online medical history intake form at least 24 hours in advance by Sept 2 at 11:00 AM.

Clinic Staff', FALSE, 'personal', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (40, 'Fill out medical history intake form for annual physical', 'Complete clinic intake form online 24h prior to appointment', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (40, 'deadline', 'Sept 2 at 11:00 AM', '2026-09-02T11:00:00', 'Complete clinic pre-visit intake form');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (40, 'event', 'Thursday, September 3 at 11:00 AM', '2026-09-03T11:00:00', 'Annual physical appointment');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (40, 'create_task_and_reminder', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_040', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Appointment Confirmation & Pre-visit Form #40 | Category: personal | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (41, 'email_041', '2026-08-25T02:47:00', 'rachel.pm@techcorp.io', 'Rachel Green (Product)', 'alex.dev@techcorp.io', '[WORK] Sprint 42 Backlog Grooming Action Items #41', 'Hi Alex,

Following our grooming session, please estimate story points for tickets TECH-401 through TECH-410 by tomorrow at 2:00 PM. Also, please review the PR from backend team before end of day Wednesday.

Thanks,
Rachel', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (41, 'Estimate story points for tickets TECH-401 to TECH-410', 'Add estimates in Jira by tomorrow 2 PM', 'user', 'pending', 'High');
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (41, 'Review backend team Pull Request', 'Review PR before end of day Wednesday', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (41, 'deadline', 'tomorrow at 2:00 PM', '2026-08-24T14:00:00', 'Jira ticket point estimations');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (41, 'deadline', 'end of day Wednesday', '2026-08-26T18:00:00', 'Backend PR review');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (41, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Rachel, I''ll finish the story point estimates by 2 PM tomorrow and review the PR by Wednesday. Thanks!');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_041', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Sprint 42 Backlog Grooming Action Items #41 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (42, 'email_042', '2026-08-25T03:54:00', 'sam.legal@techcorp.io', 'Samira Legal', 'alex.dev@techcorp.io', '[WORK] NDA Signature Required for Partner Alpha #42', 'Hi Alex,

Attached is the non-disclosure agreement for our upcoming partnership with Partner Alpha. Please sign and return the executed PDF by Thursday at 12:00 PM.

Best,
Samira', FALSE, 'work', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (42, 'Sign and return Partner Alpha NDA PDF', 'Sign executed NDA and email back to Samira by Thursday noon', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (42, 'deadline', 'Thursday at 12:00 PM', '2026-08-27T12:00:00', 'Signed NDA due to Legal');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (42, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hi Samira, received. I will sign and return the NDA before Thursday 12:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_042', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] NDA Signature Required for Partner Alpha #42 | Category: work | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (43, 'email_043', '2026-08-25T04:01:00', 'deals@techgear.shop', 'TechGear Shop', 'alex.dev@techcorp.io', '[PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #43', 'Don''t miss our biggest tech sale of the summer! Get top-tier 4K monitors, mechanical keyboards, and noise-canceling headphones at unbeatable prices.

Shop now: https://techgear.shop/deals

Sale expires Monday, Aug 31 at 11:59 PM.', FALSE, 'promotional', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (43, 'event', 'Monday, Aug 31 at 11:59 PM', '2026-08-31T23:59:00', 'TechGear sale expiration');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (43, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_043', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PROMOTIONAL] Back to School Tech Deals - Up to 40% Off Laptops & Monitors #43 | Category: promotional | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (44, 'email_044', '2026-08-25T05:08:00', 'service@uber.com', 'Uber Receipts', 'alex.dev@techcorp.io', '[NOTIFICATION] Your Sunday evening trip with Uber #44', 'Total: $24.80
Date: Aug 23, 2026
Driver: Carlos
Pickup: 5th Avenue
Dropoff: Market Street

Thanks for riding with Uber. You can view your invoice anytime in the app.', FALSE, 'notification', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (44, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_044', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] Your Sunday evening trip with Uber #44 | Category: notification | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (45, 'email_045', '2026-08-25T06:15:00', 'dr.john.okoro@nigerian-oil-board.org', 'Barrister John Okoro', 'alex.dev@techcorp.io', '[SPAM] Confidential Business Proposal: Transfer of $18.5M USD #45', 'Dear Respected Friend,

I am the personal attorney to a deceased expatriate who left funds totaling $18.5M USD with no beneficiary. I seek your partnership to claim these funds legally. You will receive 30% of total sum.

Please reply immediately with your passport copy.', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (45, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_045', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Confidential Business Proposal: Transfer of $18.5M USD #45 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (46, 'email_046', '2026-08-25T07:22:00', 'michael.friend@gmail.com', 'Michael Chang', 'alex.dev@techcorp.io', '[PERSONAL] Camping Trip Planning for Next Weekend #46', 'Hey Alex,

Are we still on for Yosemite next weekend (Sept 5-7)? Let me know if you can book the campsite by this Friday night, otherwise all spots will be taken!

Cheers,
Mike', FALSE, 'personal', 'medium', TRUE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (46, 'Book Yosemite campsite for Sept 5-7 trip', 'Reserve campsite online before Friday night', 'user', 'pending', 'Medium');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (46, 'deadline', 'this Friday night', '2026-08-28T22:00:00', 'Reserve Yosemite campsite');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (46, 'create_task_and_reminder', 'pending_approval', TRUE, 'Hey Mike, yes I''m in! I''ll book the campsite tonight and share the reservation details with you.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_046', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Camping Trip Planning for Next Weekend #46 | Category: personal | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (47, 'email_047', '2026-08-25T08:29:00', 'elena.client@globalfirm.org', 'Elena Rostova', 'alex.dev@techcorp.io', '[WORK] Contract Renewal Q4 & Feedback Form #47', 'Dear Alex,

We are preparing the Q4 service contract renewal. Please complete the attached vendor feedback form and submit it to our procurement team by August 31, 2026 at 5:00 PM.

Kind regards,
Elena', FALSE, 'work', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (47, 'Complete and submit vendor feedback form for Q4 renewal', 'Fill out attached procurement form and email to Elena by Aug 31', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (47, 'deadline', 'August 31, 2026 at 5:00 PM', '2026-08-31T17:00:00', 'Submit vendor feedback form');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (47, 'create_task_and_reminder', 'pending_approval', TRUE, 'Dear Elena, thank you. I will complete the feedback form and submit it before August 31, 5:00 PM.');
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_047', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [WORK] Contract Renewal Q4 & Feedback Form #47 | Category: work | Priority: High');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (48, 'email_048', '2026-08-25T09:36:00', 'alerts@datadog.com', 'Datadog Alert', 'alex.dev@techcorp.io', '[NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #48', 'Datadog Monitor Alert:
Host: prod-worker-04
Metric: system.mem.used > 85% for 15 mins.
Status: Warning
Dashboard: https://app.datadoghq.com/monitors/88219', FALSE, 'notification', 'medium', FALSE, 'Medium') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (48, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_048', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [NOTIFICATION] [Warn] Memory usage > 85% on prod-worker-04 #48 | Category: notification | Priority: Medium');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (49, 'email_049', '2026-08-25T10:43:00', 'fast-cash@instant-loans-preapproved.biz', 'Fast Cash Loans', 'alex.dev@techcorp.io', '[SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #49', 'Congratulations! You qualify for our instant pre-approved $50,000 credit line with zero collateral required. Click here now to claim your cash before the end of the day: http://instant-loans-preapproved.biz/apply', TRUE, 'spam', 'low', FALSE, 'Low') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (49, 'archive_label', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_049', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [SPAM] Pre-approved: $50,000 Unsecured Business Loan at 0% Interest! #49 | Category: spam | Priority: Low');
INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES (50, 'email_050', '2026-08-25T11:50:00', 'reception@cityhealthclinic.com', 'City Health Clinic', 'alex.dev@techcorp.io', '[PERSONAL] Appointment Confirmation & Pre-visit Form #50', 'Hello Alex,

This is a reminder for your annual physical exam scheduled for Thursday, September 3 at 11:00 AM.

Please complete your online medical history intake form at least 24 hours in advance by Sept 2 at 11:00 AM.

Clinic Staff', FALSE, 'personal', 'high', TRUE, 'High') ON CONFLICT (email_id) DO NOTHING;
INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES (50, 'Fill out medical history intake form for annual physical', 'Complete clinic intake form online 24h prior to appointment', 'user', 'pending', 'High');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (50, 'deadline', 'Sept 2 at 11:00 AM', '2026-09-02T11:00:00', 'Complete clinic pre-visit intake form');
INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES (50, 'event', 'Thursday, September 3 at 11:00 AM', '2026-09-03T11:00:00', 'Annual physical appointment');
INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES (50, 'create_task_and_reminder', 'executed', FALSE, NULL);
INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', 'email_050', 'INGESTED_AND_ANALYZED', 'AI_AGENT', 'Ingested email: [PERSONAL] Appointment Confirmation & Pre-visit Form #50 | Category: personal | Priority: High');

COMMIT;
