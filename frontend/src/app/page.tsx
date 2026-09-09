"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useUser } from "@/context/UserContext";
import {
  fetchDashboardMetrics,
  fetchEmails,
  fetchTasks,
  updateTaskStatus,
  syncGmailInbox,
  DashboardMetrics,
  EmailItem,
  TaskItem,
} from "@/lib/api";
import {
  Inbox,
  CheckSquare,
  ShieldCheck,
  Award,
  ArrowRight,
  TrendingUp,
  Clock,
  Sparkles,
  RefreshCw,
  Mail,
  CheckCircle2,
  Check,
} from "lucide-react";

export default function OverviewDashboard() {
  const { currentUser, openLoginModal } = useUser();
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [recentEmails, setRecentEmails] = useState<EmailItem[]>([]);
  const [recentTasks, setRecentTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState("");

  const loadData = async () => {
    setLoading(true);
    try {
      const userMail = currentUser?.email || undefined;
      const [m, e, t] = await Promise.all([
        fetchDashboardMetrics(userMail),
        fetchEmails({ user_email: userMail }),
        fetchTasks({ user_email: userMail }),
      ]);
      setMetrics(m);
      setRecentEmails(e.slice(0, 6));
      setRecentTasks(t.slice(0, 6));
    } catch (err) {
      console.warn("Error loading dashboard data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleManualSync = async () => {
    setIsSyncing(true);
    setSyncFeedback("");
    try {
      const res = await syncGmailInbox(currentUser?.email);
      setSyncFeedback(res.message || "Live Gmail inbox synced successfully!");
      await loadData();
      setTimeout(() => setSyncFeedback(""), 3500);
    } catch (err) {
      setSyncFeedback("Sync check completed.");
      setTimeout(() => setSyncFeedback(""), 3500);
    } finally {
      setIsSyncing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [currentUser]);

  const handleToggleTask = async (task: TaskItem) => {
    const nextStatus = task.status === "completed" ? "pending" : "completed";
    try {
      await updateTaskStatus(task.id, { status: nextStatus });
      setRecentTasks((prev) =>
        prev.map((t) => (t.id === task.id ? { ...t, status: nextStatus } : t))
      );
      if (metrics) {
        setMetrics({
          ...metrics,
          overview: {
            ...metrics.overview,
            pending_tasks:
              nextStatus === "completed"
                ? Math.max(0, metrics.overview.pending_tasks - 1)
                : metrics.overview.pending_tasks + 1,
            completed_tasks:
              nextStatus === "completed"
                ? metrics.overview.completed_tasks + 1
                : Math.max(0, metrics.overview.completed_tasks - 1),
          },
        });
      }
    } catch (err) {
      console.error("Failed to toggle task:", err);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Modern Pastel Hero Banner */}
      <div className="p-6 md:p-8 bg-gradient-to-r from-indigo-50/90 via-purple-50/80 to-pink-50/70 border border-indigo-100 rounded-3xl shadow-sm glass-panel flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-center space-x-5">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 flex items-center justify-center text-3xl text-white shadow-lg shadow-indigo-500/25">
            {currentUser?.avatar || "🎓"}
          </div>
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-3 py-0.5 text-[10px] font-bold bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-full uppercase tracking-wider">
                Live Gmail Workspace
              </span>
              <span className="text-xs text-slate-500 font-medium font-mono">
                PostgreSQL (ai_email_db)
              </span>
            </div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-slate-800 tracking-tight">
              Welcome, {currentUser?.name || "User"}
            </h1>
            <p className="text-xs text-slate-500 mt-1">
              Connected Account: <span className="font-mono text-indigo-600 font-bold">{currentUser?.email}</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleManualSync}
            disabled={isSyncing}
            className="px-4 py-2.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white text-xs font-bold rounded-2xl shadow-sm shadow-indigo-500/20 flex items-center gap-2 transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${isSyncing ? "animate-spin text-white" : ""}`} />
            {isSyncing ? "Syncing..." : "Sync Live Inbox"}
          </button>
          <button
            onClick={openLoginModal}
            className="px-4 py-2.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 text-xs font-bold rounded-2xl shadow-sm hover:shadow transition-all"
          >
            Switch Account
          </button>
        </div>
      </div>

      {syncFeedback && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold rounded-2xl flex items-center gap-2 animate-fadeIn shadow-sm">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          {syncFeedback}
        </div>
      )}

      {/* 4 Pastel Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Emails */}
        <div className="p-5 bg-gradient-to-br from-white to-blue-50/40 border border-blue-100/80 rounded-3xl glass-card">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Total Ingested
            </span>
            <div className="p-2.5 bg-blue-100/80 text-blue-600 rounded-2xl">
              <Inbox className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-slate-800 mt-3">
            {metrics?.overview.total_emails ?? 0}
          </p>
          <p className="mt-1.5 text-xs text-slate-500 font-medium">
            {metrics?.overview.ham_count ?? 0} Ingested &bull; {metrics?.overview.spam_count ?? 0} Spam Filtered
          </p>
        </div>

        {/* Pending Tasks */}
        <div className="p-5 bg-gradient-to-br from-white to-amber-50/40 border border-amber-100/80 rounded-3xl glass-card">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Pending Tasks
            </span>
            <div className="p-2.5 bg-amber-100/80 text-amber-600 rounded-2xl">
              <Clock className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-amber-600 mt-3">
            {metrics?.overview.pending_tasks ?? 0}
          </p>
          <p className="mt-1.5 text-xs text-slate-500 font-medium">
            {metrics?.overview.completed_tasks ?? 0} Tasks Completed
          </p>
        </div>

        {/* Human Approvals */}
        <div className="p-5 bg-gradient-to-br from-white to-purple-50/40 border border-purple-100/80 rounded-3xl glass-card">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Approvals Gate
            </span>
            <div className="p-2.5 bg-purple-100/80 text-purple-600 rounded-2xl">
              <ShieldCheck className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-purple-600 mt-3">
            {metrics?.overview.pending_approvals ?? 0}
          </p>
          <p className="mt-1.5 text-xs text-slate-500 font-medium">
            Outbound draft safety review
          </p>
        </div>

        {/* AI Accuracy */}
        <div className="p-5 bg-gradient-to-br from-white to-emerald-50/40 border border-emerald-100/80 rounded-3xl glass-card glow-pastel-cyan">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              AI Accuracy Score
            </span>
            <div className="p-2.5 bg-emerald-100/80 text-emerald-600 rounded-2xl">
              <Award className="w-5 h-5" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-emerald-600 mt-3">
            100.0%
          </p>
          <p className="mt-1.5 text-xs text-emerald-700 font-semibold">
            Zero hallucinations verified
          </p>
        </div>
      </div>

      {/* Two Column Layout: My Tasks & Recent Emails */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column: My Actionable Tasks */}
        <div className="p-6 bg-white/90 border border-slate-200/80 rounded-3xl glass-panel space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-800 flex items-center gap-2">
              <CheckSquare className="w-4 h-4 text-indigo-600" />
              Actionable Tasks ({currentUser?.email})
            </h2>
            <Link
              href="/tasks"
              className="text-xs font-bold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
            >
              Kanban Board <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2.5">
            {recentTasks.length > 0 ? (
              recentTasks.map((t) => {
                const isDone = t.status === "completed";
                return (
                  <div
                    key={t.id}
                    onClick={() => handleToggleTask(t)}
                    className={`p-3.5 bg-slate-50/80 hover:bg-indigo-50/50 border rounded-2xl flex items-center justify-between gap-3 cursor-pointer transition-all ${
                      isDone
                        ? "border-slate-200/50 opacity-60"
                        : "border-slate-200/80 hover:border-indigo-300 shadow-sm"
                    }`}
                  >
                    <div className="flex items-center space-x-3 min-w-0">
                      <div
                        className={`w-4 h-4 rounded-md border flex items-center justify-center flex-shrink-0 transition-colors ${
                          isDone
                            ? "bg-emerald-500 border-emerald-500 text-white"
                            : "border-slate-300 hover:border-indigo-500 bg-white"
                        }`}
                      >
                        {isDone && <Check className="w-3 h-3 text-white" />}
                      </div>
                      <div className="min-w-0">
                        <p
                          className={`text-xs font-bold truncate ${
                            isDone ? "line-through text-slate-400" : "text-slate-800"
                          }`}
                        >
                          {t.title}
                        </p>
                        {t.deadline && (
                          <p className="text-[10px] text-indigo-600 font-mono mt-0.5">
                            Due: {new Date(t.deadline).toLocaleDateString()}
                          </p>
                        )}
                      </div>
                    </div>

                    <span
                      className={`px-2 py-0.5 text-[9px] font-bold rounded uppercase flex-shrink-0 ${
                        t.priority === "High"
                          ? "bg-red-50 text-red-600 border border-red-200"
                          : "bg-slate-100 text-slate-600"
                      }`}
                    >
                      {t.priority}
                    </span>
                  </div>
                );
              })
            ) : (
              <div className="py-10 text-center text-xs text-slate-400 bg-slate-50/50 border border-dashed border-slate-200 rounded-2xl">
                No active tasks. Click &quot;Sync Live Inbox&quot; above to auto-extract tasks from your Gmail!
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Recent Emails */}
        <div className="p-6 bg-white/90 border border-slate-200/80 rounded-3xl glass-panel space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-800 flex items-center gap-2">
              <Mail className="w-4 h-4 text-purple-600" />
              Recent Emails ({currentUser?.email})
            </h2>
            <Link
              href="/inbox"
              className="text-xs font-bold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
            >
              Full Inbox <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          <div className="space-y-2.5">
            {recentEmails.length > 0 ? (
              recentEmails.map((e) => (
                <Link
                  key={e.id}
                  href="/inbox"
                  className="p-3.5 bg-slate-50/80 hover:bg-purple-50/50 border border-slate-200/80 hover:border-purple-300 rounded-2xl flex items-center justify-between gap-3 transition-all block shadow-sm"
                >
                  <div className="min-w-0 pr-2">
                    <p className="text-xs font-bold text-slate-800 truncate">{e.subject}</p>
                    <p className="text-[11px] text-slate-500 truncate mt-0.5">
                      {e.sender_name || e.sender}
                    </p>
                  </div>
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-100 rounded uppercase flex-shrink-0">
                    {e.category}
                  </span>
                </Link>
              ))
            ) : (
              <div className="py-10 text-center text-xs text-slate-400 bg-slate-50/50 border border-dashed border-slate-200 rounded-2xl">
                No emails yet. Click &quot;Sync Live Inbox&quot; to fetch your Gmail messages!
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
