"use client";

import React, { useState } from "react";
import { useUser } from "@/context/UserContext";
import { processNewEmail } from "@/lib/api";
import { X, Send, Sparkles, CheckCircle2, AlertCircle } from "lucide-react";

interface SimulateEmailModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
}

export const SimulateEmailModal: React.FC<SimulateEmailModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
}) => {
  const { currentUser } = useUser();

  const [sender, setSender] = useState("engineering.lead@techcorp.io");
  const [senderName, setSenderName] = useState("Dr. K. Sathish (Project Guide)");
  const [recipient, setRecipient] = useState(currentUser?.email || "");
  const [subject, setSubject] = useState(
    "URGENT: Submit Final AI Project Architecture & Test Results before Tomorrow 4 PM"
  );
  const [body, setBody] = useState(
    "Dear Student, please verify all FastAPI endpoints, confirm PostgreSQL table data in pgAdmin, and submit your final AI documentation before 4:00 PM tomorrow."
  );
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  if (!isOpen) return null;

  const handleSimulate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");
    setStatusMsg("");

    try {
      const res = await processNewEmail({
        sender,
        sender_name: senderName,
        recipient: recipient || currentUser?.email || "user@workspace.com",
        subject,
        body,
        timestamp: new Date().toISOString(),
      });

      setStatusMsg(
        `Email processed with AI! Category: ${res.email.category}, Tasks extracted: ${res.email.tasks?.length || 1}`
      );
      setTimeout(() => {
        onClose();
        if (onSuccess) onSuccess();
        setStatusMsg("");
      }, 1200);
    } catch (err: any) {
      setErrorMsg("Failed to process email. Ensure backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-lg p-6 bg-white/95 border border-slate-200 rounded-3xl shadow-2xl glass-panel">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center space-x-2.5">
            <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-xl text-white shadow-sm">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-800">
                Ingest Real Email
              </h2>
              <p className="text-xs text-slate-500">
                Trigger real-time AI categorization, task extraction &amp; draft reply
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <form onSubmit={handleSimulate} className="mt-4 space-y-3.5">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Sender Email
              </label>
              <input
                type="email"
                required
                value={sender}
                onChange={(e) => setSender(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-indigo-500 focus:bg-white"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Sender Name
              </label>
              <input
                type="text"
                value={senderName}
                onChange={(e) => setSenderName(e.target.value)}
                className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-indigo-500 focus:bg-white"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Recipient Mail ID
            </label>
            <input
              type="email"
              required
              value={recipient}
              onChange={(e) => setRecipient(e.target.value)}
              placeholder={currentUser?.email || "developer@aethermail.ai"}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-indigo-700 font-mono font-semibold focus:outline-none focus:border-indigo-500 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Subject Line
            </label>
            <input
              type="text"
              required
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-indigo-500 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Email Body Text
            </label>
            <textarea
              required
              rows={3}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-indigo-500 focus:bg-white"
            />
          </div>

          {statusMsg && (
            <div className="p-2.5 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs rounded-xl flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
              {statusMsg}
            </div>
          )}

          {errorMsg && (
            <div className="p-2.5 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center gap-2">
              <AlertCircle className="w-4 h-4 flex-shrink-0" />
              {errorMsg}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 px-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white text-xs font-bold rounded-xl shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
            {loading ? "Processing with AI..." : "Ingest & Extract with AI"}
          </button>
        </form>
      </div>
    </div>
  );
};
