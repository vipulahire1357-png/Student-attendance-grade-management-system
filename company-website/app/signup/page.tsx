"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { authAPI, authStorage, CompanySignup } from "@/services/api";
import {
  Zap,
  Mail,
  Lock,
  Building2,
  Globe,
  Briefcase,
  Loader2,
  AlertCircle,
  CheckCircle,
  Eye,
  EyeOff,
  ArrowLeft,
  ArrowRight,
} from "lucide-react";

const INDUSTRIES = [
  "Technology",
  "Finance",
  "Healthcare",
  "Education",
  "E-Commerce",
  "Consulting",
  "Media",
  "Manufacturing",
  "Energy",
  "Other",
];

export default function SignupPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPw, setShowPw] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<CompanySignup>();

  const onSubmit = async (data: CompanySignup) => {
    setLoading(true);
    setError(null);
    try {
      const res = await authAPI.signup(data);
      authStorage.save(res.data.access_token, res.data.refresh_token, res.data.role);
      router.push("/dashboard");
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      setError(e?.response?.data?.detail ?? "Failed to create account. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const perks = [
    "Post unlimited job listings",
    "Share real industry problems",
    "AI-powered candidate matching",
    "View student portfolios & projects",
  ];

  return (
    <div
      className="min-h-screen flex items-center justify-center px-4 py-16 relative overflow-hidden"
      style={{ background: "var(--bg-primary)" }}
    >
      {/* Orbs */}
      <div
        className="glow-orb w-96 h-96 opacity-15"
        style={{ background: "rgba(99,102,241,1)", top: "-100px", right: "-100px" }}
      />
      <div
        className="glow-orb w-64 h-64 opacity-10"
        style={{ background: "rgba(139,92,246,1)", bottom: "-60px", left: "-60px" }}
      />

      <div className="w-full max-w-5xl relative z-10 animate-slide-up grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
        {/* Left — feature panel */}
        <div className="hidden lg:flex flex-col gap-8 pt-4">
          <Link
            href="/"
            className="flex items-center gap-1.5 text-sm w-fit transition-colors"
            style={{ color: "var(--text-muted)" }}
          >
            <ArrowLeft size={14} />
            Back to home
          </Link>

          <div>
            <div
              className="w-12 h-12 rounded-2xl flex items-center justify-center mb-5"
              style={{
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                boxShadow: "0 0 30px rgba(99,102,241,0.35)",
              }}
            >
              <Zap size={22} className="text-white" />
            </div>
            <h1
              className="text-3xl font-bold mb-3"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              Start hiring smarter
              <br />
              <span className="gradient-text">with AI</span>
            </h1>
            <p className="text-sm leading-relaxed mb-6" style={{ color: "var(--text-muted)" }}>
              Join thousands of companies discovering exceptional student talent
              through AI-powered semantic matching.
            </p>
            <div className="flex flex-col gap-3">
              {perks.map((p) => (
                <div key={p} className="flex items-center gap-3 text-sm">
                  <CheckCircle size={16} style={{ color: "#10b981", flexShrink: 0 }} />
                  <span style={{ color: "var(--text-muted)" }}>{p}</span>
                </div>
              ))}
            </div>
          </div>

          <div
            className="glass-card p-5 italic text-sm"
            style={{ color: "var(--text-muted)" }}
          >
            &ldquo;We found our best intern ever through OnlyStudents. The AI match score
            was 94% — and it showed. Worth every minute.&rdquo;
            <div className="mt-2 font-semibold not-italic" style={{ color: "var(--text-primary)" }}>
              Priya Nair · VP Engineering, Razorpay
            </div>
          </div>
        </div>

        {/* Right — form */}
        <div>
          {/* Mobile back */}
          <Link
            href="/"
            className="flex lg:hidden items-center gap-1.5 text-sm mb-6"
            style={{ color: "var(--text-muted)" }}
          >
            <ArrowLeft size={14} />
            Back
          </Link>

          <div className="glass-card p-7">
            <h2
              className="text-xl font-bold mb-1"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              Create your company account
            </h2>
            <p className="text-sm mb-6" style={{ color: "var(--text-muted)" }}>
              Free to start · No credit card required
            </p>

            {error && (
              <div className="alert alert-error mb-5 animate-fade-in">
                <AlertCircle size={15} />
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit(onSubmit)} className="form-section">
              {/* Company Name */}
              <div>
                <label className="form-label" htmlFor="su-name">
                  <Building2 size={11} className="inline mr-1 mb-0.5" />
                  Company Name *
                </label>
                <input
                  id="su-name"
                  className="input-glass"
                  placeholder="Acme Corp"
                  {...register("company_name", { required: "Company name is required" })}
                />
                {errors.company_name && (
                  <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
                    {errors.company_name.message}
                  </p>
                )}
              </div>

              {/* Email */}
              <div>
                <label className="form-label" htmlFor="su-email">
                  <Mail size={11} className="inline mr-1 mb-0.5" />
                  Work Email *
                </label>
                <input
                  id="su-email"
                  type="email"
                  className="input-glass"
                  placeholder="you@company.com"
                  autoComplete="email"
                  {...register("email", { required: "Email is required" })}
                />
                {errors.email && (
                  <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
                    {errors.email.message}
                  </p>
                )}
              </div>

              {/* Password */}
              <div>
                <label className="form-label" htmlFor="su-password">
                  <Lock size={11} className="inline mr-1 mb-0.5" />
                  Password *
                </label>
                <div className="relative">
                  <input
                    id="su-password"
                    type={showPw ? "text" : "password"}
                    className="input-glass pr-10"
                    placeholder="Min. 8 characters"
                    autoComplete="new-password"
                    {...register("password", {
                      required: "Password is required",
                      minLength: { value: 8, message: "Must be at least 8 characters" },
                    })}
                  />
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2"
                    style={{ color: "var(--text-muted)" }}
                    onClick={() => setShowPw(!showPw)}
                    aria-label={showPw ? "Hide password" : "Show password"}
                  >
                    {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                  </button>
                </div>
                {errors.password && (
                  <p className="text-xs mt-1" style={{ color: "var(--danger)" }}>
                    {errors.password.message}
                  </p>
                )}
              </div>

              {/* Industry + Website */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="form-label" htmlFor="su-industry">
                    <Briefcase size={11} className="inline mr-1 mb-0.5" />
                    Industry
                  </label>
                  <select
                    id="su-industry"
                    className="input-glass"
                    {...register("industry")}
                    style={{ backgroundColor: "rgba(255,255,255,0.04)", cursor: "pointer" }}
                  >
                    <option value="">Select industry</option>
                    {INDUSTRIES.map((i) => (
                      <option key={i} value={i} style={{ backgroundColor: "#0f1629" }}>
                        {i}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="form-label" htmlFor="su-website">
                    <Globe size={11} className="inline mr-1 mb-0.5" />
                    Website URL
                  </label>
                  <input
                    id="su-website"
                    type="url"
                    className="input-glass"
                    placeholder="https://company.com"
                    {...register("website_url")}
                  />
                </div>
              </div>

              <button
                id="signup-submit"
                type="submit"
                disabled={loading}
                className="btn-gradient w-full flex items-center justify-center gap-2 py-3 text-sm mt-2"
              >
                {loading ? (
                  <><Loader2 size={16} className="animate-spin" /> Creating account...</>
                ) : (
                  <>Create Account <ArrowRight size={16} /></>
                )}
              </button>
            </form>

            <p className="text-center text-xs mt-5" style={{ color: "var(--text-muted)" }}>
              Already have an account?{" "}
              <Link href="/login" className="font-semibold" style={{ color: "#a5b4fc" }}>
                Sign in
              </Link>
            </p>

            <p className="text-center text-xs mt-3" style={{ color: "var(--text-muted)" }}>
              By signing up you agree to our Terms of Service and Privacy Policy.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
