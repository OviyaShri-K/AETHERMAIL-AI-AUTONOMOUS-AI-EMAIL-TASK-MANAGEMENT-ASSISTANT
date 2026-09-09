"use client";

import React, { useEffect, useState } from "react";
import {
  fetchAttachments,
  uploadAttachmentToCloudinary,
  AttachmentItem,
} from "@/lib/api";
import {
  HardDrive,
  Upload,
  Cloud,
  FileText,
  Image as ImageIcon,
  ExternalLink,
  Sparkles,
  CheckCircle2,
} from "lucide-react";

export default function CloudinaryAttachmentsPage() {
  const [attachments, setAttachments] = useState<AttachmentItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [feedback, setFeedback] = useState("");

  const loadFiles = async () => {
    setLoading(true);
    try {
      const data = await fetchAttachments();
      setAttachments(data);
    } catch (err) {
      console.warn("Failed to load attachments:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setFeedback("");
    try {
      const res = await uploadAttachmentToCloudinary(file);
      setFeedback(`File '${file.name}' uploaded to Cloudinary CDN!`);
      setAttachments((prev) => [res.attachment, ...prev]);
      setTimeout(() => setFeedback(""), 4000);
    } catch (err) {
      console.error("Upload error:", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-800 flex items-center gap-2.5">
            <HardDrive className="w-6 h-6 text-cyan-600" />
            Cloudinary Media Vault
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Secure cloud storage for email invoices, PDF documents, and image attachments
          </p>
        </div>

        <label className="px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold text-xs rounded-2xl shadow-sm shadow-cyan-500/20 flex items-center gap-2 cursor-pointer transition-all self-start md:self-auto">
          <Upload className="w-4 h-4" />
          {uploading ? "Uploading to Cloud..." : "Upload File to Cloudinary"}
          <input
            type="file"
            onChange={handleFileUpload}
            disabled={uploading}
            className="hidden"
          />
        </label>
      </div>

      {feedback && (
        <div className="p-3.5 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold rounded-2xl flex items-center gap-2 animate-fadeIn shadow-sm">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          {feedback}
        </div>
      )}

      {/* Cloudinary Integration Status Card */}
      <div className="p-6 bg-gradient-to-r from-cyan-50/80 via-sky-50/70 to-indigo-50/60 border border-cyan-100 rounded-3xl glass-panel flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center space-x-3.5">
          <div className="w-12 h-12 bg-white text-cyan-600 rounded-2xl flex items-center justify-center shadow-sm">
            <Cloud className="w-6 h-6" />
          </div>
          <div>
            <span className="px-2.5 py-0.5 text-[10px] font-bold bg-cyan-100 text-cyan-800 rounded-full uppercase tracking-wider">
              Cloudinary CDN Connected
            </span>
            <p className="text-xs text-slate-600 mt-1">
              Cloud Name: <span className="font-mono text-cyan-700 font-bold">n4tj82yc</span> &bull; Status: <span className="text-emerald-600 font-bold">Active</span>
            </p>
          </div>
        </div>
      </div>

      {/* Grid of Files */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        {loading ? (
          <div className="col-span-full py-16 text-center text-xs text-slate-400">
            Fetching files from Cloudinary storage...
          </div>
        ) : attachments.length > 0 ? (
          attachments.map((att) => (
            <div
              key={att.id}
              className="p-5 bg-white/90 border border-slate-200/80 hover:border-cyan-300 rounded-3xl space-y-3 glass-card shadow-sm hover:shadow-md transition-all"
            >
              <div className="flex items-start justify-between gap-2">
                <div className="p-3 bg-cyan-50 text-cyan-600 rounded-2xl">
                  {att.file_type && att.file_type.includes("image") ? (
                    <ImageIcon className="w-6 h-6" />
                  ) : (
                    <FileText className="w-6 h-6" />
                  )}
                </div>
                <a
                  href={att.cloudinary_url}
                  target="_blank"
                  rel="noreferrer"
                  className="p-2 text-slate-400 hover:text-cyan-600 bg-slate-50 hover:bg-cyan-50 rounded-xl transition-colors"
                >
                  <ExternalLink className="w-4 h-4" />
                </a>
              </div>

              <div>
                <h3 className="text-xs font-bold text-slate-800 truncate">
                  {att.filename}
                </h3>
                <p className="text-[11px] text-slate-400 mt-0.5">
                  Size: {Math.round(att.file_size_bytes / 1024)} KB &bull; {att.file_type || "Document"}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px]">
                <span className="text-slate-400 font-mono text-[10px]">
                  {new Date(att.uploaded_at).toLocaleDateString()}
                </span>
                <a
                  href={att.cloudinary_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs font-bold text-cyan-600 hover:text-cyan-700"
                >
                  View on CDN &rarr;
                </a>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full py-16 text-center text-xs text-slate-400 bg-white/60 border border-dashed border-slate-200 rounded-3xl">
            No attachments in Cloudinary vault yet. Upload an attachment above!
          </div>
        )}
      </div>
    </div>
  );
}
