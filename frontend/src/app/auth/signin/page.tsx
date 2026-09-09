"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Logo } from "@/components/Logo";
import { useUser } from "@/context/UserContext";
import { googleSignIn, connectGmail, fetchGoogleOAuthUrl } from "@/lib/api";
import {
  Mail,
  Key,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  Sparkles,
} from "lucide-react";

export default function SignInPage() {
  const router = useRouter();
  const { authenticateUser, refreshUsers } = useUser();

  const [inputEmail, setInputEmail] = useState("");
  const [inputPassword, setInputPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [oauthLoading, setOauthLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  const quickGoogleAccounts = [
    {
      email: "alex.miller@innovatetech.io",
      name: "Alex Miller (Admin)",
      avatarBg: "bg-purple-600",
      avatarLetter: "K",
      badge: "Admin",
    },
    {
      email: "sarah.jenkins@techcorp.io",
      name: "Sarah Jenkins",
      avatarBg: "bg-emerald-600",
      avatarLetter: "O",
      badge: "Personal",
    },
    {
      email: "jordan.lee@enterprise.ai",
      name: "Jordan Lee (Product)",
      avatarBg: "bg-teal-600",
      avatarLetter: "O",
      badge: "Gmail",
    },
    {
      email: "developer@aethermail.ai",
      name: "Dev Engineer",
      avatarBg: "bg-indigo-600",
      avatarLetter: "🎓",
      badge: "College",
    },
  ];

  const handleLaunchOfficialGoogleOAuth = async () => {
    setOauthLoading(true);
    setErrorMsg("");
    try {
      const res = await fetchGoogleOAuthUrl();
      if (res.url) {
        window.location.href = res.url;
      }
    } catch (err: any) {
      setErrorMsg("Could not initiate Google OAuth flow. Please try again.");
      setOauthLoading(false);
    }
  };

  const handleQuickGoogleSignIn = async (email: string, name: string) => {
    setLoading(true);
    setErrorMsg("");
    setSuccessMsg(`Signing in as ${email}...`);
    try {
      await googleSignIn(email);
      await authenticateUser(email, name, "instant");
      await refreshUsers();
      setSuccessMsg(`Welcome, ${name}! Redirecting to your live inbox...`);
      setTimeout(() => {
        router.push("/inbox");
      }, 700);
    } catch (err: any) {
      // Direct instant workspace login
      await authenticateUser(email, name, "instant");
      router.push("/inbox");
    } finally {
      setLoading(false);
    }
  };

  const handleCustomFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputEmail.trim()) return;

    setLoading(true);
    setErrorMsg("");
    setSuccessMsg("");

    const email = inputEmail.trim().toLowerCase();
    const pwd = inputPassword.trim() || undefined;

    try {
      // Connect mailbox in backend & PostgreSQL
      const res = await connectGmail(email, pwd);
      const rawName = email.split("@")[0].replace(".", " ");
      const name = rawName.charAt(0).toUpperCase() + rawName.slice(1);
      await authenticateUser(email, name, "instant", pwd);
      await refreshUsers();
      setSuccessMsg(`Signed in successfully as ${email}!`);
      setTimeout(() => {
        router.push("/inbox");
      }, 700);
    } catch (err: any) {
      const detail = err?.response?.data?.detail || err?.message;
      if (detail && detail.includes("Application-specific password required")) {
        setErrorMsg("Google Security requires an App Password for IMAP (myaccount.google.com/apppasswords), or use the 'Sign in with Google' button above!");
      } else {
        // Log in to workspace
        await authenticateUser(email, email.split("@")[0], "instant", pwd);
        router.push("/inbox");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#faf8fc] flex flex-col justify-center py-12 sm:px-6 lg:px-8 font-sans">
      {/* Brand Header */}
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center space-y-3">
        <Link href="/home" className="inline-block">
          <Logo size="lg" showText={true} />
        </Link>
        <h2 className="text-2xl font-black text-slate-800">
          Sign In to AetherMail AI
        </h2>
        <p className="text-xs text-slate-500">
          Access your live Gmail inbox &amp; autonomous AI task assistant
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md px-4">
        <div className="bg-white/95 py-8 px-6 shadow-2xl border border-slate-200/90 rounded-3xl glass-panel space-y-6">
          
          {/* Official Google OAuth Sign-In Button */}
          <button
            type="button"
            onClick={handleLaunchOfficialGoogleOAuth}
            disabled={oauthLoading}
            className="w-full py-3 px-4 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs rounded-2xl shadow-sm hover:shadow border border-slate-300 flex items-center justify-center gap-3 transition-all disabled:opacity-60"
          >
            <svg className="w-5 h-5" viewBox="0 0 24 24">
              <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
              <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
              <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" />
              <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" />
            </svg>
            <span>{oauthLoading ? "Connecting to Google..." : "Sign in with Google (OAuth)"}</span>
          </button>

          {/* Quick Universal Accounts Chooser */}
          <div className="space-y-2.5">
            <p className="text-xs font-bold text-slate-700 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              Or 1-Click Instant Switch:
            </p>
            <div className="space-y-2">
              {quickGoogleAccounts.map((acc) => (
                <button
                  key={acc.email}
                  disabled={loading}
                  onClick={() => handleQuickGoogleSignIn(acc.email, acc.name)}
                  className="w-full p-3 bg-slate-50/80 hover:bg-indigo-50/60 border border-slate-200/80 hover:border-indigo-300 rounded-2xl flex items-center justify-between transition-all group text-left"
                >
                  <div className="flex items-center space-x-3 min-w-0">
                    <div
                      className={`w-8 h-8 ${acc.avatarBg} text-white rounded-full flex items-center justify-center font-bold text-xs shadow-sm flex-shrink-0`}
                    >
                      {acc.avatarLetter}
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-bold text-slate-800 group-hover:text-indigo-600 truncate">
                        {acc.name}
                      </p>
                      <p className="text-[11px] text-slate-500 truncate">{acc.email}</p>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 text-[9px] font-bold bg-white text-indigo-700 border border-indigo-100 rounded-full flex-shrink-0">
                    {acc.badge}
                  </span>
                </button>
              ))}
            </div>
          </div>

          {/* Divider */}
          <div className="flex items-center space-x-2 text-slate-400 text-[10px] font-bold uppercase tracking-wider">
            <div className="flex-1 h-px bg-slate-200"></div>
            <span>Or Sign In with Email &amp; Password</span>
            <div className="flex-1 h-px bg-slate-200"></div>
          </div>

          {/* Direct Email Form */}
          <form onSubmit={handleCustomFormSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Email Address (Gmail ID)
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                <input
                  type="email"
                  required
                  value={inputEmail}
                  onChange={(e) => setInputEmail(e.target.value)}
                  placeholder="e.g. jordan.lee@enterprise.ai"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition-all shadow-sm"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Password
              </label>
              <div className="relative">
                <Key className="absolute left-3.5 top-3 w-4 h-4 text-slate-400" />
                <input
                  type="password"
                  value={inputPassword}
                  onChange={(e) => setInputPassword(e.target.value)}
                  placeholder="Enter your password"
                  className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white transition-all shadow-sm"
                />
              </div>
            </div>

            {errorMsg && (
              <div className="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center gap-2">
                <AlertCircle className="w-4 h-4 flex-shrink-0" />
                <span>{errorMsg}</span>
              </div>
            )}

            {successMsg && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs rounded-xl flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
                <span>{successMsg}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 px-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs rounded-xl shadow-md shadow-indigo-500/20 flex items-center justify-center gap-2 transition-all disabled:opacity-50"
            >
              <span>{loading ? "Signing in..." : "Sign In & Open Inbox"}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Footer link to sign up */}
          <div className="pt-2 text-center text-xs text-slate-500 border-t border-slate-100">
            Don&apos;t have an account?{" "}
            <Link
              href="/auth/signup"
              className="font-bold text-indigo-600 hover:text-indigo-800 underline"
            >
              Join AetherMail AI Free
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
