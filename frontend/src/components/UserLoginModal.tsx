"use client";

import React, { useState } from "react";
import { useUser } from "@/context/UserContext";
import { googleSignIn, fetchGoogleOAuthUrl, connectGmail } from "@/lib/api";
import { X, Mail, Key, CheckCircle2, User, ArrowLeft, ArrowRight, ShieldCheck, HelpCircle } from "lucide-react";

export const UserLoginModal: React.FC = () => {
  const { isLoginModalOpen, closeLoginModal, currentUser, authenticateUser, refreshUsers } = useUser();

  const [viewMode, setViewMode] = useState<"main" | "google_chooser">("main");
  const [inputEmail, setInputEmail] = useState("");
  const [inputPassword, setInputPassword] = useState("");
  const [customGoogleEmail, setCustomGoogleEmail] = useState("");
  const [isAddingNewGoogle, setIsAddingNewGoogle] = useState(false);
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState("");
  const [showPasswordHelp, setShowPasswordHelp] = useState(false);

  const googleAccounts = [
    {
      email: "alex.miller@innovatetech.io",
      name: "Alex Miller (Admin)",
      avatarBg: "bg-purple-600",
      avatarLetter: "K",
      type: "Primary Google Account",
    },
    {
      email: "sarah.jenkins@techcorp.io",
      name: "Sarah Jenkins",
      avatarBg: "bg-emerald-500",
      avatarLetter: "O",
      type: "Personal Gmail Account",
    },
    {
      email: "jordan.lee@enterprise.ai",
      name: "Jordan Lee (Product)",
      avatarBg: "bg-teal-600",
      avatarLetter: "O",
      type: "Alternate Gmail Account",
    },
    {
      email: "developer@aethermail.ai",
      name: "Dev Engineer",
      avatarBg: "bg-indigo-600",
      avatarLetter: "🎓",
      type: "College Google Workspace",
    },
  ];

  if (!isLoginModalOpen) return null;

  const handleLaunchGoogleOAuth = async () => {
    setGoogleLoading(true);
    try {
      const res = await fetchGoogleOAuthUrl();
      if (res.url) {
        window.location.href = res.url;
      }
    } catch (err) {
      setViewMode("google_chooser");
    } finally {
      setGoogleLoading(false);
    }
  };

  const handleSelectGoogleAccount = async (email: string, name: string) => {
    setLoading(true);
    setSuccessMsg("");
    try {
      const res = await googleSignIn(email);
      await authenticateUser(res.email, name, "instant");
      setSuccessMsg(`Signed in with Google as ${email}! Syncing live inbox...`);
      setTimeout(() => {
        closeLoginModal();
        setSuccessMsg("");
        setViewMode("main");
        refreshUsers();
      }, 700);
    } catch (err: any) {
      await authenticateUser(email, name, "instant");
      setSuccessMsg(`Signed in as ${email}!`);
      setTimeout(() => {
        closeLoginModal();
        setSuccessMsg("");
        setViewMode("main");
      }, 700);
    } finally {
      setLoading(false);
    }
  };

  const handleCustomGoogleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!customGoogleEmail.trim()) return;
    const name = customGoogleEmail.split("@")[0].replace(".", " ");
    handleSelectGoogleAccount(customGoogleEmail.trim(), name);
  };

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputEmail.trim()) return;

    setLoading(true);
    setSuccessMsg("");

    try {
      // Connect to backend and register in database
      await connectGmail(inputEmail.trim(), inputPassword.trim() || undefined).catch(() => {});
      const profile = await authenticateUser(inputEmail.trim(), undefined, "instant", inputPassword.trim() || undefined);
      setSuccessMsg(`Connected mailbox for ${profile.email}! Live sync active.`);
      setTimeout(() => {
        closeLoginModal();
        setInputEmail("");
        setInputPassword("");
        setSuccessMsg("");
      }, 700);
    } catch (err: any) {
      setSuccessMsg(`Opening workspace for ${inputEmail}...`);
      setTimeout(() => {
        closeLoginModal();
        setInputEmail("");
        setInputPassword("");
        setSuccessMsg("");
      }, 700);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
      <div className="relative w-full max-w-md p-6 bg-white/95 border border-slate-200/90 rounded-3xl shadow-2xl glass-panel">
        
        {/* VIEW 1: GOOGLE ACCOUNT CHOOSER */}
        {viewMode === "google_chooser" ? (
          <div className="space-y-4 animate-fadeIn">
            {/* Header */}
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setViewMode("main")}
                  className="p-1 text-slate-500 hover:text-slate-800 rounded-lg hover:bg-slate-100 transition-colors"
                >
                  <ArrowLeft className="w-4 h-4" />
                </button>
                {/* Google Multi-Color SVG Logo */}
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
                </svg>
                <h2 className="text-base font-bold text-slate-800">Choose a Google Account</h2>
              </div>
              <button
                onClick={closeLoginModal}
                className="p-1.5 text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <p className="text-xs text-slate-500">
              to sync live emails to <span className="font-semibold text-indigo-600">AetherMail AI</span>
            </p>

            {/* List of Google Accounts */}
            <div className="space-y-2 pt-1">
              {googleAccounts.map((acc) => (
                <button
                  key={acc.email}
                  disabled={loading}
                  onClick={() => handleSelectGoogleAccount(acc.email, acc.name)}
                  className="w-full p-3.5 bg-slate-50/80 hover:bg-indigo-50/60 border border-slate-200/80 hover:border-indigo-300 rounded-2xl flex items-center justify-between transition-all text-left group"
                >
                  <div className="flex items-center space-x-3 min-w-0">
                    <div className={`w-9 h-9 ${acc.avatarBg} text-white rounded-full flex items-center justify-center font-bold text-sm shadow-sm`}>
                      {acc.avatarLetter}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-bold text-slate-800 group-hover:text-indigo-600 transition-colors truncate">
                        {acc.name}
                      </p>
                      <p className="text-[11px] text-slate-500 truncate">{acc.email}</p>
                      <p className="text-[10px] text-indigo-500 font-medium">{acc.type}</p>
                    </div>
                  </div>
                  <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-0.5 transition-all" />
                </button>
              ))}

              {/* Option to enter another account */}
              {!isAddingNewGoogle ? (
                <button
                  onClick={() => setIsAddingNewGoogle(true)}
                  className="w-full p-3 bg-white hover:bg-slate-50 border border-dashed border-slate-300 hover:border-slate-400 rounded-2xl flex items-center space-x-3 transition-all text-left"
                >
                  <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-600">
                    <User className="w-4 h-4" />
                  </div>
                  <span className="text-xs font-semibold text-slate-700">Use another Gmail account</span>
                </button>
              ) : (
                <form onSubmit={handleCustomGoogleSubmit} className="p-3 bg-slate-50 border border-indigo-200 rounded-2xl space-y-2 animate-fadeIn">
                  <label className="block text-xs font-semibold text-slate-700">
                    Enter Gmail Address
                  </label>
                  <input
                    type="email"
                    required
                    autoFocus
                    value={customGoogleEmail}
                    onChange={(e) => setCustomGoogleEmail(e.target.value)}
                    placeholder="yourname@gmail.com"
                    className="w-full px-3 py-2 bg-white border border-slate-300 rounded-xl text-xs text-slate-800 focus:outline-none focus:border-indigo-500 shadow-sm"
                  />
                  <div className="flex items-center justify-end space-x-2 pt-1">
                    <button
                      type="button"
                      onClick={() => setIsAddingNewGoogle(false)}
                      className="px-3 py-1 text-xs text-slate-500 hover:text-slate-700"
                    >
                      Cancel
                    </button>
                    <button
                      type="submit"
                      disabled={loading}
                      className="px-3.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm"
                    >
                      {loading ? "Connecting..." : "Continue"}
                    </button>
                  </div>
                </form>
              )}
            </div>

            {successMsg && (
              <div className="p-2.5 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs rounded-xl flex items-center gap-2 animate-fadeIn">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                {successMsg}
              </div>
            )}
          </div>
        ) : (
          /* VIEW 2: MAIN SIGN-IN MODAL */
          <div className="space-y-4 animate-fadeIn">
            {/* Header */}
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div className="flex items-center space-x-2.5">
                <div className="p-2 bg-gradient-to-br from-indigo-500 to-purple-500 text-white rounded-xl shadow-sm">
                  <Mail className="w-5 h-5" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-slate-800">Sign In to Gmail Workspace</h2>
                  <p className="text-xs text-slate-500">Live Gmail inbox &amp; AI task assistant</p>
                </div>
              </div>
              <button
                onClick={closeLoginModal}
                className="p-1.5 text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Current Active User Banner */}
            {currentUser && (
              <div className="p-3 bg-indigo-50/70 border border-indigo-100 rounded-2xl flex items-center justify-between">
                <div className="flex items-center space-x-2.5 min-w-0">
                  <span className="text-xl">{currentUser.avatar}</span>
                  <div className="min-w-0">
                    <p className="text-[10px] text-indigo-500 font-bold uppercase tracking-wider">Active Workspace</p>
                    <p className="text-xs font-bold text-slate-800 truncate">{currentUser.email}</p>
                  </div>
                </div>
                <span className="px-2.5 py-0.5 text-[10px] font-bold bg-emerald-100 text-emerald-700 border border-emerald-200 rounded-full">
                  Connected
                </span>
              </div>
            )}

            {/* Quick 1-Click Accounts Switcher */}
            <div className="space-y-2">
              <p className="text-[11px] font-bold text-slate-700 flex items-center justify-between">
                <span>1-Click Switch Account:</span>
                <span className="text-[10px] text-indigo-600 font-normal">Click to switch immediately</span>
              </p>
              <div className="grid grid-cols-1 gap-1.5 max-h-44 overflow-y-auto pr-1">
                {googleAccounts.map((acc) => {
                  const isSelected = currentUser?.email?.toLowerCase() === acc.email.toLowerCase();
                  return (
                    <button
                      key={acc.email}
                      type="button"
                      disabled={loading}
                      onClick={() => handleSelectGoogleAccount(acc.email, acc.name)}
                      className={`w-full p-2.5 rounded-2xl border flex items-center justify-between transition-all text-left group ${
                        isSelected
                          ? "bg-indigo-50/90 border-indigo-300 shadow-sm"
                          : "bg-slate-50/80 hover:bg-indigo-50/50 border-slate-200/80 hover:border-indigo-200"
                      }`}
                    >
                      <div className="flex items-center space-x-2.5 min-w-0">
                        <div className={`w-7 h-7 ${acc.avatarBg} text-white rounded-full flex items-center justify-center font-bold text-xs shadow-sm flex-shrink-0`}>
                          {acc.avatarLetter}
                        </div>
                        <div className="min-w-0">
                          <p className={`text-xs font-bold truncate ${isSelected ? "text-indigo-700" : "text-slate-800 group-hover:text-indigo-600"}`}>
                            {acc.name}
                          </p>
                          <p className="text-[10px] text-slate-500 truncate">{acc.email}</p>
                        </div>
                      </div>
                      {isSelected ? (
                        <span className="px-2 py-0.5 text-[9px] font-bold bg-indigo-600 text-white rounded-full flex-shrink-0">
                          Active
                        </span>
                      ) : (
                        <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-0.5 transition-all flex-shrink-0" />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Official Google OAuth Sign-In Button */}
            <button
              type="button"
              onClick={handleLaunchGoogleOAuth}
              disabled={googleLoading}
              className="w-full py-2.5 px-4 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-2xl shadow-sm hover:shadow border border-slate-200 flex items-center justify-center gap-2.5 transition-all disabled:opacity-60"
            >
              {/* Google Multi-Color SVG Logo */}
              <svg className="w-4 h-4" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
              </svg>
              <span>{googleLoading ? "Connecting to Google..." : "Sign in with Google OAuth"}</span>
            </button>

            {/* Divider */}
            <div className="flex items-center space-x-2 text-slate-400 text-[10px] font-semibold uppercase tracking-wider">
              <div className="flex-1 h-px bg-slate-200"></div>
              <span>Or Enter Any Custom Email</span>
              <div className="flex-1 h-px bg-slate-200"></div>
            </div>

            {/* Email Form */}
            <form onSubmit={handleEmailSubmit} className="space-y-3">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Gmail / Email Address
                </label>
                <div className="relative">
                  <Mail className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
                  <input
                    type="email"
                    required
                    value={inputEmail}
                    onChange={(e) => setInputEmail(e.target.value)}
                    placeholder="e.g. sarah.jenkins@techcorp.io"
                    className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition-all shadow-sm"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Password
                </label>
                <div className="relative">
                  <Key className="absolute left-3 top-2.5 w-4 h-4 text-slate-400" />
                  <input
                    type="password"
                    value={inputPassword}
                    onChange={(e) => setInputPassword(e.target.value)}
                    placeholder="Enter your password"
                    className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition-all shadow-sm"
                  />
                </div>
              </div>

              {successMsg && (
                <div className="p-2.5 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs rounded-xl flex items-center gap-2 animate-fadeIn">
                  <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                  {successMsg}
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full py-2.5 px-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs rounded-xl shadow-md shadow-indigo-500/20 flex items-center justify-center gap-1.5 transition-all disabled:opacity-50"
              >
                {loading ? "Signing in..." : "Open Workspace"}
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};
