"use client";

import React from "react";

interface LogoProps {
  size?: "sm" | "md" | "lg";
  showText?: boolean;
}

export const Logo: React.FC<LogoProps> = ({ size = "md", showText = true }) => {
  const iconSizes = {
    sm: "w-8 h-8",
    md: "w-10 h-10",
    lg: "w-14 h-14",
  };

  const textSizes = {
    sm: "text-xs",
    md: "text-sm",
    lg: "text-xl",
  };

  return (
    <div className="flex items-center space-x-3">
      {/* Sleek Modern AI Mail Geometric SVG Logo */}
      <div
        className={`${iconSizes[size]} relative flex items-center justify-center rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-500 shadow-md shadow-indigo-500/25 p-2`}
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full text-white"
        >
          {/* Email Envelope with AI Sparkle & Wing */}
          <path
            d="M3 7.5L12 13.5L21 7.5"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
          <rect
            x="3"
            y="5"
            width="18"
            height="14"
            rx="3"
            stroke="currentColor"
            strokeWidth="2"
          />
          <circle cx="18" cy="6" r="3" fill="#38BDF8" />
          <path
            d="M17 6L19 6M18 5L18 7"
            stroke="white"
            strokeWidth="1.2"
            strokeLinecap="round"
          />
        </svg>
      </div>

      {showText && (
        <div>
          <div className="flex items-center gap-1.5">
            <span
              className={`${textSizes[size]} font-extrabold tracking-tight text-slate-800`}
            >
              AetherMail
            </span>
            <span className="px-1.5 py-0.2 text-[9px] font-black bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-md tracking-wider">
              AI
            </span>
          </div>
          <p className="text-[10px] font-bold text-slate-500 tracking-wider uppercase">
            Autonomous Assistant
          </p>
        </div>
      )}
    </div>
  );
};
