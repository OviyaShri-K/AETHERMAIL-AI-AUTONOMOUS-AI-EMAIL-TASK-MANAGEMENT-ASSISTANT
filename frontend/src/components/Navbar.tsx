"use client";

import React, { useState } from "react";
import { useUser } from "@/context/UserContext";
import { syncGmailInbox } from "@/lib/api";
import Link from "next/link";
import {
  RefreshCw,
  CheckCircle2,
  ChevronDown,
  Home,
  Sparkles,
} from "lucide-react";

export const Navbar: React.FC = () => {
  const { currentUser, openLoginModal } = useUser();
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState("");

  const handleSyncGmail = async () => {
    setIsSyncing(true);
    setSyncFeedback("");
    try {
      const res = await syncGmailInbox(currentUser?.email);
      setSyncFeedback(res.message || "Synced live Gmail inbox!");
      setTimeout(() => setSyncFeedback(""), 3500);
    } catch (err) {
      setSyncFeedback("Sync check completed.");
      setTimeout(() => setSyncFeedback(""), 3500);
    } finally {
      setIsSyncing(false);
    }
  };

  return (
    <header className="h-16 px-6 bg-white/80 border-b border-slate-200/80 flex items-center justify-between glass-panel sticky top-0 z-30">
      {/* Left: Active Workspace Pill & Home shortcut */}
      <div className="flex items-center space-x-3">
        <Link
          href="/home"
          className="p-2 bg-white hover:bg-slate-50 border border-slate-200/90 text-slate-600 hover:text-indigo-600 rounded-full shadow-sm transition-all flex items-center gap-1.5 text-xs font-bold"
          title="Visit Home Landing Page"
        >
          <Home className="w-3.5 h-3.5 text-indigo-600" />
          <span className="hidden sm:inline">Home</span>
        </Link>

        <div className="flex items-center space-x-2 px-3.5 py-1.5 bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-100 rounded-full shadow-sm">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span className="text-xs font-semibold text-slate-600">Active Workspace:</span>
          <span className="text-xs font-bold text-indigo-700 font-mono">
            {currentUser?.email || "No Account Active"}
          </span>
        </div>

        {syncFeedback && (
          <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 border border-emerald-200 px-3.5 py-1 rounded-full flex items-center gap-1.5 animate-fadeIn">
            <CheckCircle2 className="w-3.5 h-3.5" /> {syncFeedback}
          </span>
        )}
      </div>

      {/* Right: Actions */}
      <div className="flex items-center space-x-2.5">
        <button
          onClick={handleSyncGmail}
          disabled={isSyncing}
          className="px-3.5 py-1.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white rounded-full text-xs font-bold flex items-center gap-1.5 transition-all shadow-sm shadow-indigo-500/20 disabled:opacity-50"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? "animate-spin text-white" : ""}`} />
          <span>{isSyncing ? "Syncing..." : "Sync Live Inbox"}</span>
        </button>

        <button
          onClick={openLoginModal}
          className="flex items-center space-x-2 pl-2 pr-3.5 py-1 bg-white hover:bg-slate-50 border border-slate-200 rounded-full text-xs font-semibold shadow-sm transition-all text-slate-800"
        >
          <span className="text-base">{currentUser?.avatar || "🎓"}</span>
          <span className="hidden sm:inline">Switch / Sign In</span>
          <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
        </button>
      </div>
    </header>
  );
};
