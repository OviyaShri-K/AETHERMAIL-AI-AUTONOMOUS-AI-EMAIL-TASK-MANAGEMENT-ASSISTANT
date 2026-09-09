"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useUser } from "@/context/UserContext";
import { Logo } from "./Logo";
import {
  Home,
  LayoutDashboard,
  Inbox,
  CheckSquare,
  ShieldCheck,
  HardDrive,
  Settings,
  Database,
  Cloud,
  Layers,
  ChevronRight,
} from "lucide-react";

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const { currentUser, openLoginModal } = useUser();

  const navItems = [
    { href: "/home", label: "Home Page", icon: Home },
    { href: "/", label: "Dashboard", icon: LayoutDashboard },
    { href: "/inbox", label: "Live Inbox", icon: Inbox },
    { href: "/tasks", label: "Kanban Tasks", icon: CheckSquare },
    { href: "/approvals", label: "Approvals Gate", icon: ShieldCheck },
    { href: "/attachments", label: "Media Vault", icon: HardDrive },
    { href: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <aside className="w-64 flex-shrink-0 min-h-screen bg-white/80 border-r border-slate-200/80 flex flex-col justify-between p-4 glass-panel sticky top-0 h-screen overflow-y-auto">
      {/* Brand Header */}
      <div>
        <div className="px-2 py-3 mb-5">
          <Logo size="md" showText={true} />
        </div>

        {/* Active Account Pill Card */}
        <div className="mb-5 p-3.5 bg-gradient-to-br from-indigo-50/70 via-purple-50/50 to-pink-50/40 border border-indigo-100 rounded-2xl shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-[10px] uppercase font-bold text-indigo-600 tracking-wider">
              Connected Workspace
            </span>
            <button
              onClick={openLoginModal}
              className="text-[10px] text-indigo-600 hover:text-indigo-800 font-bold hover:underline"
            >
              Switch
            </button>
          </div>
          <div className="flex items-center space-x-2.5 min-w-0">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-white flex items-center justify-center font-bold text-xs shadow-sm flex-shrink-0">
              {currentUser?.avatar || "🎓"}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-bold text-slate-800 truncate">
                {currentUser?.email || "Loading Workspace..."}
              </p>
              <p className="text-[10px] text-slate-500 truncate">
                {currentUser?.name || "User Profile"}
              </p>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="space-y-1.5">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center justify-between px-3.5 py-2.5 rounded-2xl text-xs font-bold transition-all ${
                  isActive
                    ? "bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white shadow-md shadow-indigo-500/20"
                    : "text-slate-600 hover:text-slate-900 hover:bg-slate-100/80"
                }`}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-slate-500"}`} />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-3.5 h-3.5 text-white/80" />}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer System Status */}
      <div className="pt-4 border-t border-slate-200/80 space-y-2">
        <div className="p-3 bg-slate-50/80 border border-slate-200/60 rounded-2xl space-y-2 text-[11px]">
          <div className="flex items-center justify-between text-slate-600">
            <span className="flex items-center gap-1.5 font-semibold">
              <Database className="w-3.5 h-3.5 text-indigo-500" /> PostgreSQL
            </span>
            <span className="text-emerald-600 font-bold font-mono">ai_email_db</span>
          </div>
          <div className="flex items-center justify-between text-slate-600">
            <span className="flex items-center gap-1.5 font-semibold">
              <Cloud className="w-3.5 h-3.5 text-cyan-500" /> Cloudinary CDN
            </span>
            <span className="text-indigo-600 font-bold font-mono">n4tj82yc</span>
          </div>
          <div className="flex items-center justify-between text-slate-600">
            <span className="flex items-center gap-1.5 font-semibold">
              <Layers className="w-3.5 h-3.5 text-purple-500" /> AI Accuracy
            </span>
            <span className="text-purple-600 font-bold">100.0%</span>
          </div>
        </div>
        <p className="text-[10px] text-center text-slate-400 font-medium">
          AetherMail AI Production Suite v1.0
        </p>
      </div>
    </aside>
  );
};
