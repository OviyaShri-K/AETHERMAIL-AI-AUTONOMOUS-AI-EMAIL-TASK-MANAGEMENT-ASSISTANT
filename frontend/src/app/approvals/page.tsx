"use client";

import React, { useEffect, useState } from "react";
import { useUser } from "@/context/UserContext";
import {
  fetchApprovals,
  authorizeApprovalAction,
  rejectApprovalAction,
  ApprovalItem,
} from "@/lib/api";
import {
  ShieldCheck,
  Send,
  XCircle,
  Clock,
  Sparkles,
  RefreshCw,
  Mail,
  CheckCircle2,
} from "lucide-react";

export default function ApprovalsGatePage() {
  const { currentUser } = useUser();
  const [approvals, setApprovals] = useState<ApprovalItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [editedDrafts, setEditedDrafts] = useState<Record<number, string>>({});
  const [feedback, setFeedback] = useState<string>("");

  const loadApprovals = async () => {
    setLoading(true);
    try {
      const res = await fetchApprovals({
        status: "pending_approval",
        user_email: currentUser?.email,
      });
      const list = Array.isArray(res) ? res : res.actions || [];
      setApprovals(list);
    } catch (err) {
      console.warn("Failed to load approvals:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadApprovals();
  }, [currentUser]);

  const handleApprove = async (actionId: number) => {
    try {
      const customDraft = editedDrafts[actionId];
      const res = await authorizeApprovalAction(actionId, customDraft);
      setFeedback(res.message || "Draft approved & transmitted successfully!");
      setApprovals((prev) => prev.filter((a) => a.id !== actionId));
      setTimeout(() => setFeedback(""), 4000);
    } catch (err) {
      console.error("Failed to approve action:", err);
    }
  };

  const handleReject = async (actionId: number) => {
    try {
      await rejectApprovalAction(actionId, "Rejected by user in safety gate.");
      setFeedback("AI Action rejected and archived.");
      setApprovals((prev) => prev.filter((a) => a.id !== actionId));
      setTimeout(() => setFeedback(""), 4000);
    } catch (err) {
      console.error("Failed to reject action:", err);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-800 flex items-center gap-2.5">
            <ShieldCheck className="w-6 h-6 text-purple-600" />
            Human-in-the-Loop Approvals Gate
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Review, edit, and authorize AI-generated outbound replies before transmission
          </p>
        </div>

        <button
          onClick={loadApprovals}
          className="p-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-600 rounded-2xl shadow-sm transition-all self-start md:self-auto"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-purple-600" : ""}`} />
        </button>
      </div>

      {feedback && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold rounded-2xl flex items-center gap-2 animate-fadeIn shadow-sm">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          {feedback}
        </div>
      )}

      {/* Approvals List */}
      <div className="space-y-5">
        {loading ? (
          <div className="py-16 text-center text-xs text-slate-400">
            Checking safety gate for pending outbound replies...
          </div>
        ) : approvals.length > 0 ? (
          approvals.map((item) => (
            <div
              key={item.id}
              className="p-6 bg-white/95 border border-purple-100 rounded-3xl space-y-4 glass-panel shadow-sm hover:shadow-md transition-all"
            >
              <div className="flex flex-col md:flex-row md:items-center justify-between pb-3 border-b border-slate-100 gap-2">
                <div className="flex items-center space-x-2.5">
                  <span className="p-2 bg-purple-100 text-purple-600 rounded-xl">
                    <Mail className="w-4 h-4" />
                  </span>
                  <div>
                    <h3 className="text-xs font-bold text-slate-800">
                      Reply to: {item.sender || "Sender"}
                    </h3>
                    <p className="text-[11px] text-slate-500">
                      Subject: {item.email_subject || "Re: Notification"}
                    </p>
                  </div>
                </div>
                <span className="px-3 py-1 text-[10px] font-bold uppercase bg-amber-50 text-amber-700 border border-amber-200 rounded-full self-start md:self-auto">
                  Awaiting Authorization
                </span>
              </div>

              {/* Editable Draft */}
              <div className="space-y-2">
                <label className="block text-xs font-bold text-slate-700 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-purple-600" />
                  AI Draft Content (Editable):
                </label>
                <textarea
                  rows={4}
                  value={
                    editedDrafts[item.id] !== undefined
                      ? editedDrafts[item.id]
                      : item.draft_reply || ""
                  }
                  onChange={(e) =>
                    setEditedDrafts({
                      ...editedDrafts,
                      [item.id]: e.target.value,
                    })
                  }
                  className="w-full p-3.5 bg-slate-50 border border-slate-200 rounded-2xl text-xs text-slate-800 focus:outline-none focus:border-purple-500 focus:bg-white shadow-sm transition-all"
                />
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end space-x-3 pt-2">
                <button
                  onClick={() => handleReject(item.id)}
                  className="px-4 py-2 bg-white hover:bg-red-50 border border-slate-200 hover:border-red-200 text-slate-600 hover:text-red-600 font-bold text-xs rounded-xl flex items-center gap-1.5 transition-all shadow-sm"
                >
                  <XCircle className="w-4 h-4" /> Reject &amp; Discard
                </button>
                <button
                  onClick={() => handleApprove(item.id)}
                  className="px-5 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs rounded-xl shadow-md shadow-emerald-500/20 flex items-center gap-1.5 transition-all"
                >
                  <Send className="w-4 h-4" /> Authorize &amp; Send
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="py-16 text-center text-xs text-slate-400 bg-white/60 border border-dashed border-slate-200 rounded-3xl">
            🎉 All outbound replies authorized! No pending items in safety gate for {currentUser?.email}.
          </div>
        )}
      </div>
    </div>
  );
}
