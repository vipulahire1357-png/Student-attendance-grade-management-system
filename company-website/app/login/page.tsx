"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { authAPI, authStorage } from "@/services/api";
import { Zap, Mail, Lock, Loader2, AlertCircle, Eye, EyeOff, ArrowLeft } from "lucide-react";

interface LoginForm {
  email: string;
  password: string;
}

export default function LoginPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showPw, setShowPw] = useState(false);

  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>();

  const onSubmit = async (data: LoginForm) => {
    setLoading(true);
    setError(null);
    try {
      const res = await authAPI.login(data.email, data.password);
      authStorage.save(res.data.access_token, res.data.refresh_token, res.data.role);
      router.push("/dashboard");
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } } };
      setError(e?.response?.data?.detail ?? "Invalid email or password.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center px-4 relative overflow-hidden"
      style={{ background: "var(--bg-primary)" }}
    >
      {/* Orbs */}
      <div
        className="glow-orb w-96 h-96 opacity-15"
        style={{ background: "rgba(99,102,241,1)", top: "-120px", left: "-100px" }}
      />
      <div
        className="glow-orb w-64 h-64 opacity-10"
        style={{ background: "rgba(6,182,212,1)", bottom: "-60px", right: "-60px" }}
      />

      <div className="w-full max-w-md relative z-10 animate-slide-up">
        {/* Back */}
        <Link
          href="/"
          className="flex items-center gap-1.5 text-sm mb-8 transition-colors"
          style={{ color: "var(--text-muted)" }}
        >
          <ArrowLeft size={15} />
          Back to home
        </Link>

        <div className="glass-card p-8">
          {/* Logo */}
          <div className="flex flex-col items-center mb-8">
            <div
              className="w-12 h-12 rounded-2xl flex items-center justify-center mb-4"
              style={{
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                boxShadow: "0 0 30px rgba(99,102,241,0.35)",
              }}
            >
              <Zap size={22} className="text-white" />
            </div>
            <h1
              className="text-2xl font-bold"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              Welcome back
            </h1>
            <p className="text-sm mt-1" style={{ color: "var(--text-muted)" }}>
              Sign in to your company account
            </p>
          </div>

          {/* Error */}
          {error && (
            <div className="alert alert-error mb-5 animate-fade-in">
              <AlertCircle size={15} />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit(onSubmit)} className="form-section">
            {/* Email */}
            <div>
              <label className="form-label" htmlFor="login-email">
                <Mail size={11} className="inline mr-1 mb-0.5" />
                Email Address
              </label>
              <input
                id="login-email"
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
              <label className="form-label" htmlFor="login-password">
                <Lock size={11} className="inline mr-1 mb-0.5" />
                Password
              </label>
              <div className="relative">
                <input
                  id="login-password"
                  type={showPw ? "text" : "password"}
                  className="input-glass pr-10"
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  {...register("password", { required: "Password is required" })}
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

            <button
              id="login-submit"
              type="submit"
              disabled={loading}
              className="btn-gradient w-full flex items-center justify-center gap-2 py-3 text-sm"
            >
              {loading ? (
                <><Loader2 size={16} className="animate-spin" /> Signing in...</>
              ) : (
                "Sign in to Dashboard"
              )}
            </button>
          </form>

          <p className="text-center text-sm mt-6" style={{ color: "var(--text-muted)" }}>
            No account yet?{" "}
            <Link
              href="/signup"
              className="font-semibold transition-colors"
              style={{ color: "#a5b4fc" }}
            >
              Create company account
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
