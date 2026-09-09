import type { Metadata } from "next";
import "./globals.css";
import { UserProvider } from "@/context/UserContext";
import { AppShell } from "@/components/AppShell";

export const metadata: Metadata = {
  title: "AetherMail AI — Autonomous AI Email & Task Management Assistant",
  description:
    "Autonomous AI assistant for email categorization, task extraction, human approvals, and Cloudinary media vault.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen text-slate-900 antialiased font-sans">
        <UserProvider>
          <AppShell>{children}</AppShell>
        </UserProvider>
      </body>
    </html>
  );
}

