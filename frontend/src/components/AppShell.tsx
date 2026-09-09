"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { Sidebar } from "./Sidebar";
import { Navbar } from "./Navbar";
import { UserLoginModal } from "./UserLoginModal";

export const AppShell: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const pathname = usePathname();
  const isPublicPage = pathname.startsWith("/home") || pathname.startsWith("/auth");

  if (isPublicPage) {
    return (
      <div className="min-h-screen bg-[#fcfbfe] text-slate-900 flex flex-col">
        {children}
        <UserLoginModal />
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-[#faf8fc]">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0">
        <Navbar />
        <main className="flex-1 p-5 md:p-8 max-w-7xl w-full mx-auto">
          {children}
        </main>
      </div>
      <UserLoginModal />
    </div>
  );
};
