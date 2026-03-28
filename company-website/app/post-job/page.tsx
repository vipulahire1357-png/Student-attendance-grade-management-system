"use client";

import JobForm from "@/components/JobForm";
import { useQuery } from "@tanstack/react-query";
import { jobsAPI, type JobOut } from "@/services/api";
import {
  Briefcase,
  Sparkles,
  CheckCircle,
  Clock,
  MapPin,
  TrendingUp,
} from "lucide-react";

export default function PostJobPage() {
  const { data: jobs } = useQuery<JobOut[]>({
    queryKey: ["all-jobs"],
    queryFn: async () => (await jobsAPI.listJobs({ limit: 100 })).data,
  });

  const recentJobs = jobs?.slice(-4).reverse() ?? [];

  return (
    <div className="space-y-8 pt-6 animate-fade-in">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{
              background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
              boxShadow: "0 0 16px rgba(99,102,241,0.35)",
            }}
          >
            <Briefcase size={15} className="text-white" />
          </div>
          <h1
            className="text-2xl font-bold"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            Post a Job
          </h1>
        </div>
        <p className="text-sm" style={{ color: "var(--text-muted)" }}>
          Publish a new listing and let our AI match it with the best student candidates.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form — 2 cols */}
        <div className="lg:col-span-2 glass-card p-7">
          <div className="flex items-center gap-2 mb-6 pb-4" style={{ borderBottom: "1px solid rgba(99,102,241,0.12)" }}>
            <Sparkles size={16} style={{ color: "#6366f1" }} />
            <h2 className="font-semibold">Job Details</h2>
          </div>
          <JobForm />
        </div>

        {/* Sidebar */}
        <div className="flex flex-col gap-5">
          {/* Tips */}
          <div className="glass-card p-5">
            <h3
              className="font-semibold text-sm mb-3 flex items-center gap-2"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              <TrendingUp size={14} style={{ color: "#10b981" }} />
              Tips for better results
            </h3>
            <ul className="flex flex-col gap-2">
              {[
                "Be specific about required skills",
                "Include salary range — gets 40% more applicants",
                "Mention remote options to widen the pool",
                "Add responsibilities to attract the right fit",
              ].map((tip) => (
                <li key={tip} className="flex items-start gap-2 text-xs" style={{ color: "var(--text-muted)" }}>
                  <CheckCircle size={12} className="mt-0.5 flex-shrink-0" style={{ color: "#10b981" }} />
                  {tip}
                </li>
              ))}
            </ul>
          </div>

          {/* Recent Jobs */}
          {recentJobs.length > 0 && (
            <div className="glass-card p-5">
              <h3
                className="font-semibold text-sm mb-3 flex items-center gap-2"
                style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
              >
                <Clock size={14} style={{ color: "#6366f1" }} />
                Recently Posted
              </h3>
              <div className="flex flex-col gap-3">
                {recentJobs.map((job) => (
                  <div key={job.id} className="flex flex-col gap-1">
                    <span className="text-xs font-medium line-clamp-1">{job.title}</span>
                    <div className="flex items-center gap-2 text-xs" style={{ color: "var(--text-muted)" }}>
                      {job.location && (
                        <span className="flex items-center gap-0.5">
                          <MapPin size={9} /> {job.location}
                        </span>
                      )}
                      <span
                        className={`badge ${job.is_active ? "badge-green" : "badge-red"}`}
                        style={{ padding: "1px 7px", fontSize: "10px" }}
                      >
                        {job.is_active ? "Active" : "Closed"}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* AI badge */}
          <div
            className="glass-card p-5"
            style={{
              background: "linear-gradient(135deg, rgba(99,102,241,0.1), rgba(139,92,246,0.06))",
              border: "1px solid rgba(99,102,241,0.22)",
            }}
          >
            <Sparkles size={18} className="mb-2" style={{ color: "#a5b4fc" }} />
            <div className="text-sm font-semibold mb-1">AI Auto-Match</div>
            <p className="text-xs" style={{ color: "var(--text-muted)" }}>
              After posting, our AI will automatically embed your job description and
              surface the top student candidates on the Candidates page.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
