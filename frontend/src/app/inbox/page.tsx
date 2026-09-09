"use client";

import React, { useEffect, useState, useRef } from "react";
import { useUser } from "@/context/UserContext";
import { fetchEmails, syncGmailInbox, connectGmail, fetchGoogleOAuthUrl, EmailItem } from "@/lib/api";
import {
  Inbox,
  Search,
  Paperclip,
  Sparkles,
  X,
  RefreshCw,
  ExternalLink,
  Zap,
  Key,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";

export default function SmartInboxPage() {
  const { currentUser, openLoginModal, authenticateUser } = useUser();
  const [emails, setEmails] = useState<EmailItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [lastSyncTime, setLastSyncTime] = useState<string>("Just now");
  const [selectedEmail, setSelectedEmail] = useState<EmailItem | null>(null);
  const [activeCategory, setActiveCategory] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Live Mailbox Connection State
  const [showConnectCard, setShowConnectCard] = useState(false);
  const [connectEmail, setConnectEmail] = useState(currentUser?.email || "");
  const [mailPassword, setMailPassword] = useState("");
  const [connecting, setConnecting] = useState(false);
  const [connectMessage, setConnectMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  useEffect(() => {
    if (currentUser?.email) {
      setConnectEmail(currentUser.email);
    }
  }, [currentUser?.email]);

  const loadEmails = async (silent: boolean = false) => {
    if (!silent) setLoading(true);
    try {
      const data = await fetchEmails({
        user_email: currentUser?.email,
        category: activeCategory !== "all" ? activeCategory : undefined,
      });
      setEmails(data);
      setLastSyncTime(new Date().toLocaleTimeString());
    } catch (err) {
      console.warn("Failed to fetch emails:", err);
    } finally {
      if (!silent) setLoading(false);
    }
  };

  const handleManualSync = async () => {
    setSyncing(true);
    setConnectMessage(null);
    try {
      const res = await syncGmailInbox(currentUser?.email);
      await loadEmails(true);
      if (res?.message) {
        setConnectMessage({ type: "success", text: res.message });
        setTimeout(() => setConnectMessage(null), 4000);
      }
    } catch (err: any) {
      console.warn("Manual sync notice:", err);
      setConnectMessage({
        type: "error",
        text: err?.response?.data?.detail || "Could not sync live emails. Please check your password.",
      });
      setTimeout(() => setConnectMessage(null), 5000);
    } finally {
      setSyncing(false);
    }
  };

  const handleConnectLiveMailbox = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    const targetMail = (connectEmail.trim() || currentUser?.email || "").toLowerCase();
    if (!targetMail) return;

    setConnecting(true);
    setConnectMessage(null);
    try {
      const res = await connectGmail(targetMail, mailPassword.trim() || undefined);
      await authenticateUser(targetMail, undefined, "instant", mailPassword.trim() || undefined);
      setConnectMessage({
        type: "success",
        text: res.message || `Successfully connected live mailbox for ${targetMail}!`,
      });
      setShowConnectCard(false);
      setMailPassword("");
      await loadEmails();
    } catch (err: any) {
      setConnectMessage({
        type: "error",
        text: err?.response?.data?.detail || "Authentication failed. Please verify your email and password.",
      });
    } finally {
      setConnecting(false);
    }
  };

  // Initial load on user or category change
  useEffect(() => {
    loadEmails();
  }, [currentUser, activeCategory]);

  // Autonomous Live Polling: Checks for new emails every 6 seconds and syncs Gmail every 15 seconds
  useEffect(() => {
    if (!currentUser?.email) return;

    const emailPollInterval = setInterval(() => {
      loadEmails(true);
    }, 6000);

    const gmailSyncInterval = setInterval(() => {
      syncGmailInbox(currentUser.email).catch(() => {});
    }, 15000);

    return () => {
      clearInterval(emailPollInterval);
      clearInterval(gmailSyncInterval);
    };
  }, [currentUser?.email, activeCategory]);

  const categories = [
    { id: "all", label: "All Mail" },
    { id: "work", label: "Work & Academic" },
    { id: "personal", label: "Personal" },
    { id: "notification", label: "Notifications" },
    { id: "spam", label: "Spam Filtered" },
  ];

  const filteredEmails = emails.filter((e) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    return (
      e.subject.toLowerCase().includes(q) ||
      e.body.toLowerCase().includes(q) ||
      e.sender.toLowerCase().includes(q)
    );
  });

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-extrabold text-slate-800 flex items-center gap-2.5">
              <Inbox className="w-6 h-6 text-indigo-600" />
              Live Gmail Inbox
            </h1>
            {/* Live Polling Pulse Indicator */}
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200/80 rounded-full shadow-sm">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span>
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-600"></span>
              Live Auto-Sync
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5 flex items-center gap-2">
            <span>
              Active Account:{" "}
              <span className="font-bold text-indigo-700 font-mono">
                {currentUser?.email || "No Mailbox Connected"}
              </span>
            </span>
            <span className="text-slate-300">&bull;</span>
            <span className="text-[11px] text-slate-400">
              Last checked: {lastSyncTime}
            </span>
          </p>
        </div>

        <div className="flex items-center gap-2.5 flex-wrap">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search subject, sender..."
              className="pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm w-52"
            />
          </div>

          {/* Connect / Update Password Button */}
          <button
            onClick={() => setShowConnectCard(!showConnectCard)}
            className="px-3.5 py-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-bold text-xs rounded-2xl shadow-sm hover:shadow transition-all flex items-center gap-1.5"
          >
            <Key className="w-3.5 h-3.5 text-indigo-600" />
            <span>{showConnectCard ? "Hide Setup" : "Connect Live Mailbox"}</span>
          </button>

          {/* Sync Live Gmail Button */}
          <button
            onClick={handleManualSync}
            disabled={syncing}
            className="px-3.5 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs rounded-2xl shadow-sm hover:shadow transition-all flex items-center gap-1.5 disabled:opacity-60"
          >
            <Zap className={`w-3.5 h-3.5 ${syncing ? "animate-bounce text-amber-300" : "text-amber-300"}`} />
            <span>{syncing ? "Syncing Gmail..." : "Sync Live Gmail"}</span>
          </button>

          {/* Refresh emails list */}
          <button
            onClick={() => loadEmails(false)}
            title="Refresh list"
            className="p-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-600 rounded-2xl shadow-sm transition-all"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-indigo-600" : ""}`} />
          </button>
        </div>
      </div>

      {/* Alert Notification Message */}
      {connectMessage && (
        <div
          className={`p-3.5 rounded-2xl border text-xs font-semibold flex items-center justify-between gap-2 shadow-sm animate-fadeIn ${
            connectMessage.type === "success"
              ? "bg-emerald-50 border-emerald-200 text-emerald-800"
              : "bg-amber-50 border-amber-200 text-amber-800"
          }`}
        >
          <div className="flex items-center gap-2">
            {connectMessage.type === "success" ? (
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            ) : (
              <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
            )}
            <span>{connectMessage.text}</span>
          </div>
          <button
            onClick={() => setConnectMessage(null)}
            className="text-slate-400 hover:text-slate-600 p-1"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Expandable Connect Live Mailbox Card */}
      {showConnectCard && (
        <div className="p-6 bg-gradient-to-r from-indigo-50/95 via-purple-50/90 to-pink-50/80 border border-indigo-200/80 rounded-3xl shadow-md glass-panel space-y-4 animate-fadeIn">
          <div className="flex items-start justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2.5 bg-gradient-to-tr from-indigo-600 to-purple-600 text-white rounded-2xl shadow-sm">
                <Key className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-sm font-extrabold text-slate-800">
                  Connect Live Mailbox: {currentUser?.email}
                </h2>
                <p className="text-xs text-slate-500">
                  Secure direct connection fetches ONLY authentic real emails from your inbox.
                </p>
              </div>
            </div>
            <button
              onClick={() => setShowConnectCard(false)}
              className="p-1 text-slate-400 hover:text-slate-700 bg-white/80 rounded-full"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <form onSubmit={handleConnectLiveMailbox} className="grid grid-cols-1 md:grid-cols-3 gap-3 items-center">
            <div>
              <label className="block text-[11px] font-bold text-slate-700 mb-1">
                Email Address (Gmail ID)
              </label>
              <input
                type="email"
                required
                value={connectEmail}
                onChange={(e) => setConnectEmail(e.target.value)}
                placeholder="e.g. sarah.jenkins@techcorp.io"
                className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm"
              />
            </div>
            <div>
              <label className="block text-[11px] font-bold text-slate-700 mb-1">
                Mail Password
              </label>
              <input
                type="password"
                value={mailPassword}
                onChange={(e) => setMailPassword(e.target.value)}
                placeholder="Enter your email password"
                className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm"
              />
            </div>
            <div className="pt-5">
              <button
                type="submit"
                disabled={connecting}
                className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs rounded-2xl shadow-sm transition-all flex items-center justify-center gap-1.5 disabled:opacity-60"
              >
                <Zap className="w-4 h-4 text-amber-300" />
                <span>{connecting ? "Connecting..." : "Connect & Fetch Real Emails"}</span>
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Category Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-200/80 pb-3 overflow-x-auto">
        {categories.map((cat) => (
          <button
            key={cat.id}
            onClick={() => setActiveCategory(cat.id)}
            className={`px-4 py-2 rounded-2xl text-xs font-bold whitespace-nowrap transition-all ${
              activeCategory === cat.id
                ? "bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-sm shadow-indigo-500/20"
                : "bg-white text-slate-600 hover:text-slate-900 border border-slate-200/80 shadow-sm"
            }`}
          >
            {cat.label}
          </button>
        ))}
      </div>

      {/* Email List */}
      <div className="space-y-3">
        {loading ? (
          <div className="py-16 text-center text-xs text-slate-400">
            Loading inbox messages for {currentUser?.email}...
          </div>
        ) : filteredEmails.length > 0 ? (
          filteredEmails.map((email) => (
            <div
              key={email.id}
              onClick={() => setSelectedEmail(email)}
              className={`p-4 bg-white/90 hover:bg-indigo-50/40 border rounded-3xl cursor-pointer transition-all flex flex-col md:flex-row md:items-center justify-between gap-3 shadow-sm hover:shadow-md ${
                email.is_spam
                  ? "border-red-200 bg-red-50/20"
                  : email.priority === "High"
                  ? "border-indigo-200 hover:border-indigo-300"
                  : "border-slate-200/80 hover:border-slate-300"
              }`}
            >
              <div className="flex items-start space-x-3.5 min-w-0">
                <div
                  className={`p-2.5 rounded-2xl flex-shrink-0 ${
                    email.is_spam
                      ? "bg-red-100 text-red-600"
                      : email.category === "work"
                      ? "bg-blue-100 text-blue-600"
                      : "bg-emerald-100 text-emerald-600"
                  }`}
                >
                  <Inbox className="w-5 h-5" />
                </div>
                <div className="min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-bold text-slate-800 truncate">
                      {email.sender_name || email.sender}
                    </span>
                    <span className="text-[11px] text-slate-400 truncate">
                      &lt;{email.sender}&gt;
                    </span>
                    {email.is_spam && (
                      <span className="px-2 py-0.5 text-[9px] font-bold bg-red-100 text-red-600 border border-red-200 rounded">
                        SPAM
                      </span>
                    )}
                  </div>
                  <h3 className="text-xs font-bold text-slate-800 truncate">
                    {email.subject}
                  </h3>
                  <p className="text-[11px] text-slate-500 truncate mt-0.5 max-w-2xl">
                    {email.body}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-3 flex-shrink-0 self-end md:self-center">
                {email.attachments && email.attachments.length > 0 && (
                  <span className="px-2.5 py-1 text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-full flex items-center gap-1">
                    <Paperclip className="w-3 h-3" /> {email.attachments.length} file
                  </span>
                )}
                <span
                  className={`px-2.5 py-0.5 text-[10px] font-bold rounded-full uppercase ${
                    email.priority === "High"
                      ? "bg-red-50 text-red-600 border border-red-200"
                      : email.priority === "Medium"
                      ? "bg-amber-50 text-amber-600 border border-amber-200"
                      : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {email.priority}
                </span>
                <span className="text-[11px] text-slate-400 whitespace-nowrap">
                  {new Date(email.timestamp).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))
        ) : (
          /* Empty State with integrated Live Mailbox Connect Card */
          <div className="py-12 px-6 text-center bg-white/80 border border-dashed border-indigo-200/90 rounded-3xl space-y-4 max-w-2xl mx-auto shadow-sm">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center shadow-sm">
              <Inbox className="w-7 h-7 animate-pulse" />
            </div>
            <div>
              <h3 className="text-base font-extrabold text-slate-800">
                Live Mailbox Inbox for {currentUser?.email}
              </h3>
              <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                No random or mock emails. Enter your email password to retrieve and process only authentic live emails from your inbox.
              </p>
            </div>

            {/* Quick Password Connect Inline Box */}
            <form onSubmit={handleConnectLiveMailbox} className="max-w-md mx-auto space-y-3 pt-2">
              <div className="space-y-2">
                <input
                  type="email"
                  required
                  value={connectEmail}
                  onChange={(e) => setConnectEmail(e.target.value)}
                  placeholder="Enter your Gmail address"
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm text-center font-medium"
                />
                <input
                  type="password"
                  value={mailPassword}
                  onChange={(e) => setMailPassword(e.target.value)}
                  placeholder="Enter your email password"
                  className="w-full px-3.5 py-2.5 bg-white border border-slate-300 rounded-2xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 shadow-sm text-center"
                />
              </div>
              <div className="flex flex-col sm:flex-row items-center justify-center gap-2">
                <button
                  type="submit"
                  disabled={connecting}
                  className="w-full sm:w-auto px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold text-xs rounded-2xl shadow-md shadow-indigo-500/20 transition-all flex items-center justify-center gap-1.5 disabled:opacity-60"
                >
                  <Zap className="w-4 h-4 text-amber-300" />
                  <span>{connecting ? "Connecting..." : "Connect & Fetch Real Emails"}</span>
                </button>
                <button
                  type="button"
                  onClick={handleManualSync}
                  disabled={syncing}
                  className="w-full sm:w-auto px-4 py-2.5 bg-white hover:bg-slate-50 border border-slate-200 text-slate-700 font-bold text-xs rounded-2xl shadow-sm transition-all"
                >
                  {syncing ? "Checking..." : "Check Existing Inbox"}
                </button>
              </div>

              {/* Direct Google OAuth Button */}
              <div className="pt-2 border-t border-slate-200/80">
                <button
                  type="button"
                  onClick={async () => {
                    try {
                      const res = await fetchGoogleOAuthUrl();
                      if (res.url) window.location.href = res.url;
                    } catch (e) {}
                  }}
                  className="w-full py-2.5 px-4 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-2xl shadow-sm hover:shadow border border-slate-300 flex items-center justify-center gap-2.5 transition-all"
                >
                  <svg className="w-4 h-4" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                  </svg>
                  <span>Sign in with Google OAuth (No Password Needed)</span>
                </button>
              </div>
            </form>
          </div>
        )}
      </div>

      {/* Email Detail Modal */}
      {selectedEmail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
          <div className="relative w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 bg-white border border-slate-200 rounded-3xl shadow-2xl glass-panel space-y-4">
            {/* Modal Header */}
            <div className="flex items-start justify-between pb-3 border-b border-slate-100">
              <div>
                <span className="px-3 py-1 text-[10px] font-bold uppercase bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-full">
                  {selectedEmail.category} &bull; {selectedEmail.priority} Priority
                </span>
                <h2 className="text-base font-extrabold text-slate-800 mt-2">
                  {selectedEmail.subject}
                </h2>
                <p className="text-xs text-slate-500 mt-0.5">
                  From: <span className="text-slate-800 font-bold">{selectedEmail.sender_name || selectedEmail.sender}</span> ({selectedEmail.sender})
                </p>
                <p className="text-xs text-slate-500">
                  To: <span className="text-indigo-600 font-mono font-bold">{selectedEmail.recipient}</span>
                </p>
              </div>
              <button
                onClick={() => setSelectedEmail(null)}
                className="p-1.5 text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Email Body */}
            <div className="p-4 bg-slate-50/80 border border-slate-200/80 rounded-2xl text-xs text-slate-800 leading-relaxed whitespace-pre-wrap">
              {selectedEmail.body}
            </div>

            {/* Cloudinary Attachments */}
            {selectedEmail.attachments && selectedEmail.attachments.length > 0 && (
              <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl space-y-2">
                <p className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                  <Paperclip className="w-3.5 h-3.5 text-indigo-600" />
                  Cloudinary Attachments:
                </p>
                <div className="flex flex-wrap gap-2">
                  {selectedEmail.attachments.map((att) => (
                    <a
                      key={att.id}
                      href={att.cloudinary_url}
                      target="_blank"
                      rel="noreferrer"
                      className="px-3 py-1.5 bg-white hover:bg-slate-50 border border-slate-200 rounded-xl text-xs text-indigo-600 font-bold flex items-center gap-1.5 shadow-sm transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" />
                      {att.filename} ({Math.round(att.file_size_bytes / 1024)} KB)
                    </a>
                  ))}
                </div>
              </div>
            )}

            {/* AI Generated Draft Reply */}
            {selectedEmail.draft_reply && (
              <div className="p-4 bg-gradient-to-br from-indigo-50/80 to-purple-50/80 border border-indigo-100 rounded-2xl space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-700 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                    AI Pre-Composed Draft Reply
                  </span>
                  <span className="text-[10px] font-semibold text-slate-500">
                    Ready for Human Authorization
                  </span>
                </div>
                <div className="p-3 bg-white/95 border border-slate-200/80 rounded-xl text-xs text-slate-700 whitespace-pre-wrap font-sans shadow-sm">
                  {selectedEmail.draft_reply}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
