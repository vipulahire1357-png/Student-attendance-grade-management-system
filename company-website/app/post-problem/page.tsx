"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { companyAPI, type ProblemCreate } from "@/services/api";
import {
  Lightbulb,
  Sparkles,
  CheckCircle,
  AlertCircle,
  Loader2,
  Trophy,
  Calendar,
  Tag,
  Plus,
  X,
  Brain,
} from "lucide-react";
import { QueryClient, useQueryClient } from "@tanstack/react-query";

const PROBLEM_TYPES = ["Algorithmic", "Design", "Business", "DataScience", "Security", "DevOps", "Fullstack", "Other"];
const DIFFICULTIES = ["Easy", "Medium", "Hard"];

export default function PostProblemPage() {
  const queryClient = useQueryClient();
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [skillInput, setSkillInput] = useState("");
  const [skills, setSkills] = useState<string[]>([]);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ProblemCreate>();

  const addSkill = () => {
    const s = skillInput.trim();
    if (s && !skills.includes(s)) {
      setSkills([...skills, s]);
    }
    setSkillInput("");
  };

  const removeSkill = (skill: string) => {
    setSkills(skills.filter((s) => s !== skill));
  };

  const onSubmit = async (data: ProblemCreate) => {
    setSubmitting(true);
    setError(null);
    try {
      await companyAPI.postProblem({ ...data, required_skills: skills });
      setSuccess(true);
      setSkills([]);
      reset();
      queryClient.invalidateQueries({ queryKey: ["all-problems"] });
      setTimeout(() => setSuccess(false), 5000);
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      setError(e?.response?.data?.detail ?? "Failed to post problem. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 pt-6 animate-fade-in">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-2">
          <div
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{
              background: "linear-gradient(135deg, #8b5cf6, #a855f7)",
              boxShadow: "0 0 16px rgba(139,92,246,0.35)",
            }}
          >
            <Lightbulb size={15} className="text-white" />
          </div>
          <h1
            className="text-2xl font-bold"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            Post an Industry Challenge
          </h1>
        </div>
        <p className="text-sm" style={{ color: "var(--text-muted)" }}>
          Share a real-world problem and let talented students compete to solve it.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-2 glass-card p-7">
          <div
            className="flex items-center gap-2 mb-6 pb-4"
            style={{ borderBottom: "1px solid rgba(139,92,246,0.12)" }}
          >
            <Sparkles size={16} style={{ color: "#8b5cf6" }} />
            <h2 className="font-semibold">Problem Details</h2>
          </div>

          {success && (
            <div className="alert alert-success mb-5 animate-fade-in">
              <CheckCircle size={15} />
              Industry challenge posted! Students will see it immediately.
            </div>
          )}
          {error && (
            <div className="alert alert-error mb-5 animate-fade-in">
              <AlertCircle size={15} />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="form-section">
            {/* Title */}
            <div>
              <label className="form-label" htmlFor="pp-title">
                <Lightbulb size={11} className="inline mr-1 mb-0.5" />
                Problem Title *
              </label>
              <input
                id="pp-title"
                className="input-glass"
                placeholder="e.g. Build a real-time fraud detection system"
                {...register("title", { required: "Title is required" })}
              />
              {errors.title && (
                <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
                  {errors.title.message}
                </p>
              )}
            </div>

            {/* Description */}
            <div>
              <label className="form-label" htmlFor="pp-desc">
                Full Description *
              </label>
              <textarea
                id="pp-desc"
                rows={5}
                className="input-glass resize-none"
                placeholder="Describe the problem context, goals, constraints, expected deliverables..."
                {...register("description", { required: "Description is required" })}
              />
              {errors.description && (
                <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
                  {errors.description.message}
                </p>
              )}
            </div>

            {/* Type + Difficulty */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="form-label" htmlFor="pp-type">
                  <Tag size={11} className="inline mr-1 mb-0.5" />
                  Problem Type
                </label>
                <select
                  id="pp-type"
                  className="input-glass"
                  {...register("problem_type")}
                  style={{ backgroundColor: "rgba(255,255,255,0.04)", cursor: "pointer" }}
                >
                  <option value="">Select type</option>
                  {PROBLEM_TYPES.map((t) => (
                    <option key={t} value={t} style={{ backgroundColor: "#0f1629" }}>
                      {t}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="form-label" htmlFor="pp-diff">Difficulty</label>
                <select
                  id="pp-diff"
                  className="input-glass"
                  {...register("difficulty")}
                  style={{ backgroundColor: "rgba(255,255,255,0.04)", cursor: "pointer" }}
                >
                  <option value="">Select difficulty</option>
                  {DIFFICULTIES.map((d) => (
                    <option key={d} value={d} style={{ backgroundColor: "#0f1629" }}>
                      {d}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Reward + Deadline */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="form-label" htmlFor="pp-reward">
                  <Trophy size={11} className="inline mr-1 mb-0.5" />
                  Reward / Prize
                </label>
                <input
                  id="pp-reward"
                  className="input-glass"
                  placeholder="e.g. $500 cash, Internship offer"
                  {...register("reward")}
                />
              </div>
              <div>
                <label className="form-label" htmlFor="pp-deadline">
                  <Calendar size={11} className="inline mr-1 mb-0.5" />
                  Submission Deadline
                </label>
                <input
                  id="pp-deadline"
                  type="date"
                  className="input-glass"
                  {...register("deadline")}
                  style={{ colorScheme: "dark" }}
                />
              </div>
            </div>

            {/* Max Submissions */}
            <div>
              <label className="form-label" htmlFor="pp-max">Max Submissions</label>
              <input
                id="pp-max"
                type="number"
                className="input-glass"
                placeholder="e.g. 100 (leave blank for unlimited)"
                {...register("max_submissions", { valueAsNumber: true })}
              />
            </div>

            {/* Required Skills */}
            <div>
              <label className="form-label">Required Skills</label>
              <div className="flex gap-2 mb-2">
                <input
                  className="input-glass flex-1"
                  placeholder="e.g. Python, Machine Learning"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      addSkill();
                    }
                  }}
                  id="pp-skill-input"
                />
                <button
                  type="button"
                  onClick={addSkill}
                  className="px-3 py-2 rounded-lg text-sm font-semibold transition-all"
                  style={{
                    background: "rgba(139,92,246,0.15)",
                    color: "#c4b5fd",
                    border: "1px solid rgba(139,92,246,0.25)",
                  }}
                  id="pp-add-skill-btn"
                >
                  <Plus size={16} />
                </button>
              </div>
              {skills.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-1">
                  {skills.map((s) => (
                    <span key={s} className="badge badge-violet flex items-center gap-1.5">
                      {s}
                      <button
                        type="button"
                        onClick={() => removeSkill(s)}
                        className="hover:text-white transition-colors"
                        aria-label={`Remove ${s}`}
                      >
                        <X size={11} />
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>

            <button
              id="pp-submit-btn"
              type="submit"
              disabled={submitting}
              className="btn-gradient flex items-center justify-center gap-2 w-full"
            >
              {submitting ? (
                <><Loader2 size={16} className="animate-spin" /> Posting Challenge...</>
              ) : (
                <><Sparkles size={16} /> Publish Industry Challenge</>
              )}
            </button>
          </form>
        </div>

        {/* Sidebar */}
        <div className="flex flex-col gap-5">
          {/* Why post */}
          <div className="glass-card p-5">
            <h3
              className="font-semibold text-sm mb-3 flex items-center gap-2"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              <Brain size={14} style={{ color: "#8b5cf6" }} />
              Why post a challenge?
            </h3>
            <ul className="flex flex-col gap-2.5">
              {[
                "Identify problem-solvers, not resume fillers",
                "Get real working prototypes for your problem",
                "Build brand recognition among top students",
                "Fast-track promising candidates to interviews",
              ].map((tip) => (
                <li
                  key={tip}
                  className="flex items-start gap-2 text-xs"
                  style={{ color: "var(--text-muted)" }}
                >
                  <CheckCircle
                    size={12}
                    className="mt-0.5 flex-shrink-0"
                    style={{ color: "#8b5cf6" }}
                  />
                  {tip}
                </li>
              ))}
            </ul>
          </div>

          {/* How it works */}
          <div className="glass-card p-5">
            <h3
              className="font-semibold text-sm mb-3"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              How it works
            </h3>
            <ol className="flex flex-col gap-3">
              {[
                "You post the problem with details and requirements",
                "Students submit solutions within the deadline",
                "You review all submissions in the Candidates page",
                "Hire the best solver directly!",
              ].map((step, i) => (
                <li
                  key={step}
                  className="flex items-start gap-3 text-xs"
                  style={{ color: "var(--text-muted)" }}
                >
                  <span
                    className="w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 text-xs font-bold"
                    style={{
                      background: "rgba(139,92,246,0.2)",
                      color: "#c4b5fd",
                      border: "1px solid rgba(139,92,246,0.3)",
                    }}
                  >
                    {i + 1}
                  </span>
                  {step}
                </li>
              ))}
            </ol>
          </div>

          {/* Stat */}
          <div
            className="glass-card p-5 text-center"
            style={{
              background: "linear-gradient(135deg, rgba(139,92,246,0.1), rgba(168,85,247,0.06))",
              border: "1px solid rgba(139,92,246,0.22)",
            }}
          >
            <div
              className="text-3xl font-extrabold gradient-text mb-1"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              120+
            </div>
            <div className="text-xs" style={{ color: "var(--text-muted)" }}>
              Average submissions per challenge on our platform
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
