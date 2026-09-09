"use client";

import React, { useEffect, useState } from "react";
import { useUser } from "@/context/UserContext";
import {
  fetchTasks,
  createCustomTask,
  updateTaskStatus,
  deleteTaskById,
  TaskItem,
} from "@/lib/api";
import {
  CheckSquare,
  Plus,
  CheckCircle2,
  Trash2,
  Calendar,
  Play,
  RotateCcw,
  RefreshCw,
  X,
} from "lucide-react";

export default function KanbanTasksPage() {
  const { currentUser } = useUser();
  const [tasks, setTasks] = useState<TaskItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreateOpen, setIsCreateOpen] = useState(false);
  const [taskDesc, setTaskDesc] = useState("");
  const [createLoading, setCreateLoading] = useState(false);

  const loadTasks = async () => {
    setLoading(true);
    try {
      const data = await fetchTasks({ user_email: currentUser?.email });
      setTasks(data);
    } catch (err) {
      console.warn("Failed to load tasks:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, [currentUser]);

  const handleStatusChange = async (taskId: number, newStatus: string) => {
    try {
      await updateTaskStatus(taskId, { status: newStatus });
      setTasks((prev) =>
        prev.map((t) => (t.id === taskId ? { ...t, status: newStatus } : t))
      );
    } catch (err) {
      console.error("Failed to update status:", err);
    }
  };

  const handleDelete = async (taskId: number) => {
    try {
      await deleteTaskById(taskId);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
    } catch (err) {
      console.error("Failed to delete task:", err);
    }
  };

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskDesc.trim()) return;
    setCreateLoading(true);
    try {
      const newTask = await createCustomTask({
        recipient: currentUser?.email || "user@workspace.com",
        description: taskDesc.trim(),
      });
      setTasks((prev) => [newTask, ...prev]);
      setTaskDesc("");
      setIsCreateOpen(false);
    } catch (err) {
      console.error("Failed to create task:", err);
    } finally {
      setCreateLoading(false);
    }
  };

  const pendingTasks = tasks.filter(
    (t) => !t.status || t.status.toLowerCase() === "pending"
  );
  const inProgressTasks = tasks.filter(
    (t) => t.status && t.status.toLowerCase() === "in_progress"
  );
  const completedTasks = tasks.filter(
    (t) => t.status && t.status.toLowerCase() === "completed"
  );

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-800 flex items-center gap-2.5">
            <CheckSquare className="w-6 h-6 text-indigo-600" />
            Kanban Task Board
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Managing tasks for:{" "}
            <span className="font-bold text-indigo-700 font-mono">
              {currentUser?.email || "Active User"}
            </span>
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsCreateOpen(true)}
            className="px-4 py-2 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs rounded-2xl shadow-sm shadow-indigo-500/20 flex items-center gap-1.5 transition-all"
          >
            <Plus className="w-4 h-4" />
            Create Custom Task
          </button>
          <button
            onClick={loadTasks}
            className="p-2 bg-white hover:bg-slate-50 border border-slate-200 text-slate-600 rounded-2xl shadow-sm transition-all"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-indigo-600" : ""}`} />
          </button>
        </div>
      </div>

      {/* 3 Pastel Kanban Columns */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Column 1: Pending */}
        <div className="bg-gradient-to-b from-amber-50/50 to-white border border-amber-200/80 rounded-3xl p-5 flex flex-col glass-panel shadow-sm">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-amber-100">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span>
              <h2 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                Pending Actions
              </h2>
            </div>
            <span className="px-2.5 py-0.5 text-xs font-bold bg-amber-100 text-amber-700 rounded-full">
              {pendingTasks.length}
            </span>
          </div>

          <div className="space-y-3 flex-1 overflow-y-auto max-h-[68vh] pr-1">
            {pendingTasks.map((t) => (
              <div
                key={t.id}
                className="p-4 bg-white border border-slate-200/80 hover:border-amber-400 rounded-2xl space-y-2.5 transition-all glass-card shadow-sm hover:shadow"
              >
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs font-bold text-slate-800 leading-snug">
                    {t.title}
                  </p>
                  <span
                    className={`px-2 py-0.5 text-[9px] font-bold uppercase rounded-full ${
                      t.priority === "High"
                        ? "bg-red-50 text-red-600 border border-red-200"
                        : "bg-amber-50 text-amber-600 border border-amber-200"
                    }`}
                  >
                    {t.priority}
                  </span>
                </div>

                {t.description && (
                  <p className="text-[11px] text-slate-500 line-clamp-2">
                    {t.description}
                  </p>
                )}

                {t.deadline && (
                  <div className="flex items-center gap-1.5 text-[10px] text-indigo-600 font-mono bg-indigo-50/60 px-2.5 py-1 rounded-xl">
                    <Calendar className="w-3 h-3 text-indigo-500" />
                    Due: {new Date(t.deadline).toLocaleDateString()}
                  </div>
                )}

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  <button
                    onClick={() => handleStatusChange(t.id, "in_progress")}
                    className="text-[11px] font-bold text-indigo-600 hover:text-indigo-700 flex items-center gap-1"
                  >
                    <Play className="w-3 h-3" /> Start
                  </button>
                  <button
                    onClick={() => handleDelete(t.id)}
                    className="text-slate-400 hover:text-red-500 transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Column 2: In Progress */}
        <div className="bg-gradient-to-b from-blue-50/50 to-white border border-blue-200/80 rounded-3xl p-5 flex flex-col glass-panel shadow-sm">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-blue-100">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-500"></span>
              <h2 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                In Progress
              </h2>
            </div>
            <span className="px-2.5 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-full">
              {inProgressTasks.length}
            </span>
          </div>

          <div className="space-y-3 flex-1 overflow-y-auto max-h-[68vh] pr-1">
            {inProgressTasks.map((t) => (
              <div
                key={t.id}
                className="p-4 bg-white border border-slate-200/80 hover:border-blue-400 rounded-2xl space-y-2.5 transition-all glass-card shadow-sm hover:shadow"
              >
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs font-bold text-slate-800 leading-snug">
                    {t.title}
                  </p>
                  <span className="px-2 py-0.5 text-[9px] font-bold uppercase rounded-full bg-blue-50 text-blue-600 border border-blue-200">
                    {t.priority}
                  </span>
                </div>

                {t.description && (
                  <p className="text-[11px] text-slate-500 line-clamp-2">
                    {t.description}
                  </p>
                )}

                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  <button
                    onClick={() => handleStatusChange(t.id, "completed")}
                    className="text-[11px] font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5" /> Complete
                  </button>
                  <button
                    onClick={() => handleStatusChange(t.id, "pending")}
                    className="text-slate-400 hover:text-slate-600"
                  >
                    <RotateCcw className="w-3 h-3" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Column 3: Completed */}
        <div className="bg-gradient-to-b from-emerald-50/50 to-white border border-emerald-200/80 rounded-3xl p-5 flex flex-col glass-panel shadow-sm">
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-emerald-100">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h2 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
                Completed
              </h2>
            </div>
            <span className="px-2.5 py-0.5 text-xs font-bold bg-emerald-100 text-emerald-700 rounded-full">
              {completedTasks.length}
            </span>
          </div>

          <div className="space-y-3 flex-1 overflow-y-auto max-h-[68vh] pr-1">
            {completedTasks.map((t) => (
              <div
                key={t.id}
                className="p-4 bg-white/70 border border-slate-200/60 rounded-2xl space-y-2 opacity-80 hover:opacity-100 transition-all shadow-sm"
              >
                <div className="flex items-start justify-between gap-2">
                  <p className="text-xs font-semibold text-slate-400 line-through">
                    {t.title}
                  </p>
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                </div>
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
                  <button
                    onClick={() => handleStatusChange(t.id, "in_progress")}
                    className="text-[10px] text-slate-500 hover:text-indigo-600 font-medium"
                  >
                    Reopen
                  </button>
                  <button
                    onClick={() => handleDelete(t.id)}
                    className="text-slate-400 hover:text-red-500 transition-colors"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Create Custom Task Modal */}
      {isCreateOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm animate-fadeIn">
          <div className="relative w-full max-w-md p-6 bg-white border border-slate-200 rounded-3xl shadow-2xl glass-panel">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <h2 className="text-base font-bold text-slate-800 flex items-center gap-2">
                <Plus className="w-5 h-5 text-indigo-600" />
                Create Custom Task
              </h2>
              <button
                onClick={() => setIsCreateOpen(false)}
                className="p-1.5 text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-full"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleCreateTask} className="mt-4 space-y-3.5">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Assignee Account
                </label>
                <input
                  type="text"
                  disabled
                  value={currentUser?.email || ""}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-indigo-700 font-mono font-bold"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Task Description (Include deadline like &apos;by tomorrow 4 PM&apos;)
                </label>
                <textarea
                  required
                  rows={4}
                  value={taskDesc}
                  onChange={(e) => setTaskDesc(e.target.value)}
                  placeholder="e.g. Verify PostgreSQL database records and submit final project presentation by Friday 5 PM"
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-800 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:bg-white"
                />
              </div>

              <button
                type="submit"
                disabled={createLoading}
                className="w-full py-2.5 px-4 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs rounded-xl shadow-md shadow-indigo-500/20 flex items-center justify-center gap-1.5 transition-all disabled:opacity-50"
              >
                {createLoading ? "Creating..." : "Save & Calculate Deadline"}
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
