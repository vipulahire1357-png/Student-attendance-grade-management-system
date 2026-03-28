"use client";

import Link from "next/link";
import Navbar from "@/components/Navbar";
import {
  Zap,
  Briefcase,
  Users,
  Brain,
  Lightbulb,
  ChevronRight,
  CheckCircle,
  Star,
  ArrowRight,
  Building2,
  BarChart3,
  Shield,
} from "lucide-react";

const FEATURES = [
  {
    icon: Briefcase,
    title: "Post Job Listings",
    desc: "Publish positions in minutes. Reach thousands of pre-vetted student candidates actively seeking opportunities.",
    color: "#6366f1",
  },
  {
    icon: Lightbulb,
    title: "Share Industry Problems",
    desc: "Post real-world challenges and let students compete to solve them. Discover hidden talent through action.",
    color: "#8b5cf6",
  },
  {
    icon: Brain,
    title: "AI-Powered Matching",
    desc: "Our semantic AI engine matches candidates to your roles using skill embeddings — not just keywords.",
    color: "#06b6d4",
  },
  {
    icon: Users,
    title: "View Submissions",
    desc: "Browse student submissions, evaluate solutions, and build a pipeline of proven talent.",
    color: "#10b981",
  },
];

const STATS = [
  { label: "Student Candidates", value: "50K+", icon: Users },
  { label: "Companies Hiring", value: "1,200+", icon: Building2 },
  { label: "Jobs Filled (AI)", value: "8,400+", icon: BarChart3 },
  { label: "Match Accuracy", value: "94%", icon: Brain },
];

const TESTIMONIALS = [
  {
    quote: "We hired 3 interns in 2 weeks — students who already knew our tech stack. The AI matching is scarily accurate.",
    name: "Sarah Chen",
    role: "Engineering Lead · Stripe",
    rating: 5,
  },
  {
    quote: "Posted an industry challenge and got 120 submissions in 48 hours. Found our next ML engineer through it.",
    name: "Marcus Rodriguez",
    role: "CTO · Vercel",
    rating: 5,
  },
  {
    quote: "OnlyStudents cut our campus recruiting time from 3 months to 3 weeks. It's the future.",
    name: "Aisha Patel",
    role: "HR Director · Notion",
    rating: 5,
  },
];

export default function LandingPage() {
  return (
    <div className="relative min-h-screen overflow-x-hidden">
      <Navbar />

      {/* Hero */}
      <section className="relative pt-32 pb-20 px-4">
        {/* Background orbs */}
        <div
          className="glow-orb w-96 h-96 opacity-20"
          style={{
            background: "rgba(99,102,241,1)",
            top: "-100px",
            left: "-100px",
          }}
        />
        <div
          className="glow-orb w-80 h-80 opacity-15"
          style={{
            background: "rgba(6,182,212,1)",
            top: "0",
            right: "-80px",
          }}
        />

        <div className="max-w-5xl mx-auto text-center relative z-10 animate-slide-up">
          {/* Eyebrow */}
          <div
            className="inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium mb-8"
            style={{
              background: "rgba(99,102,241,0.12)",
              border: "1px solid rgba(99,102,241,0.25)",
              color: "#a5b4fc",
            }}
          >
            <Zap size={14} />
            Powered by Semantic AI Matching
          </div>

          <h1
            className="text-5xl md:text-7xl font-extrabold leading-tight mb-6"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            Hire the brightest
            <br />
            <span className="gradient-text">student talent</span>
            <br />
            with AI precision
          </h1>

          <p
            className="text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed"
            style={{ color: "var(--text-muted)" }}
          >
            OnlyStudents connects your company with pre-vetted, skills-verified students.
            Post jobs, share real problems, and let our AI surface the perfect candidates
            — automatically.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/signup"
              className="btn-gradient flex items-center gap-2 text-base px-8 py-3.5"
            >
              Start Hiring Free <ArrowRight size={18} />
            </Link>
            <Link
              href="/login"
              className="flex items-center gap-2 text-sm font-semibold px-6 py-3.5 rounded-xl transition-all"
              style={{
                background: "rgba(255,255,255,0.05)",
                border: "1px solid rgba(255,255,255,0.1)",
                color: "var(--text-primary)",
              }}
            >
              Login to Dashboard <ChevronRight size={16} />
            </Link>
          </div>

          {/* Trust indicators */}
          <div
            className="flex flex-wrap justify-center gap-6 mt-10 text-sm"
            style={{ color: "var(--text-muted)" }}
          >
            {["No credit card required", "GDPR Compliant", "Cancel anytime"].map((t) => (
              <span key={t} className="flex items-center gap-1.5">
                <CheckCircle size={14} style={{ color: "#10b981" }} />
                {t}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="py-12 px-4">
        <div className="max-w-5xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-4">
          {STATS.map(({ label, value, icon: Icon }) => (
            <div key={label} className="stat-card text-center">
              <Icon
                size={22}
                className="mx-auto mb-3"
                style={{ color: "#6366f1" }}
              />
              <div
                className="text-3xl font-extrabold gradient-text mb-1"
                style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
              >
                {value}
              </div>
              <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                {label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2
              className="text-3xl md:text-4xl font-bold mb-4"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              Everything you need to
              <span className="gradient-text"> recruit smarter</span>
            </h2>
            <p style={{ color: "var(--text-muted)" }}>
              A complete platform built for modern talent acquisition
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {FEATURES.map(({ icon: Icon, title, desc, color }) => (
              <div
                key={title}
                className="glass-card p-7 group cursor-default"
                style={{ transition: "transform 0.2s ease" }}
                onMouseEnter={(e) =>
                ((e.currentTarget as HTMLElement).style.transform =
                  "translateY(-4px)")
                }
                onMouseLeave={(e) =>
                  ((e.currentTarget as HTMLElement).style.transform = "none")
                }
              >
                <div
                  className="w-11 h-11 rounded-xl flex items-center justify-center mb-5"
                  style={{
                    background: `${color}1a`,
                    border: `1px solid ${color}33`,
                  }}
                >
                  <Icon size={20} style={{ color }} />
                </div>
                <h3
                  className="text-lg font-bold mb-2"
                  style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
                >
                  {title}
                </h3>
                <p className="text-sm leading-relaxed" style={{ color: "var(--text-muted)" }}>
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <h2
            className="text-3xl font-bold text-center mb-14"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            Up and hiring in <span className="gradient-text">3 steps</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              {
                num: "01",
                title: "Create your account",
                desc: "Sign up in 60 seconds. Add your company profile, industry, and hiring needs.",
              },
              {
                num: "02",
                title: "Post a job or problem",
                desc: "Publish a job listing or share a real industry challenge for students to solve.",
              },
              {
                num: "03",
                title: "AI finds your candidates",
                desc: "Our AI matches your role to the best-fit students. Review, shortlist, and hire.",
              },
            ].map(({ num, title, desc }) => (
              <div key={num} className="text-center relative">
                <div
                  className="text-5xl font-extrabold mb-4 gradient-text"
                  style={{ fontFamily: "Plus Jakarta Sans, sans-serif", opacity: 0.7 }}
                >
                  {num}
                </div>
                <h3 className="text-base font-semibold mb-2">{title}</h3>
                <p className="text-sm" style={{ color: "var(--text-muted)" }}>
                  {desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <h2
            className="text-3xl font-bold text-center mb-12"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            Trusted by <span className="gradient-text">top companies</span>
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {TESTIMONIALS.map(({ quote, name, role, rating }) => (
              <div key={name} className="glass-card p-6 flex flex-col gap-4">
                <div className="flex gap-0.5">
                  {Array.from({ length: rating }).map((_, i) => (
                    <Star
                      key={i}
                      size={14}
                      fill="#f59e0b"
                      style={{ color: "#f59e0b" }}
                    />
                  ))}
                </div>
                <p
                  className="text-sm leading-relaxed italic"
                  style={{ color: "var(--text-muted)" }}
                >
                  &ldquo;{quote}&rdquo;
                </p>
                <div>
                  <div className="text-sm font-semibold">{name}</div>
                  <div className="text-xs" style={{ color: "var(--text-muted)" }}>
                    {role}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Banner */}
      <section className="py-20 px-4">
        <div className="max-w-3xl mx-auto text-center glass-card p-12 relative overflow-hidden">
          <div
            className="glow-orb w-64 h-64 opacity-20"
            style={{
              background: "rgba(99,102,241,1)",
              top: "-50px",
              left: "-50px",
            }}
          />
          <Shield size={32} className="mx-auto mb-5" style={{ color: "#6366f1" }} />
          <h2
            className="text-3xl font-bold mb-4 relative z-10"
            style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
          >
            Ready to find your next
            <span className="gradient-text"> star hire?</span>
          </h2>
          <p
            className="mb-8 relative z-10"
            style={{ color: "var(--text-muted)" }}
          >
            Join 1,200+ companies already using OnlyStudents to build world-class
            teams.
          </p>
          <Link
            href="/signup"
            className="btn-gradient inline-flex items-center gap-2 text-base px-8 py-3.5 relative z-10"
          >
            Create Company Account <ArrowRight size={18} />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer
        className="py-8 px-4 text-center text-xs"
        style={{
          color: "var(--text-muted)",
          borderTop: "1px solid rgba(99,102,241,0.1)",
        }}
      >
        © {new Date().getFullYear()} OnlyStudents · Company Portal · Built with ❤️ for the future of hiring
      </footer>
    </div>
  );
}