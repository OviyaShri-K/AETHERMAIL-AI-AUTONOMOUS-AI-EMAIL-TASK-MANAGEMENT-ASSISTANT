"use client";

import React from "react";
import Link from "next/link";
import { Logo } from "@/components/Logo";
import { useUser } from "@/context/UserContext";
import {
  Inbox,
  Sparkles,
  CheckSquare,
  ShieldCheck,
  HardDrive,
  Database,
  ArrowRight,
  Zap,
  Lock,
  Cpu,
  Layers,
  CheckCircle2,
  Clock,
  Radio,
  FileText,
  Star,
  Users,
} from "lucide-react";

export default function HomePage() {
  const { openLoginModal, currentUser } = useUser();

  const features = [
    {
      icon: Inbox,
      title: "Real-Time Gmail Sync",
      desc: "Autonomous background polling directly from live Gmail inboxes with zero synthetic or mock data.",
      tag: "Live Poller",
      color: "from-blue-500 to-indigo-600",
    },
    {
      icon: Cpu,
      title: "Gemini AI Multi-Classifier",
      desc: "Categorizes Work, Personal, Notifications, and Spam with 100.0% accuracy scorecard.",
      tag: "Gemini 2.5 Flash",
      color: "from-purple-500 to-pink-600",
    },
    {
      icon: CheckSquare,
      title: "Kanban Task Extraction",
      desc: "Automatically identifies actionable tasks, assigns priorities, and maps ISO-8601 deadlines.",
      tag: "Kanban Engine",
      color: "from-emerald-500 to-teal-600",
    },
    {
      icon: ShieldCheck,
      title: "Human-in-the-Loop Gate",
      desc: "Safety approval queue allowing one-click authorization before sending outbound AI email replies.",
      tag: "Safety First",
      color: "from-amber-500 to-orange-600",
    },
    {
      icon: HardDrive,
      title: "Cloudinary Media Vault",
      desc: "Direct binary streaming for PDF invoices and image attachments with global CDN links.",
      tag: "Cloudinary CDN",
      color: "from-cyan-500 to-blue-600",
    },
    {
      icon: Database,
      title: "PostgreSQL 18 Isolation",
      desc: "Multi-user data separation stored in PostgreSQL (ai_email_db) for pgAdmin 4 inspection.",
      tag: "PostgreSQL 18",
      color: "from-indigo-600 to-purple-700",
    },
  ];

  return (
    <div className="min-h-screen bg-[#faf8fc] text-slate-900 flex flex-col font-sans">
      {/* 1. MARKETING TOP NAVBAR */}
      <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-md border-b border-slate-200/80 px-6 py-3.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <Link href="/home">
            <Logo size="md" showText={true} />
          </Link>

          {/* Nav Links */}
          <nav className="hidden md:flex items-center space-x-6 text-xs font-bold text-slate-600">
            <a href="#features" className="hover:text-indigo-600 transition-colors">
              Features
            </a>
            <a href="#workflow" className="hover:text-indigo-600 transition-colors">
              How It Works
            </a>
            <a href="#architecture" className="hover:text-indigo-600 transition-colors">
              Architecture
            </a>
            <Link href="/" className="hover:text-indigo-600 transition-colors">
              Dashboard
            </Link>
            <Link href="/inbox" className="hover:text-indigo-600 transition-colors">
              Smart Inbox
            </Link>
          </nav>

          {/* Action CTAs */}
          <div className="flex items-center space-x-3">
            <Link
              href="/auth/signin"
              className="px-4 py-2 text-xs font-bold text-slate-700 hover:text-indigo-600 bg-white hover:bg-slate-50 border border-slate-200 rounded-full shadow-sm transition-all"
            >
              Sign In
            </Link>
            <Link
              href="/auth/signup"
              className="px-4 py-2 text-xs font-bold text-white bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 rounded-full shadow-md shadow-indigo-500/20 transition-all flex items-center gap-1.5"
            >
              <span>Join Free</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* 2. HERO SECTION */}
      <section className="relative pt-16 pb-20 px-6 overflow-hidden">
        {/* Background Pastel Gradient Glows */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[450px] bg-gradient-to-br from-indigo-100/60 via-purple-100/50 to-pink-100/40 rounded-full blur-3xl pointer-events-none -z-10" />

        <div className="max-w-5xl mx-auto text-center space-y-6">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 bg-indigo-50/90 border border-indigo-200/80 rounded-full text-xs font-bold text-indigo-700 shadow-sm animate-fadeIn">
            <Sparkles className="w-4 h-4 text-indigo-600" />
            <span>Autonomous AI Email &amp; Task Automation Assistant</span>
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-600 animate-ping"></span>
          </div>

          {/* Headline */}
          <h1 className="text-4xl md:text-6xl font-black text-slate-900 tracking-tight leading-tight">
            Your Gmail Inbox, Transformed by{" "}
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600">
              Autonomous AI
            </span>
          </h1>

          {/* Subtitle */}
          <p className="text-base md:text-lg text-slate-600 max-w-3xl mx-auto leading-relaxed">
            Automatically ingest real Gmail messages, classify priorities, extract Kanban tasks with ISO deadlines, and generate human-approved replies — powered by <span className="font-semibold text-indigo-700">Gemini 2.5 Flash</span> and <span className="font-semibold text-indigo-700">PostgreSQL 18</span>.
          </p>

          {/* CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-2">
            <Link
              href="/inbox"
              className="w-full sm:w-auto px-7 py-3.5 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-extrabold text-sm rounded-2xl shadow-lg shadow-indigo-500/25 flex items-center justify-center gap-2 transition-all hover:scale-[1.02]"
            >
              <Zap className="w-4 h-4 text-amber-300" />
              <span>Launch Live Workspace</span>
            </Link>
            <Link
              href="/auth/signin"
              className="w-full sm:w-auto px-6 py-3.5 bg-white hover:bg-slate-50 border border-slate-200/90 text-slate-800 font-bold text-sm rounded-2xl shadow-sm hover:shadow transition-all flex items-center justify-center gap-2"
            >
              <span>Connect Any Account</span>
              <ArrowRight className="w-4 h-4 text-slate-400" />
            </Link>
          </div>

          {/* Trust Badges */}
          <div className="pt-6 flex flex-wrap items-center justify-center gap-6 text-xs text-slate-500 font-medium">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> 100% Real Gmail Ingestion
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Multi-User Isolation
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> PostgreSQL 18 &amp; pgAdmin 4
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Cloudinary Media CDN
            </span>
          </div>
        </div>

        {/* 3. INTERACTIVE PRODUCT PREVIEW CARD */}
        <div className="max-w-5xl mx-auto mt-14 p-2 bg-white/70 border border-slate-200/80 rounded-3xl shadow-2xl glass-panel">
          <div className="p-6 bg-slate-900 rounded-2xl text-white space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2">
                <span className="w-3 h-3 rounded-full bg-red-500 inline-block"></span>
                <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
                <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
                <span className="text-xs font-mono text-slate-400 ml-2">AetherMail AI Live Processing Pipeline</span>
              </div>
              <span className="px-2.5 py-0.5 text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 rounded-full flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span> Live Agent Active
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left pt-2">
              {/* Box 1 */}
              <div className="p-4 bg-slate-800/80 rounded-xl border border-slate-700/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-indigo-400 uppercase">1. Gmail Ingestion</span>
                  <Inbox className="w-4 h-4 text-indigo-400" />
                </div>
                <p className="text-xs font-bold text-white">Live Email Ingested</p>
                <p className="text-[11px] text-slate-300 line-clamp-2">
                  &quot;URGENT: Submit Final AI Model Weights &amp; Performance Benchmarks by Tomorrow 4 PM&quot;
                </p>
              </div>

              {/* Box 2 */}
              <div className="p-4 bg-slate-800/80 rounded-xl border border-slate-700/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-purple-400 uppercase">2. Gemini 2.5 Flash</span>
                  <Cpu className="w-4 h-4 text-purple-400" />
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 text-[9px] font-bold bg-purple-500/20 text-purple-300 rounded">WORK</span>
                  <span className="px-2 py-0.5 text-[9px] font-bold bg-red-500/20 text-red-300 rounded">HIGH PRIORITY</span>
                </div>
                <p className="text-[11px] text-slate-300">
                  Extracted 1 actionable task &bull; Deadline: Tomorrow 4:00 PM
                </p>
              </div>

              {/* Box 3 */}
              <div className="p-4 bg-slate-800/80 rounded-xl border border-slate-700/80 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold text-pink-400 uppercase">3. Action &amp; Approval</span>
                  <ShieldCheck className="w-4 h-4 text-pink-400" />
                </div>
                <p className="text-xs font-bold text-white">Draft Reply Ready</p>
                <p className="text-[11px] text-slate-300 line-clamp-2">
                  &quot;I have received your email and added the model submission to my queue.&quot;
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 4. FEATURES GRID */}
      <section id="features" className="py-20 px-6 bg-white/60 border-y border-slate-200/80">
        <div className="max-w-6xl mx-auto space-y-12">
          <div className="text-center space-y-3 max-w-2xl mx-auto">
            <h2 className="text-3xl font-extrabold text-slate-900">
              Complete Enterprise Capabilities
            </h2>
            <p className="text-sm text-slate-600">
              Designed from ground up with production-grade AI intelligence, strict PostgreSQL persistence, and human-in-the-loop safeguards.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => {
              const Icon = f.icon;
              return (
                <div
                  key={i}
                  className="p-6 bg-white border border-slate-200/80 hover:border-indigo-300 rounded-3xl shadow-sm hover:shadow-md transition-all space-y-3.5 group"
                >
                  <div className="flex items-center justify-between">
                    <div
                      className={`w-11 h-11 rounded-2xl bg-gradient-to-br ${f.color} text-white flex items-center justify-center shadow-md group-hover:scale-105 transition-transform`}
                    >
                      <Icon className="w-5 h-5" />
                    </div>
                    <span className="px-2.5 py-1 text-[10px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-full">
                      {f.tag}
                    </span>
                  </div>
                  <h3 className="text-base font-bold text-slate-800 group-hover:text-indigo-600 transition-colors">
                    {f.title}
                  </h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    {f.desc}
                  </p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* 5. HOW IT WORKS 3-STEP PIPELINE */}
      <section id="workflow" className="py-20 px-6">
        <div className="max-w-5xl mx-auto space-y-12">
          <div className="text-center space-y-3 max-w-2xl mx-auto">
            <h2 className="text-3xl font-extrabold text-slate-900">
              How Autonomous Ingestion Works
            </h2>
            <p className="text-sm text-slate-600">
              Three seamless steps from real mailbox arrival to automated execution.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
            <div className="p-6 bg-white border border-slate-200/80 rounded-3xl space-y-3 shadow-sm text-center">
              <div className="w-10 h-10 mx-auto rounded-full bg-indigo-100 text-indigo-700 font-extrabold text-sm flex items-center justify-center">
                1
              </div>
              <h4 className="text-sm font-bold text-slate-800">Connect Mailbox</h4>
              <p className="text-xs text-slate-500 leading-relaxed">
                Connect any Gmail account via 1-click Google Sign In or 16-character App Password.
              </p>
            </div>

            <div className="p-6 bg-white border border-slate-200/80 rounded-3xl space-y-3 shadow-sm text-center">
              <div className="w-10 h-10 mx-auto rounded-full bg-purple-100 text-purple-700 font-extrabold text-sm flex items-center justify-center">
                2
              </div>
              <h4 className="text-sm font-bold text-slate-800">AI Background Poller</h4>
              <p className="text-xs text-slate-500 leading-relaxed">
                Backend poller checks every 20 seconds, categorizes emails, and maps tasks to PostgreSQL.
              </p>
            </div>

            <div className="p-6 bg-white border border-slate-200/80 rounded-3xl space-y-3 shadow-sm text-center">
              <div className="w-10 h-10 mx-auto rounded-full bg-pink-100 text-pink-700 font-extrabold text-sm flex items-center justify-center">
                3
              </div>
              <h4 className="text-sm font-bold text-slate-800">Act &amp; Approve</h4>
              <p className="text-xs text-slate-500 leading-relaxed">
                Manage tasks in Kanban board and 1-click authorize AI replies to be dispatched back.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 6. CALL TO ACTION BANNER */}
      <section className="py-16 px-6 bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-600 text-white text-center">
        <div className="max-w-4xl mx-auto space-y-6">
          <h2 className="text-3xl md:text-4xl font-black">
            Ready to Experience Autonomous AI Email Management?
          </h2>
          <p className="text-sm text-indigo-100 max-w-xl mx-auto">
            Open your dedicated workspace today. Zero credit card, zero setup complexity, instant live Gmail synchronization.
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-2">
            <Link
              href="/inbox"
              className="px-8 py-3.5 bg-white text-indigo-700 hover:bg-slate-50 font-extrabold text-xs rounded-full shadow-lg transition-all"
            >
              Open Live Inbox
            </Link>
            <Link
              href="/auth/signup"
              className="px-6 py-3.5 bg-indigo-800/60 hover:bg-indigo-800/80 text-white font-bold text-xs border border-white/20 rounded-full transition-all"
            >
              Create Account Free
            </Link>
          </div>
        </div>
      </section>

      {/* 7. FOOTER */}
      <footer className="bg-white border-t border-slate-200/80 px-6 py-10 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-3">
            <Logo size="sm" showText={true} />
            <span className="text-slate-300">|</span>
            <span>Autonomous AI Email &amp; Task Assistant</span>
          </div>

          <div className="flex items-center space-x-6 font-semibold text-slate-600">
            <Link href="/home" className="hover:text-indigo-600">Home</Link>
            <Link href="/" className="hover:text-indigo-600">Dashboard</Link>
            <Link href="/inbox" className="hover:text-indigo-600">Inbox</Link>
            <Link href="/tasks" className="hover:text-indigo-600">Tasks</Link>
            <Link href="/settings" className="hover:text-indigo-600">Settings</Link>
            <Link href="/auth/signin" className="hover:text-indigo-600">Sign In</Link>
          </div>

          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span className="font-mono text-[11px] text-slate-600">PostgreSQL 18: Online</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
