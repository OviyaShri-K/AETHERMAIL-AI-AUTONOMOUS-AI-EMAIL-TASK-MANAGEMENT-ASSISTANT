"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { UserProfile, fetchUsersDirectory, loginOrSwitchUser } from "@/lib/api";

interface UserContextType {
  currentUser: UserProfile | null;
  usersList: UserProfile[];
  isLoadingUser: boolean;
  isLoginModalOpen: boolean;
  openLoginModal: () => void;
  closeLoginModal: () => void;
  switchUser: (email: string) => Promise<void>;
  authenticateUser: (
    email: string,
    name?: string,
    authType?: string,
    password?: string
  ) => Promise<UserProfile>;
  refreshUsers: (targetEmail?: string) => Promise<void>;
}

const DEFAULT_USER: UserProfile = {
  email: "alex.miller@innovatetech.io",
  name: "Alex Miller",
  role: "AI Project Lead / Administrator",
  avatar: "👨‍💻",
  email_count: 0,
  task_count: 0,
  pending_approvals: 0,
  last_active: "Active Now",
  is_authenticated: true,
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<UserProfile | null>(DEFAULT_USER);
  const [usersList, setUsersList] = useState<UserProfile[]>([]);
  const [isLoadingUser, setIsLoadingUser] = useState<boolean>(false);
  const [isLoginModalOpen, setIsLoginModalOpen] = useState<boolean>(false);

  const refreshUsers = async (targetEmail?: string) => {
    try {
      const data = await fetchUsersDirectory();
      setUsersList(data);
      
      const activeMail = targetEmail || (typeof window !== "undefined" ? JSON.parse(localStorage.getItem("ai_assistant_active_user") || "{}").email : null);
      if (activeMail) {
        const cleanMail = activeMail.trim().toLowerCase();
        const found = data.find((u) => u.email.toLowerCase() === cleanMail);
        if (found) {
          setCurrentUser(found);
          localStorage.setItem("ai_assistant_active_user", JSON.stringify(found));
        } else {
          const rawName = cleanMail.split("@")[0].replace(".", " ");
          const name = cleanMail.includes("alex miller")
            ? "Alex Miller"
            : cleanMail.includes("sarah jenkins") || cleanMail.includes("enterprise")
            ? "Sarah Jenkins"
            : rawName.charAt(0).toUpperCase() + rawName.slice(1);
          const fallbackUser: UserProfile = {
            email: cleanMail,
            name: name,
            role: "Active Workspace User",
            avatar: cleanMail.includes("alex miller") ? "👨‍💻" : (cleanMail.includes("enterprise") ? "🎓" : (cleanMail.includes("sarah jenkins") ? "👩‍💻" : "👤")),
            email_count: 0,
            task_count: 0,
            pending_approvals: 0,
            last_active: "Active Now",
            is_authenticated: true,
          };
          setCurrentUser(fallbackUser);
          localStorage.setItem("ai_assistant_active_user", JSON.stringify(fallbackUser));
        }
      }
    } catch (err) {
      console.warn("Failed to fetch users directory:", err);
    }
  };

  useEffect(() => {
    // Check localStorage on initial client mount
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("ai_assistant_active_user");
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          if (parsed && parsed.email) {
            setCurrentUser(parsed);
            refreshUsers(parsed.email);
            return;
          }
        } catch (e) {}
      }
    }
    refreshUsers(DEFAULT_USER.email);
  }, []);

  const switchUser = async (email: string) => {
    setIsLoadingUser(true);
    const cleanEmail = email.trim().toLowerCase();
    const rawName = cleanEmail.split("@")[0].replace(".", " ");
    const name = cleanEmail.includes("alex miller") ? "Alex Miller" : (cleanEmail.includes("sarah jenkins") || cleanEmail.includes("enterprise") ? "Sarah Jenkins" : rawName.charAt(0).toUpperCase() + rawName.slice(1));
    const immediateUser: UserProfile = {
      email: cleanEmail,
      name: name,
      role: "Active Workspace User",
      avatar: cleanEmail.includes("alex miller") ? "👨‍💻" : (cleanEmail.includes("enterprise") ? "🎓" : (cleanEmail.includes("sarah jenkins") ? "👩‍💻" : "👤")),
      email_count: 0,
      task_count: 0,
      pending_approvals: 0,
      last_active: "Active Now",
      is_authenticated: true,
    };
    
    // Immediately set local and storage state
    setCurrentUser(immediateUser);
    if (typeof window !== "undefined") {
      localStorage.setItem("ai_assistant_active_user", JSON.stringify(immediateUser));
    }

    try {
      const profile = await loginOrSwitchUser(cleanEmail, name, "instant");
      setCurrentUser(profile);
      if (typeof window !== "undefined") {
        localStorage.setItem("ai_assistant_active_user", JSON.stringify(profile));
      }
      await refreshUsers(cleanEmail);
    } catch (err) {
      console.warn("Backend user switch fallback:", err);
    } finally {
      setIsLoadingUser(false);
      setIsLoginModalOpen(false);
    }
  };

  const authenticateUser = async (
    email: string,
    name?: string,
    authType: string = "instant",
    password?: string
  ): Promise<UserProfile> => {
    setIsLoadingUser(true);
    const cleanEmail = email.trim().toLowerCase();
    const rawName = cleanEmail.split("@")[0].replace(".", " ");
    const displayName = name || (cleanEmail.includes("alex miller") ? "Alex Miller" : (cleanEmail.includes("sarah jenkins") || cleanEmail.includes("enterprise") ? "Sarah Jenkins" : rawName.charAt(0).toUpperCase() + rawName.slice(1)));
    
    const immediateProfile: UserProfile = {
      email: cleanEmail,
      name: displayName,
      role: "Active Workspace User",
      avatar: cleanEmail.includes("alex miller") ? "👨‍💻" : (cleanEmail.includes("enterprise") ? "🎓" : (cleanEmail.includes("sarah jenkins") ? "👩‍💻" : "👤")),
      email_count: 0,
      task_count: 0,
      pending_approvals: 0,
      last_active: "Active Now",
      is_authenticated: true,
    };
    
    setCurrentUser(immediateProfile);
    if (typeof window !== "undefined") {
      localStorage.setItem("ai_assistant_active_user", JSON.stringify(immediateProfile));
    }

    try {
      const profile = await loginOrSwitchUser(cleanEmail, displayName, authType, password);
      setCurrentUser(profile);
      if (typeof window !== "undefined") {
        localStorage.setItem("ai_assistant_active_user", JSON.stringify(profile));
      }
      await refreshUsers(cleanEmail);
      setIsLoginModalOpen(false);
      return profile;
    } catch (err) {
      setIsLoginModalOpen(false);
      return immediateProfile;
    } finally {
      setIsLoadingUser(false);
    }
  };

  const openLoginModal = () => setIsLoginModalOpen(true);
  const closeLoginModal = () => setIsLoginModalOpen(false);

  return (
    <UserContext.Provider
      value={{
        currentUser,
        usersList,
        isLoadingUser,
        isLoginModalOpen,
        openLoginModal,
        closeLoginModal,
        switchUser,
        authenticateUser,
        refreshUsers,
      }}
    >
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};
