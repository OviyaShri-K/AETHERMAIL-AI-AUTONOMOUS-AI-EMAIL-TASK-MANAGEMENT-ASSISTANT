"use client";

import React, { useState } from "react";
import { useUser } from "@/context/UserContext";
import { connectGmail, syncGmailInbox } from "@/lib/api";
import {
  Settings,
  Database,
  Cloud,
  Layers,
  UserCheck,
  Sparkles,
  Key,
  Zap,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
  Shield,
  RefreshCw,
} from "lucide-react";

export default function SettingsPage() {
  const { currentUser, openLoginModal, authenticateUser } = useUser();
  const [settingsEmail, setSettingsEmail] = useState(currentUser?.email || "");
  const [appPassword, setAppPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [statusMsg, setStatusMsg] = useState<{ type: "success" | "error"; text: string } | null>(null);

  React.useEffect(() => {
    if (currentUser?.email) {
      setSettingsEmail(currentUser.email);
    }
  }, [currentUser?.email]);

  const handleSaveCredentials = async (e: React.FormEvent) => {
    e.preventDefault();
    const targetMail = (settingsEmail.trim() || currentUser?.email || "").toLowerCase();
    if (!targetMail) return;

    setSaving(true);
    setStatusMsg(null);
    try {
      const res = await connectGmail(targetMail, appPassword.trim() || undefined);
      await authenticateUser(targetMail, undefined, "instant", appPassword.trim() || undefined);
      setStatusMsg({
        type: "success",
        text: res.message || `Successfully verified and connected ${targetMail}!`,
      });
      setAppPassword("");
    } catch (err: any) {
      setStatusMsg({
        type: "error",
        text: err?.response?.data?.detail || "Could not verify credentials on imap.gmail.com:993",
      });
    } finally {
      setSaving(false);
    }
  };

  const handleSyncNow = async () => {
    if (!currentUser?.email) return;
    setSyncing(true);
    setStatusMsg(null);
    try {
      const res = await syncGmailInbox(currentUser.email);
      setStatusMsg({
        type: "success",
        text: res.message || "Live Gmail inbox synced successfully!",
      });
    } catch (err: any) {
      setStatusMsg({
        type: "error",
        text: err?.response?.data?.detail || "Sync failed. Check your App Password.",
      });
    } finally {
      setSyncing(false);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-slate-800 flex items-center gap-2.5">
          <Settings className="w-6 h-6 text-slate-600" />
          Settings &amp; Workspace Profile
        </h1>
        <p className="text-xs text-slate-500 mt-0.5">
          Manage your account profile, live mailbox connection, local PostgreSQL database, and Cloudinary CDN
        </p>
      </div>

      {/* Active User Account Profile Card */}
      <div className="p-6 bg-gradient-to-r from-indigo-50/90 via-purple-50/80 to-pink-50/70 border border-indigo-100 rounded-3xl glass-panel space-y-4 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <div className="w-16 h-16 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center text-3xl text-white shadow-md shadow-indigo-500/20">
              {currentUser?.avatar || "🎓"}
            </div>
            <div>
              <span className="px-2.5 py-0.5 text-[10px] font-bold uppercase bg-indigo-100 text-indigo-700 rounded-full">
                Active Workspace
              </span>
              <h2 className="text-lg font-extrabold text-slate-800 mt-1">
                {currentUser?.name || "User Profile"}
              </h2>
              <p className="text-xs font-mono text-indigo-700 font-bold mt-0.5">
                {currentUser?.email || "No Email Active"}
              </p>
              <p className="text-xs text-slate-500 mt-0.5">
                Role: {currentUser?.role || "Active User"}
              </p>
            </div>
          </div>
          <button
            onClick={openLoginModal}
            className="px-5 py-2.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs rounded-2xl shadow-md shadow-indigo-500/20 transition-all self-start sm:self-auto"
          >
            Switch Account
          </button>
        </div>
      </div>

      {/* Status Feedback Notification */}
      {statusMsg && (
        <div
          className={`p-3.5 rounded-2xl border text-xs font-semibold flex items-center justify-between gap-2 shadow-sm animate-fadeIn ${
            statusMsg.type === "success"
              ? "bg-emerald-50 border-emerald-200 text-emerald-800"
              : "bg-amber-50 border-amber-200 text-amber-800"
          }`}
        >
          <div className="flex items-center gap-2">
            {statusMsg.type === "success" ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
            )}
            <span>{statusMsg.text}</span>
          </div>
          <button
            onClick={() => setStatusMsg(null)}
            className="text-slate-400 hover:text-slate-600 text-xs px-2"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Live Mailbox & Security Box */}
      <div className="p-6 bg-white/95 border border-slate-200/90 rounded-3xl space-y-4 shadow-sm glass-panel">
        <div className="flex items-center space-x-3 pb-3 border-b border-slate-100">
          <div className="p-2.5 bg-indigo-100 text-indigo-600 rounded-2xl">
            <Key className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-extrabold text-slate-800">
              Live Mailbox Connection &amp; Password
            </h2>
            <p className="text-xs text-slate-500">
              Direct live connection retrieves and syncs real emails from your inbox into PostgreSQL.
            </p>
          </div>
        </div>

        <form onSubmit={handleSaveCredentials} className="space-y-3">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
            <div className="md:col-span-2">
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Email Address (Gmail ID)
              </label>
              <input
                type="email"
                required
                value={settingsEmail}
                onChange={(e) => setSettingsEmail(e.target.value)}
                placeholder="e.g. sarah.jenkins@techcorp.io"
                className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm"
              />
            </div>
            <div className="md:col-span-1">
              <label className="block text-xs font-bold text-slate-700 mb-1">
                Mailbox Password
              </label>
              <input
                type="password"
                value={appPassword}
                onChange={(e) => setAppPassword(e.target.value)}
                placeholder="Enter password"
                className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm"
              />
            </div>
            <div className="flex items-end gap-2">
              <button
                type="submit"
                disabled={saving}
                className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs rounded-2xl shadow-sm transition-all flex items-center justify-center gap-1.5 disabled:opacity-60"
              >
                <Key className="w-3.5 h-3.5" />
                <span>{saving ? "..." : "Save"}</span>
              </button>
              <button
                type="button"
                onClick={handleSyncNow}
                disabled={syncing}
                className="w-full py-2.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-bold text-xs rounded-2xl shadow-sm transition-all flex items-center justify-center gap-1.5 disabled:opacity-60"
              >
                <RefreshCw className={`w-3.5 h-3.5 ${syncing ? "animate-spin text-indigo-600" : ""}`} />
                <span>{syncing ? "..." : "Sync"}</span>
              </button>
            </div>
          </div>
        </form>
      </div>

      {/* System Infrastructure Details */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* PostgreSQL Box */}
        <div className="p-5 bg-gradient-to-br from-white to-indigo-50/50 border border-indigo-100 rounded-3xl space-y-3 glass-card shadow-sm">
          <div className="flex items-center space-x-2.5 text-indigo-600">
            <div className="p-2 bg-indigo-100 rounded-xl">
              <Database className="w-5 h-5" />
            </div>
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Local PostgreSQL
            </h3>
          </div>
          <div className="space-y-1.5 text-xs text-slate-600 pt-1">
            <p>Database: <span className="font-mono text-indigo-700 font-bold">ai_email_db</span></p>
            <p>Host: <span className="font-mono text-slate-500">localhost:5432</span></p>
            <p>Admin Tool: <span className="text-emerald-600 font-bold">pgAdmin 4</span></p>
          </div>
        </div>

        {/* Cloudinary Box */}
        <div className="p-5 bg-gradient-to-br from-white to-cyan-50/50 border border-cyan-100 rounded-3xl space-y-3 glass-card shadow-sm">
          <div className="flex items-center space-x-2.5 text-cyan-600">
            <div className="p-2 bg-cyan-100 rounded-xl">
              <Cloud className="w-5 h-5" />
            </div>
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              Cloudinary Media CDN
            </h3>
          </div>
          <div className="space-y-1.5 text-xs text-slate-600 pt-1">
            <p>Cloud Name: <span className="font-mono text-cyan-700 font-bold">n4tj82yc</span></p>
            <p>Status: <span className="text-emerald-600 font-bold">Connected</span></p>
            <p>Storage: <span className="text-slate-500">Invoices &amp; Attachments</span></p>
          </div>
        </div>

        {/* AI Inference Box */}
        <div className="p-5 bg-gradient-to-br from-white to-purple-50/50 border border-purple-100 rounded-3xl space-y-3 glass-card shadow-sm">
          <div className="flex items-center space-x-2.5 text-purple-600">
            <div className="p-2 bg-purple-100 rounded-xl">
              <Layers className="w-5 h-5" />
            </div>
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
              AI Processing Engine
            </h3>
          </div>
          <div className="space-y-1.5 text-xs text-slate-600 pt-1">
            <p>Accuracy: <span className="font-bold text-emerald-600">100.0%</span></p>
            <p>Safety Gate: <span className="text-purple-600 font-bold">Human-in-the-Loop</span></p>
            <p>Task Engine: <span className="text-slate-500">Autonomous Extraction</span></p>
          </div>
        </div>
      </div>
    </div>
  );
}
