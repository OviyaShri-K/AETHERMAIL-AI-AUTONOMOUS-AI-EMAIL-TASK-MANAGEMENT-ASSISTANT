import json
import os
from datetime import datetime

def generate_sql_seed():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    
    json_path = os.path.join(project_root, "dataset", "email_unified_benchmark.json")
    sql_path = os.path.join(project_root, "backend", "supabase_seed_data.sql")
    
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    sql_lines = [
        "-- ====================================================================",
        "-- SEED DATA: 50 BENCHMARK EMAILS, TASKS, DEADLINES & AI ACTIONS",
        "-- ====================================================================\n",
        "BEGIN;\n"
    ]
    
    for idx, item in enumerate(data, start=1):
        gt = item["ground_truth"]
        
        def esc(val):
            if val is None:
                return "NULL"
            return "'" + str(val).replace("'", "''") + "'"
            
        subj_esc = esc(item['subject'])
        body_esc = esc(item['body'])
        sender_esc = esc(item['sender'])
        sender_name_esc = esc(item.get('sender_name', ''))
        recip_esc = esc(item.get('recipient', 'alex.dev@techcorp.io'))
        ts_esc = esc(item['timestamp'])
        
        is_spam_str = "TRUE" if gt['is_spam'] else "FALSE"
        cat_esc = esc(gt['category'])
        imp_esc = esc(gt['importance'])
        is_act_str = "TRUE" if gt['is_actionable'] else "FALSE"
        prio_esc = esc(gt['priority'])
        
        # 1. Insert Email
        sql_lines.append(f"INSERT INTO emails (id, email_id, timestamp, sender, sender_name, recipient, subject, body, is_spam, category, importance, is_actionable, priority) VALUES ({idx}, {esc(item['email_id'])}, {ts_esc}, {sender_esc}, {sender_name_esc}, {recip_esc}, {subj_esc}, {body_esc}, {is_spam_str}, {cat_esc}, {imp_esc}, {is_act_str}, {prio_esc}) ON CONFLICT (email_id) DO NOTHING;")
        
        # 2. Insert Tasks
        tasks = gt.get("tasks", [])
        for t in tasks:
            t_title = esc(t['title'])
            t_desc = esc(t.get('description', ''))
            t_assignee = esc(t.get('assignee', 'user'))
            t_status = esc(t.get('status', 'pending'))
            sql_lines.append(f"INSERT INTO tasks (email_id, title, description, assignee, status, priority) VALUES ({idx}, {t_title}, {t_desc}, {t_assignee}, {t_status}, {prio_esc});")
            
        # 3. Insert Deadlines
        deadlines = gt.get("events_deadlines", [])
        for d in deadlines:
            d_type = esc(d.get('type', 'deadline'))
            d_raw = esc(d.get('raw_text', ''))
            d_norm = esc(d.get('normalized_datetime'))
            d_desc = esc(d.get('description', ''))
            sql_lines.append(f"INSERT INTO deadlines_events (email_id, event_type, raw_text, normalized_datetime, description) VALUES ({idx}, {d_type}, {d_raw}, {d_norm}, {d_desc});")
            
        # 4. Insert AI Actions
        rec_act = gt.get("recommended_action", {})
        act_type = esc(rec_act.get('action_type', 'none'))
        req_appr = "TRUE" if rec_act.get('requires_human_approval') else "FALSE"
        act_status = "'pending_approval'" if rec_act.get('requires_human_approval') else "'executed'"
        draft_esc = esc(rec_act.get('draft_reply'))
        sql_lines.append(f"INSERT INTO ai_actions (email_id, action_type, status, requires_human_approval, draft_reply) VALUES ({idx}, {act_type}, {act_status}, {req_appr}, {draft_esc});")
        
        # 5. Insert Audit Log
        details_esc = esc(f"Ingested email: {item['subject']} | Category: {gt['category']} | Priority: {gt['priority']}")
        sql_lines.append(f"INSERT INTO audit_logs (entity_type, entity_id, action, performed_by, details) VALUES ('EMAIL', {esc(item['email_id'])}, 'INGESTED_AND_ANALYZED', 'AI_AGENT', {details_esc});")
        
    sql_lines.append("\nCOMMIT;\n")
    
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("\n".join(sql_lines))
        
    print(f"SUCCESS: Generated full SQL seed file with {len(data)} emails at: {sql_path}")

if __name__ == "__main__":
    generate_sql_seed()
