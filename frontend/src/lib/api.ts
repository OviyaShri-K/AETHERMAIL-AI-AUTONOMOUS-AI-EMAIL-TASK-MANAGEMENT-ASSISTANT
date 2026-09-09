import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json",
  },
});

export interface UserProfile {
  email: string;
  name: string;
  role: string;
  avatar: string;
  email_count: number;
  task_count: number;
  pending_approvals: number;
  last_active: string;
  is_authenticated: boolean;
}

export interface EmailItem {
  id: number;
  email_id: string;
  timestamp: string;
  sender: string;
  sender_name?: string;
  recipient: string;
  subject: string;
  body: string;
  is_spam: boolean;
  category: string;
  importance: string;
  is_actionable: boolean;
  priority: string;
  draft_reply?: string;
  tasks?: TaskItem[];
  deadlines?: DeadlineItem[];
  attachments?: AttachmentItem[];
}

export interface TaskItem {
  id: number;
  email_id: number;
  title: string;
  description?: string;
  assignee: string;
  status: "pending" | "in_progress" | "completed" | "cancelled" | string;
  priority: "High" | "Medium" | "Low" | string;
  deadline?: string;
  created_at: string;
  updated_at: string;
}

export interface DeadlineItem {
  id: number;
  email_id: number;
  task_id?: number;
  event_type: string;
  raw_text: string;
  normalized_datetime?: string;
  description?: string;
}

export interface ActionItem {
  id: number;
  email_id: number;
  email_subject?: string;
  sender?: string;
  category?: string;
  action_type: string;
  status: "pending_approval" | "approved" | "rejected" | "executed" | string;
  requires_human_approval: boolean;
  draft_reply?: string;
  created_at: string;
  executed_at?: string;
}

export interface AttachmentItem {
  id: number;
  email_id?: number;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  cloudinary_url: string;
  uploaded_at: string;
}

export interface DashboardMetrics {
  user_filter?: string;
  overview: {
    total_emails: number;
    spam_count: number;
    ham_count: number;
    total_tasks: number;
    pending_tasks: number;
    in_progress_tasks: number;
    completed_tasks: number;
    pending_approvals: number;
    total_deadlines: number;
  };
  category_distribution: Record<string, number>;
  priority_distribution: Record<string, number>;
  ai_benchmark_accuracy: {
    overall_accuracy: number;
    target_accuracy: string;
    status: string;
  };
}

// User APIs
export const fetchUsersDirectory = async (): Promise<UserProfile[]> => {
  const res = await apiClient.get<UserProfile[]>("/users");
  return res.data;
};

export const loginOrSwitchUser = async (
  email: string,
  name?: string,
  auth_type: string = "instant",
  password?: string
): Promise<UserProfile> => {
  const res = await apiClient.post<UserProfile>("/users/login", {
    email,
    name,
    auth_type,
    password,
  });
  return res.data;
};

// Email APIs
export const fetchEmails = async (params?: {
  user_email?: string;
  category?: string;
  is_spam?: boolean;
  priority?: string;
}): Promise<EmailItem[]> => {
  const res = await apiClient.get<EmailItem[]>("/emails", { params });
  return res.data;
};

export const fetchEmailById = async (id: string | number): Promise<EmailItem> => {
  const res = await apiClient.get<EmailItem>(`/emails/${id}`);
  return res.data;
};

export const processNewEmail = async (payload: {
  sender: string;
  sender_name?: string;
  recipient: string;
  subject: string;
  body: string;
  timestamp?: string;
}): Promise<{ success: boolean; email: EmailItem; ai_decision_summary: string }> => {
  const res = await apiClient.post("/emails/process-new", payload);
  return res.data;
};

// Task APIs
export const fetchTasks = async (params?: {
  user_email?: string;
  status?: string;
  priority?: string;
}): Promise<TaskItem[]> => {
  const res = await apiClient.get<TaskItem[]>("/tasks", { params });
  return res.data;
};

export const createCustomTask = async (payload: {
  email_id?: number;
  recipient?: string;
  description: string;
}): Promise<TaskItem> => {
  const res = await apiClient.post<TaskItem>("/tasks", payload);
  return res.data;
};

export const updateTaskStatus = async (
  id: number,
  payload: { status?: string; priority?: string; title?: string; description?: string }
): Promise<TaskItem> => {
  const res = await apiClient.put<TaskItem>(`/tasks/${id}`, payload);
  return res.data;
};

export const deleteTaskById = async (id: number): Promise<{ success: boolean }> => {
  const res = await apiClient.delete(`/tasks/${id}`);
  return res.data;
};

// Approvals APIs
export const fetchApprovals = async (params?: {
  user_email?: string;
  status?: string;
}): Promise<{
  status_filter: string;
  count: number;
  total_in_db: number;
  actions: ActionItem[];
}> => {
  const res = await apiClient.get("/approvals", { params });
  return res.data;
};

export const decideApproval = async (
  actionId: number,
  decision: "approve" | "reject",
  custom_draft_reply?: string
): Promise<any> => {
  const res = await apiClient.post(`/approvals/${actionId}/decide`, {
    decision,
    custom_draft_reply,
  });
  return res.data;
};

export const authorizeApprovalAction = async (actionId: number, customDraft?: string): Promise<any> => {
  return decideApproval(actionId, "approve", customDraft);
};

export const rejectApprovalAction = async (actionId: number, reason?: string): Promise<any> => {
  return decideApproval(actionId, "reject");
};

export type ApprovalItem = ActionItem;

// Attachments APIs
export const fetchAttachments = async (email_id?: number): Promise<AttachmentItem[]> => {
  const res = await apiClient.get<AttachmentItem[]>("/attachments", {
    params: { email_id },
  });
  return res.data;
};

export const uploadAttachment = async (file: File, email_id?: number): Promise<any> => {
  const formData = new FormData();
  formData.append("file", file);
  if (email_id) {
    formData.append("email_id", String(email_id));
  }
  const res = await apiClient.post("/attachments/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return res.data;
};

export const uploadAttachmentToCloudinary = uploadAttachment;

// Analytics & Sync APIs
export const fetchDashboardMetrics = async (user_email?: string): Promise<DashboardMetrics> => {
  const res = await apiClient.get<DashboardMetrics>("/analytics/metrics", {
    params: { user_email },
  });
  return res.data;
};

export const syncGmailInbox = async (user_email?: string): Promise<any> => {
  const res = await apiClient.post("/gmail/sync", null, {
    params: { user_email },
  });
  return res.data;
};

export const fetchGoogleOAuthUrl = async (): Promise<{ configured: boolean; url: string }> => {
  const res = await apiClient.get("/gmail/oauth-url");
  return res.data;
};

export const googleSignIn = async (email?: string): Promise<any> => {
  const res = await apiClient.post("/gmail/google-signin", { email });
  return res.data;
};

export const connectGmail = async (email: string, password?: string): Promise<any> => {
  const res = await apiClient.post("/gmail/connect", { email, password, app_password: password });
  return res.data;
};

export const fetchConnectedAccounts = async (): Promise<any[]> => {
  const res = await apiClient.get("/gmail/accounts");
  return res.data;
};

export const fetchSystemHealth = async (): Promise<any> => {
  const res = await apiClient.get("/health");
  return res.data;
};

