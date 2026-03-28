"use client";

import { useQuery } from "@tanstack/react-query";
import { companyAPI, jobsAPI, problemsAPI, type CompanyProfile, type JobOut, type ProblemOut } from "@/services/api";
import {
  Briefcase,
  Lightbulb,
  Users,
  TrendingUp,
  Plus,
  ArrowRight,
  Building2,
  CheckCircle,
  Clock,
  Loader2,
  AlertCircle,
  Zap,
  BarChart3,
} from "lucide-react";
import Link from "next/link";

// ── Stat card ─────────────────────────────────────────────────────────────────
function StatCard({
  label,
  value,
  icon: Icon,
  iconColor,
  sub,
}: {
  label: string;
  value: string | number;
  icon: React.ElementType;
  iconColor: string;
  sub?: string;
}) {
  return (
    <div className="stat-card flex items-start gap-4">
      <div
        className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
        style={{ background: `${iconColor}1a`, border: `1px solid ${iconColor}30` }}
      >
        <Icon size={18} style={{ color: iconColor }} />
      </div>
      <div>
        <div
          className="text-2xl font-bold mb-0.5"
          style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
        >
          {value}
        </div>
        <div className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
          {label}
        </div>
        {sub && (
          <div className="text-xs mt-0.5" style={{ color: "var(--text-muted)", opacity: 0.7 }}>
            {sub}
          </div>
        )}
      </div>
    </div>
  );
}

// ── Quick action card ─────────────────────────────────────────────────────────
function QuickAction({
  href,
  icon: Icon,
  title,
  desc,
  color,
  id,
}: {
  href: string;
  icon: React.ElementType;
  title: string;
  desc: string;
  color: string;
  id: string;
}) {
  return (
    <Link
      href={href}
      id={id}
      className="glass-card p-5 flex items-center gap-4 group no-underline"
      style={{ transition: "transform 0.2s ease" }}
      onMouseEnter={(e) =>
        ((e.currentTarget as HTMLElement).style.transform = "translateY(-3px)")
      }
      onMouseLeave={(e) =>
        ((e.currentTarget as HTMLElement).style.transform = "none")
      }
    >
      <div
        className="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
        style={{ background: `${color}1a`, border: `1px solid ${color}35` }}
      >
        <Icon size={18} style={{ color }} />
      </div>
      <div className="flex-1">
        <div className="text-sm font-semibold">{title}</div>
        <div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>
          {desc}
        </div>
      </div>
      <ArrowRight
        size={16}
        style={{ color: "var(--text-muted)" }}
        className="group-hover:translate-x-1 transition-transform"
      />
    </Link>
  );
}

// ── Recent Job row ────────────────────────────────────────────────────────────
function JobRow({ job }: { job: JobOut }) {
  return (
    <div
      className="flex items-center justify-between py-3 px-1"
      style={{ borderBottom: "1px solid rgba(99,102,241,0.08)" }}
    >
      <div>
        <div className="text-sm font-medium">{job.title}</div>
        <div className="text-xs mt-0.5" style={{ color: "var(--text-muted)" }}>
          {job.job_type ?? "N/A"} · {job.location ?? "Remote"}
        </div>
      </div>
      <div className="flex items-center gap-2">
        {job.is_active ? (
          <span className="badge badge-green">
            <CheckCircle size={10} /> Active
          </span>
        ) : (
          <span className="badge badge-red">Closed</span>
        )}
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const {
    data: profile,
    isLoading: profileLoading,
    error: profileError,
  } = useQuery<CompanyProfile>({
    queryKey: ["company-profile"],
    queryFn: async () => (await companyAPI.getProfile()).data,
  });

  const { data: jobs, isLoading: jobsLoading } = useQuery<JobOut[]>({
    queryKey: ["all-jobs"],
    queryFn: async () => (await jobsAPI.listJobs({ limit: 100 })).data,
  });

  const { data: problems, isLoading: problemsLoading } = useQuery<ProblemOut[]>({
    queryKey: ["all-problems"],
    queryFn: async () => (await problemsAPI.listProblems()).data,
  });

  const { data: candidatesData } = useQuery({
    queryKey: ["candidates"],
    queryFn: async () => (await companyAPI.getCandidates({})).data,
  });

  if (profileLoading) {
    return (
      <div className="flex items-center justify-center py-32">
        <div className="flex items-center gap-3" style={{ color: "var(--text-muted)" }}>
          <Loader2 size={20} className="animate-spin" />
          Loading dashboard...
        </div>
      </div>
    );
  }

  if (profileError) {
    return (
      <div className="flex flex-col items-center justify-center py-32 gap-4">
        <AlertCircle size={32} style={{ color: "#ef4444" }} />
        <p style={{ color: "var(--text-muted)" }}>
          Failed to load company data. Please try refreshing.
        </p>
      </div>
    );
  }

  const activeJobs =
    jobs?.filter((j) => j.is_active) ?? [];
  const companyJobs =
    jobs?.filter((j) => j.company_id === profile?.id) ?? [];
  const companyProblems =
    problems?.filter((p) => p.company_id === profile?.id) ?? [];

  return (
    <div className="space-y-8 pt-4 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                boxShadow: "0 0 16px rgba(99,102,241,0.35)",
              }}
            >
              <Building2 size={15} className="text-white" />
            </div>
            <h1
              className="text-xl font-bold"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              {profile?.company_name ?? "Your Company"}
            </h1>
            {profile?.is_verified && (
              <span className="badge badge-green text-xs">
                <CheckCircle size={10} /> Verified
              </span>
            )}
          </div>
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>
            {profile?.industry ?? "Company"} ·{" "}
            {new Date().toLocaleDateString("en-US", {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
            })}
          </p>
        </div>

        <Link
          href="/post-job"
          id="dashboard-post-job-btn"
          className="btn-gradient flex items-center gap-2 text-sm self-start sm:self-auto"
        >
          <Plus size={15} /> Post a Job
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          label="Active Jobs"
          value={jobsLoading ? "—" : companyJobs.filter((j) => j.is_active).length}
          icon={Briefcase}
          iconColor="#6366f1"
          sub={`${companyJobs.length} total posted`}
        />
        <StatCard
          label="Problems Posted"
          value={problemsLoading ? "—" : companyProblems.length}
          icon={Lightbulb}
          iconColor="#8b5cf6"
          sub={`${companyProblems.filter((p) => p.is_active).length} active`}
        />
        <StatCard
          label="Candidates"
          value={candidatesData?.total ?? "—"}
          icon={Users}
          iconColor="#06b6d4"
          sub="Applied to your jobs"
        />
        <StatCard
          label="Platform Jobs"
          value={activeJobs.length}
          icon={TrendingUp}
          iconColor="#10b981"
          sub="Total active listings"
        />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Jobs — 2 cols */}
        <div className="lg:col-span-2 glass-card p-6">
          <div className="flex items-center justify-between mb-4">
            <h2
              className="font-semibold flex items-center gap-2"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              <Briefcase size={16} style={{ color: "#6366f1" }} />
              Your Job Listings
            </h2>
            <Link
              href="/post-job"
              className="text-xs font-semibold flex items-center gap-1"
              style={{ color: "#a5b4fc" }}
            >
              <Plus size={12} /> New Job
            </Link>
          </div>

          {jobsLoading ? (
            <div className="flex items-center gap-2 py-6" style={{ color: "var(--text-muted)" }}>
              <Loader2 size={15} className="animate-spin" /> Loading...
            </div>
          ) : companyJobs.length === 0 ? (
            <div className="text-center py-10">
              <Briefcase size={32} className="mx-auto mb-3 opacity-30" />
              <p className="text-sm" style={{ color: "var(--text-muted)" }}>
                No jobs posted yet
              </p>
              <Link
                href="/post-job"
                className="inline-flex items-center gap-1.5 mt-3 text-xs font-semibold"
                style={{ color: "#a5b4fc" }}
              >
                Post your first job <ArrowRight size={12} />
              </Link>
            </div>
          ) : (
            <div>
              {companyJobs.slice(0, 6).map((job) => (
                <JobRow key={job.id} job={job} />
              ))}
              {companyJobs.length > 6 && (
                <p
                  className="text-xs text-center mt-3"
                  style={{ color: "var(--text-muted)" }}
                >
                  +{companyJobs.length - 6} more jobs
                </p>
              )}
            </div>
          )}
        </div>

        {/* Quick Actions — 1 col */}
        <div className="flex flex-col gap-4">
          <h2
            className="font-semibold flex items-center gap-2 px-1"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            <Zap size={16} style={{ color: "#f59e0b" }} />
            Quick Actions
          </h2>
          <QuickAction
            href="/post-job"
            icon={Briefcase}
            title="Post New Job"
            desc="Create a new job listing"
            color="#6366f1"
            id="qa-post-job"
          />
          <QuickAction
            href="/post-problem"
            icon={Lightbulb}
            title="Post Industry Problem"
            desc="Challenge students to solve it"
            color="#8b5cf6"
            id="qa-post-problem"
          />
          <QuickAction
            href="/candidates"
            icon={Users}
            title="View Candidates"
            desc="Browse applicants & AI scores"
            color="#06b6d4"
            id="qa-candidates"
          />

          {/* AI Highlight */}
          <div
            className="glass-card p-5 relative overflow-hidden"
            style={{
              background:
                "linear-gradient(135deg, rgba(99,102,241,0.12), rgba(139,92,246,0.08))",
              border: "1px solid rgba(99,102,241,0.25)",
            }}
          >
            <div
              className="glow-orb w-24 h-24 opacity-30"
              style={{
                background: "rgba(99,102,241,1)",
                top: "-20px",
                right: "-20px",
              }}
            />
            <BarChart3
              size={20}
              className="mb-3 relative z-10"
              style={{ color: "#a5b4fc" }}
            />
            <div
              className="text-sm font-semibold mb-1 relative z-10"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              AI Match Engine
            </div>
            <p
              className="text-xs leading-relaxed relative z-10"
              style={{ color: "var(--text-muted)" }}
            >
              Our AI engine automatically ranks candidates by skill-match. Head to
              Candidates to see match scores.
            </p>
            <Link
              href="/candidates"
              className="inline-flex items-center gap-1 mt-3 text-xs font-semibold relative z-10"
              style={{ color: "#a5b4fc" }}
              id="ai-match-link"
            >
              View Candidates <ArrowRight size={12} />
            </Link>
          </div>
        </div>
      </div>

      {/* Problems Section */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h2
            className="font-semibold flex items-center gap-2"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            <Lightbulb size={16} style={{ color: "#8b5cf6" }} />
            Your Industry Challenges
          </h2>
          <Link
            href="/post-problem"
            className="text-xs font-semibold flex items-center gap-1"
            style={{ color: "#c4b5fd" }}
          >
            <Plus size={12} /> New Problem
          </Link>
        </div>

        {problemsLoading ? (
          <div className="flex items-center gap-2 py-4" style={{ color: "var(--text-muted)" }}>
            <Loader2 size={14} className="animate-spin" /> Loading...
          </div>
        ) : companyProblems.length === 0 ? (
          <div className="text-center py-8">
            <Lightbulb size={28} className="mx-auto mb-3 opacity-30" />
            <p className="text-sm" style={{ color: "var(--text-muted)" }}>
              No industry challenges posted yet
            </p>
            <Link
              href="/post-problem"
              className="inline-flex items-center gap-1.5 mt-3 text-xs font-semibold"
              style={{ color: "#c4b5fd" }}
            >
              Post a challenge <ArrowRight size={12} />
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {companyProblems.slice(0, 6).map((p) => (
              <div key={p.id} className="stat-card">
                <div className="flex items-start justify-between gap-2 mb-2">
                  <h3 className="text-sm font-semibold line-clamp-1">{p.title}</h3>
                  <span
                    className={`badge flex-shrink-0 ${
                      p.difficulty === "Hard"
                        ? "badge-red"
                        : p.difficulty === "Medium"
                        ? "badge-amber"
                        : "badge-green"
                    }`}
                  >
                    {p.difficulty ?? "Any"}
                  </span>
                </div>
                <p
                  className="text-xs line-clamp-2 mb-3"
                  style={{ color: "var(--text-muted)" }}
                >
                  {p.description}
                </p>
                <div className="flex items-center gap-3 text-xs" style={{ color: "var(--text-muted)" }}>
                  {p.reward && (
                    <span className="badge badge-cyan">💰 {p.reward}</span>
                  )}
                  {p.problem_type && (
                    <span className="flex items-center gap-1">
                      <Clock size={10} /> {p.problem_type}
                    </span>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
