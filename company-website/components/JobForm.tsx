"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { companyAPI, JobCreate } from "@/services/api";
import { Briefcase, MapPin, DollarSign, Clock, CheckCircle, AlertCircle, Loader2, Sparkles } from "lucide-react";

interface Props {
  onSuccess?: () => void;
}

const JOB_TYPES = [
  { label: "Full-time", value: "full-time" },
  { label: "Part-time", value: "part-time" },
  { label: "Contract", value: "contract" },
  { label: "Internship", value: "internship" },
  { label: "Remote", value: "remote" },
];

const EXP_LEVELS = [
  { label: "Entry", value: "entry" },
  { label: "Mid", value: "mid" },
  { label: "Senior", value: "senior" },
  { label: "Lead", value: "lead" },
];

export default function JobForm({ onSuccess }: Props) {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<JobCreate>({
    defaultValues: {
      remote_allowed: false,
      currency: "USD",
    },
  });

  const onSubmit = async (data: JobCreate) => {
    setSubmitting(true);
    setError(null);
    try {
      await companyAPI.postJob(data);
      setSuccess(true);
      reset();
      onSuccess?.();
      setTimeout(() => setSuccess(false), 4000);
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: unknown } } };
      const detail = e?.response?.data?.detail;
      if (Array.isArray(detail)) {
        setError(detail.map((d: { msg?: string }) => d.msg ?? String(d)).join(", "));
      } else if (typeof detail === "string") {
        setError(detail);
      } else {
        setError("Failed to post job. Please try again.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="form-section">
      {/* Success */}
      {success && (
        <div className="alert alert-success animate-fade-in">
          <CheckCircle size={16} />
          Job posted successfully! Students will be notified.
        </div>
      )}
      {error && (
        <div className="alert alert-error animate-fade-in">
          <AlertCircle size={16} />
          {error}
        </div>
      )}

      {/* Title */}
      <div>
        <label className="form-label" htmlFor="jf-title">
          <Briefcase size={12} className="inline mr-1 mb-0.5" />
          Job Title *
        </label>
        <input
          id="jf-title"
          className="input-glass"
          placeholder="e.g. Junior React Developer"
          {...register("title", { required: "Job title is required" })}
        />
        {errors.title && (
          <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
            {errors.title.message}
          </p>
        )}
      </div>

      {/* Description */}
      <div>
        <label className="form-label" htmlFor="jf-desc">
          Description *
        </label>
        <textarea
          id="jf-desc"
          rows={4}
          className="input-glass resize-none"
          placeholder="Describe the role, what you're building, culture..."
          {...register("description", { required: "Description is required" })}
        />
        {errors.description && (
          <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
            {errors.description.message}
          </p>
        )}
      </div>

      {/* Requirements & Responsibilities */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="form-label" htmlFor="jf-req">Requirements</label>
          <textarea
            id="jf-req"
            rows={3}
            className="input-glass resize-none"
            placeholder="Required skills, experience..."
            {...register("requirements")}
          />
        </div>
        <div>
          <label className="form-label" htmlFor="jf-resp">Responsibilities</label>
          <textarea
            id="jf-resp"
            rows={3}
            className="input-glass resize-none"
            placeholder="Day-to-day tasks..."
            {...register("responsibilities")}
          />
        </div>
      </div>

      {/* Row: Job Type + Experience Level */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="form-label" htmlFor="jf-type">
            <Clock size={12} className="inline mr-1 mb-0.5" />
            Job Type
          </label>
          <select
            id="jf-type"
            className="input-glass"
            {...register("job_type")}
            style={{ backgroundColor: "rgba(255,255,255,0.04)", cursor: "pointer" }}
          >
            <option value="">Select type</option>
            {JOB_TYPES.map((t) => (
              <option key={t.value} value={t.value} style={{ backgroundColor: "#0f1629" }}>
                {t.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <label className="form-label" htmlFor="jf-exp">Experience Level</label>
          <select
            id="jf-exp"
            className="input-glass"
            {...register("experience_level")}
            style={{ backgroundColor: "rgba(255,255,255,0.04)", cursor: "pointer" }}
          >
            <option value="">Select level</option>
            {EXP_LEVELS.map((l) => (
              <option key={l.value} value={l.value} style={{ backgroundColor: "#0f1629" }}>
                {l.label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Location + Remote */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="form-label" htmlFor="jf-loc">
            <MapPin size={12} className="inline mr-1 mb-0.5" />
            Location
          </label>
          <input
            id="jf-loc"
            className="input-glass"
            placeholder="e.g. San Francisco, CA"
            {...register("location")}
          />
        </div>
        <div className="flex items-end pb-1">
          <label
            className="flex items-center gap-3 cursor-pointer"
            htmlFor="jf-remote"
          >
            <input
              id="jf-remote"
              type="checkbox"
              {...register("remote_allowed")}
              className="w-4 h-4 accent-indigo-500 rounded"
            />
            <span className="text-sm font-medium" style={{ color: "var(--text-muted)" }}>
              Remote Allowed
            </span>
          </label>
        </div>
      </div>

      {/* Salary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label className="form-label" htmlFor="jf-smin">
            <DollarSign size={12} className="inline mr-1 mb-0.5" />
            Salary Min
          </label>
          <input
            id="jf-smin"
            type="number"
            className="input-glass"
            placeholder="e.g. 50000"
            {...register("salary_min", { valueAsNumber: true })}
          />
        </div>
        <div>
          <label className="form-label" htmlFor="jf-smax">Salary Max</label>
          <input
            id="jf-smax"
            type="number"
            className="input-glass"
            placeholder="e.g. 80000"
            {...register("salary_max", { valueAsNumber: true })}
          />
        </div>
        <div>
          <label className="form-label" htmlFor="jf-curr">Currency</label>
          <select
            id="jf-curr"
            className="input-glass"
            {...register("currency")}
            style={{ backgroundColor: "rgba(255,255,255,0.04)", cursor: "pointer" }}
          >
            {["USD", "EUR", "GBP", "INR", "CAD"].map((c) => (
              <option key={c} value={c} style={{ backgroundColor: "#0f1629" }}>
                {c}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Expires At */}
      <div>
        <label className="form-label" htmlFor="jf-exp-date">Application Deadline</label>
        <input
          id="jf-exp-date"
          type="date"
          className="input-glass"
          {...register("expires_at")}
          style={{ colorScheme: "dark" }}
        />
      </div>

      {/* Submit */}
      <button
        type="submit"
        disabled={submitting}
        className="btn-gradient flex items-center justify-center gap-2 w-full"
        id="job-submit-btn"
      >
        {submitting ? (
          <><Loader2 size={16} className="animate-spin" /> Posting Job...</>
        ) : (
          <><Sparkles size={16} /> Post Job Listing</>
        )}
      </button>
    </form>
  );
}