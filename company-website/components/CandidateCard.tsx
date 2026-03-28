"use client";

import { CandidateOut } from "@/services/api";
import { User, GraduationCap, Briefcase, Brain, Star } from "lucide-react";
import clsx from "clsx";

interface Props {
  candidate: CandidateOut;
  onMatchScore?: (studentId: number, jobId: number) => void;
  jobId?: number;
}

function ScoreBar({ score }: { score: number }) {
  const pct = Math.round(score * 100);
  const color =
    pct >= 80
      ? "#10b981"
      : pct >= 60
      ? "#6366f1"
      : pct >= 40
      ? "#f59e0b"
      : "#ef4444";

  return (
    <div className="flex items-center gap-2 mt-1">
      <div
        className="flex-1 h-1.5 rounded-full overflow-hidden"
        style={{ background: "rgba(255,255,255,0.08)" }}
      >
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{ width: `${pct}%`, backgroundColor: color }}
        />
      </div>
      <span className="text-xs font-bold tabular-nums" style={{ color }}>
        {pct}%
      </span>
    </div>
  );
}

export default function CandidateCard({ candidate, onMatchScore, jobId }: Props) {
  const score = candidate.match_score ?? 0;
  const hasSScore = candidate.match_score !== undefined && candidate.match_score !== null;
  const scoreLabel =
    score >= 0.8
      ? "Excellent Match"
      : score >= 0.6
      ? "Good Match"
      : score >= 0.4
      ? "Fair Match"
      : "Low Match";

  const scoreColor = clsx(
    score >= 0.8
      ? "badge-green"
      : score >= 0.6
      ? "badge-indigo"
      : score >= 0.4
      ? "badge-amber"
      : "badge-red"
  );

  return (
    <div
      className="glass-card p-5 flex flex-col gap-4"
      id={`candidate-card-${candidate.student_id}`}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-center gap-3">
          {/* Avatar */}
          <div
            className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0"
            style={{
              background: "linear-gradient(135deg, rgba(99,102,241,0.25), rgba(139,92,246,0.25))",
              border: "1px solid rgba(99,102,241,0.25)",
            }}
          >
            <User size={20} style={{ color: "#a5b4fc" }} />
          </div>

          <div>
            <h3 className="font-semibold text-sm" style={{ color: "var(--text-primary)" }}>
              {candidate.full_name}
            </h3>
            <p className="text-xs" style={{ color: "var(--text-muted)" }}>
              {candidate.email}
            </p>
          </div>
        </div>

        {hasSScore && (
          <span className={`badge ${scoreColor} flex-shrink-0`}>
            <Star size={10} />
            {scoreLabel}
          </span>
        )}
      </div>

      {/* Details */}
      <div className="flex flex-col gap-2">
        {candidate.university && (
          <div className="flex items-center gap-2 text-xs" style={{ color: "var(--text-muted)" }}>
            <GraduationCap size={13} className="flex-shrink-0" />
            <span>
              {candidate.university}
              {candidate.degree ? ` · ${candidate.degree}` : ""}
            </span>
          </div>
        )}
        {candidate.job_title && (
          <div className="flex items-center gap-2 text-xs" style={{ color: "var(--text-muted)" }}>
            <Briefcase size={13} className="flex-shrink-0" />
            <span>Applied for: {candidate.job_title}</span>
          </div>
        )}
      </div>

      {/* AI Match Score */}
      {hasSScore && (
        <div>
          <div className="flex items-center gap-1 mb-1">
            <Brain size={11} style={{ color: "#a5b4fc" }} />
            <span className="text-xs font-medium" style={{ color: "var(--text-muted)" }}>
              AI Match Score
            </span>
          </div>
          <ScoreBar score={score} />
        </div>
      )}

      {/* Action */}
      {onMatchScore && jobId && (
        <button
          onClick={() => onMatchScore(candidate.student_id, jobId)}
          className="w-full mt-1 text-xs font-semibold py-2 px-3 rounded-lg transition-all flex items-center justify-center gap-1.5"
          style={{
            background: "rgba(99,102,241,0.12)",
            color: "#a5b4fc",
            border: "1px solid rgba(99,102,241,0.2)",
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.background = "rgba(99,102,241,0.22)")
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.background = "rgba(99,102,241,0.12)")
          }
          id={`run-match-${candidate.student_id}`}
        >
          <Brain size={13} />
          Run AI Match
        </button>
      )}
    </div>
  );
}
