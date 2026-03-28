"use client";

import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { companyAPI, jobsAPI, aiAPI, type CandidateOut, type JobOut } from "@/services/api";
import CandidateCard from "@/components/CandidateCard";
import {
  Users,
  Search,
  Brain,
  Filter,
  Loader2,
  AlertCircle,
  RefreshCcw,
  ChevronDown,
  Sparkles,
  ArrowUpDown,
} from "lucide-react";

type SortBy = "name" | "score_desc" | "score_asc";

export default function CandidatesPage() {
  const [jobFilter, setJobFilter] = useState<number | "all">("all");
  const [search, setSearch] = useState("");
  const [sortBy, setSortBy] = useState<SortBy>("score_desc");
  const [matchResults, setMatchResults] = useState<Record<string, number>>({});
  const [matchingId, setMatchingId] = useState<string | null>(null);

  // Fetch candidates
  const {
    data: candidatesData,
    isLoading: candidatesLoading,
    error: candidatesError,
    refetch,
  } = useQuery({
    queryKey: ["candidates", jobFilter],
    queryFn: async () => {
      const params =
        jobFilter !== "all" ? { job_id: jobFilter as number } : {};
      const res = await companyAPI.getCandidates(params);
      return res.data as { company_id: number; total: number; candidates: CandidateOut[] };
    },
  });

  // Fetch company's jobs for filter dropdown
  const { data: jobs } = useQuery<JobOut[]>({
    queryKey: ["all-jobs"],
    queryFn: async () => (await jobsAPI.listJobs({ limit: 100 })).data,
  });

  // AI match mutation
  const matchMutation = useMutation({
    mutationFn: ({ studentId, jobId }: { studentId: number; jobId: number }) =>
      aiAPI.matchStudentJob({ student_id: studentId, job_id: jobId }),
    onSuccess: (data, variables) => {
      const key = `${variables.studentId}-${variables.jobId}`;
      setMatchResults((prev) => ({ ...prev, [key]: data.data.score }));
    },
  });

  const handleMatchScore = async (studentId: number, jobId: number) => {
    const key = `${studentId}-${jobId}`;
    setMatchingId(key);
    try {
      await matchMutation.mutateAsync({ studentId, jobId });
    } finally {
      setMatchingId(null);
    }
  };

  // Enrich candidates with match results
  const candidates: CandidateOut[] = (candidatesData?.candidates ?? []).map((c) => {
    const key = `${c.student_id}-${jobFilter}`;
    const freshScore = matchResults[key];
    return freshScore !== undefined
      ? { ...c, match_score: freshScore }
      : c;
  });

  // Filter by search
  const filtered = candidates.filter((c) => {
    const q = search.toLowerCase();
    return (
      c.full_name.toLowerCase().includes(q) ||
      c.email.toLowerCase().includes(q) ||
      (c.university ?? "").toLowerCase().includes(q) ||
      (c.degree ?? "").toLowerCase().includes(q)
    );
  });

  // Sort
  const sorted = [...filtered].sort((a, b) => {
    if (sortBy === "name") return a.full_name.localeCompare(b.full_name);
    if (sortBy === "score_desc")
      return (b.match_score ?? 0) - (a.match_score ?? 0);
    if (sortBy === "score_asc")
      return (a.match_score ?? 0) - (b.match_score ?? 0);
    return 0;
  });

  // Stats
  const withScores = candidates.filter((c) => c.match_score !== undefined && c.match_score !== null);
  const avgScore =
    withScores.length > 0
      ? Math.round(
          (withScores.reduce((sum, c) => sum + (c.match_score ?? 0), 0) /
            withScores.length) *
            100
        )
      : null;
  const topMatches = candidates.filter((c) => (c.match_score ?? 0) >= 0.8).length;

  return (
    <div className="space-y-6 pt-4 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{
                background: "linear-gradient(135deg, #06b6d4, #6366f1)",
                boxShadow: "0 0 16px rgba(6,182,212,0.3)",
              }}
            >
              <Users size={15} className="text-white" />
            </div>
            <h1
              className="text-2xl font-bold"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              Candidates
            </h1>
          </div>
          <p className="text-sm" style={{ color: "var(--text-muted)" }}>
            {candidatesData?.total ?? 0} total candidates · Run AI match for live scoring
          </p>
        </div>

        <button
          onClick={() => refetch()}
          id="candidates-refresh-btn"
          className="flex items-center gap-2 text-sm px-4 py-2 rounded-lg transition-all self-start sm:self-auto"
          style={{
            background: "rgba(99,102,241,0.1)",
            color: "#a5b4fc",
            border: "1px solid rgba(99,102,241,0.2)",
          }}
        >
          <RefreshCcw size={14} /> Refresh
        </button>
      </div>

      {/* Stats strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          {
            label: "Total Candidates",
            value: candidatesData?.total ?? "—",
            icon: Users,
            color: "#06b6d4",
          },
          {
            label: "With AI Score",
            value: withScores.length,
            icon: Brain,
            color: "#6366f1",
          },
          {
            label: "Avg Match Score",
            value: avgScore !== null ? `${avgScore}%` : "—",
            icon: Sparkles,
            color: "#8b5cf6",
          },
          {
            label: "Top Matches (≥80%)",
            value: topMatches,
            icon: ArrowUpDown,
            color: "#10b981",
          },
        ].map(({ label, value, icon: Icon, color }) => (
          <div key={label} className="stat-card flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0"
              style={{ background: `${color}1a`, border: `1px solid ${color}30` }}
            >
              <Icon size={16} style={{ color }} />
            </div>
            <div>
              <div
                className="text-xl font-bold"
                style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
              >
                {value}
              </div>
              <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                {label}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="glass-card p-4 flex flex-col md:flex-row gap-3">
        {/* Search */}
        <div className="relative flex-1">
          <Search
            size={15}
            className="absolute left-3 top-1/2 -translate-y-1/2"
            style={{ color: "var(--text-muted)" }}
          />
          <input
            className="input-glass pl-9"
            placeholder="Search by name, email, university..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            id="candidates-search"
          />
        </div>

        {/* Job filter */}
        <div className="relative min-w-48">
          <Filter
            size={14}
            className="absolute left-3 top-1/2 -translate-y-1/2"
            style={{ color: "var(--text-muted)" }}
          />
          <select
            className="input-glass pl-9 appearance-none cursor-pointer"
            value={jobFilter}
            onChange={(e) =>
              setJobFilter(
                e.target.value === "all" ? "all" : Number(e.target.value)
              )
            }
            id="candidates-job-filter"
            style={{ backgroundColor: "rgba(255,255,255,0.04)" }}
          >
            <option value="all" style={{ backgroundColor: "#0f1629" }}>
              All Jobs
            </option>
            {jobs?.map((j) => (
              <option key={j.id} value={j.id} style={{ backgroundColor: "#0f1629" }}>
                {j.title}
              </option>
            ))}
          </select>
          <ChevronDown
            size={14}
            className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: "var(--text-muted)" }}
          />
        </div>

        {/* Sort */}
        <div className="relative min-w-44">
          <ArrowUpDown
            size={14}
            className="absolute left-3 top-1/2 -translate-y-1/2"
            style={{ color: "var(--text-muted)" }}
          />
          <select
            className="input-glass pl-9 appearance-none cursor-pointer"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortBy)}
            id="candidates-sort"
            style={{ backgroundColor: "rgba(255,255,255,0.04)" }}
          >
            <option value="score_desc" style={{ backgroundColor: "#0f1629" }}>
              Score: High → Low
            </option>
            <option value="score_asc" style={{ backgroundColor: "#0f1629" }}>
              Score: Low → High
            </option>
            <option value="name" style={{ backgroundColor: "#0f1629" }}>
              Name A → Z
            </option>
          </select>
          <ChevronDown
            size={14}
            className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none"
            style={{ color: "var(--text-muted)" }}
          />
        </div>
      </div>

      {/* AI Match info banner */}
      {jobFilter !== "all" && (
        <div
          className="glass-card px-5 py-4 flex items-center gap-3"
          style={{
            background: "linear-gradient(135deg, rgba(99,102,241,0.1), rgba(6,182,212,0.06))",
            border: "1px solid rgba(99,102,241,0.2)",
          }}
        >
          <Brain size={18} style={{ color: "#a5b4fc" }} />
          <div className="flex-1">
            <div className="text-sm font-semibold">AI Match Mode Active</div>
            <div className="text-xs" style={{ color: "var(--text-muted)" }}>
              Click &quot;Run AI Match&quot; on any candidate card to compute their
              semantic similarity score for the selected job.
            </div>
          </div>
          {matchMutation.isPending && (
            <div className="flex items-center gap-2 text-xs" style={{ color: "#a5b4fc" }}>
              <Loader2 size={13} className="animate-spin" />
              Computing...
            </div>
          )}
        </div>
      )}

      {/* Content */}
      {candidatesLoading ? (
        <div className="flex items-center justify-center py-24">
          <div className="flex items-center gap-3" style={{ color: "var(--text-muted)" }}>
            <Loader2 size={20} className="animate-spin" />
            Loading candidates...
          </div>
        </div>
      ) : candidatesError ? (
        <div className="flex flex-col items-center justify-center py-24 gap-4">
          <AlertCircle size={32} style={{ color: "#ef4444" }} />
          <div className="text-center">
            <p className="font-medium">Failed to load candidates</p>
            <p className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>
              {(candidatesError as Error).message}
            </p>
          </div>
          <button
            onClick={() => refetch()}
            className="btn-gradient text-sm px-5 py-2"
          >
            Try Again
          </button>
        </div>
      ) : sorted.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 gap-4">
          <Users size={40} className="opacity-20" />
          <div className="text-center">
            <p
              className="font-semibold"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              {search ? "No candidates match your search" : "No candidates yet"}
            </p>
            <p className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>
              {search
                ? "Try a different search term"
                : "Candidates will appear here once students apply to your jobs"}
            </p>
          </div>
        </div>
      ) : (
        <>
          {/* Results count */}
          <div className="flex items-center justify-between">
            <p className="text-sm" style={{ color: "var(--text-muted)" }}>
              Showing{" "}
              <span style={{ color: "var(--text-primary)", fontWeight: 600 }}>
                {sorted.length}
              </span>{" "}
              candidate{sorted.length !== 1 ? "s" : ""}
              {search && ` matching "${search}"`}
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {sorted.map((candidate) => (
              <CandidateCard
                key={candidate.student_id}
                candidate={candidate}
                jobId={jobFilter !== "all" ? (jobFilter as number) : undefined}
                onMatchScore={
                  jobFilter !== "all"
                    ? (sid, jid) => handleMatchScore(sid, jid)
                    : undefined
                }
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
