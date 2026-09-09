-- ====================================================================
-- SUPABASE POSTGRESQL SCHEMA: AI EMAIL & TASK MANAGEMENT ASSISTANT
-- ====================================================================

-- 1. Table: Emails
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email_id VARCHAR(100) UNIQUE NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    sender VARCHAR(255) NOT NULL,
    sender_name VARCHAR(255),
    recipient VARCHAR(255) DEFAULT 'user@company.com' NOT NULL,
    subject VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    is_spam BOOLEAN DEFAULT FALSE NOT NULL,
    category VARCHAR(50) DEFAULT 'work' NOT NULL,
    importance VARCHAR(50) DEFAULT 'medium' NOT NULL,
    is_actionable BOOLEAN DEFAULT FALSE NOT NULL,
    priority VARCHAR(50) DEFAULT 'Medium' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. Table: Tasks
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    assignee VARCHAR(100) DEFAULT 'user' NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' NOT NULL, -- pending, in_progress, completed, cancelled
    priority VARCHAR(50) DEFAULT 'Medium' NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. Table: Deadlines & Events
CREATE TABLE IF NOT EXISTS deadlines_events (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id) ON DELETE CASCADE NOT NULL,
    task_id INTEGER REFERENCES tasks(id) ON DELETE SET NULL,
    event_type VARCHAR(50) DEFAULT 'deadline' NOT NULL, -- deadline, event, meeting, reminder
    raw_text VARCHAR(255) NOT NULL,
    normalized_datetime TIMESTAMP WITH TIME ZONE,
    description VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. Table: AI Actions & Human Approvals
CREATE TABLE IF NOT EXISTS ai_actions (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id) ON DELETE CASCADE NOT NULL,
    action_type VARCHAR(100) DEFAULT 'none' NOT NULL, -- create_task_and_reminder, archive_label, escalate
    status VARCHAR(50) DEFAULT 'pending_approval' NOT NULL, -- pending_approval, approved, rejected, executed
    requires_human_approval BOOLEAN DEFAULT FALSE NOT NULL,
    draft_reply TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE
);

-- 5. Table: Audit Logs
CREATE TABLE IF NOT EXISTS audit_logs (
    id SERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL, -- EMAIL, TASK, ACTION, APPROVAL
    entity_id VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL, -- INGESTED_AND_ANALYZED, STATUS_UPDATED, APPROVED, REJECTED
    performed_by VARCHAR(50) DEFAULT 'AI_AGENT' NOT NULL, -- AI_AGENT, USER
    details TEXT,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Create Indexes for High-Performance Querying
CREATE INDEX IF NOT EXISTS idx_emails_category ON emails(category);
CREATE INDEX IF NOT EXISTS idx_emails_priority ON emails(priority);
CREATE INDEX IF NOT EXISTS idx_emails_is_spam ON emails(is_spam);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_actions_status ON ai_actions(status);
