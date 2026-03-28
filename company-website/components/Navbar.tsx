"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import {
  Briefcase,
  LayoutDashboard,
  Users,
  Zap,
  LogOut,
  Menu,
  X,
  ChevronRight,
  Lightbulb,
} from "lucide-react";
import { useState } from "react";

const NAV_LINKS = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/post-job", label: "Post Job", icon: Briefcase },
  { href: "/post-problem", label: "Post Problem", icon: Lightbulb },
  { href: "/candidates", label: "Candidates", icon: Users },
];

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="fixed top-0 inset-x-0 z-50">
      <div
        className="mx-auto px-4 py-3"
        style={{
          background: "rgba(10, 15, 30, 0.85)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          borderBottom: "1px solid rgba(99, 102, 241, 0.15)",
        }}
      >
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 no-underline">
            <div
              className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{
                background: "linear-gradient(135deg, #6366f1, #8b5cf6)",
                boxShadow: "0 0 20px rgba(99,102,241,0.4)",
              }}
            >
              <Zap size={16} className="text-white" />
            </div>
            <span
              className="font-bold text-lg"
              style={{ fontFamily: "Plus Jakarta Sans, sans-serif" }}
            >
              Only<span className="gradient-text">Students</span>
            </span>
            <span
              className="text-xs px-2 py-0.5 rounded-full"
              style={{
                background: "rgba(99,102,241,0.15)",
                color: "#a5b4fc",
                border: "1px solid rgba(99,102,241,0.25)",
              }}
            >
              Company
            </span>
          </Link>

          {/* Desktop Nav */}
          {isAuthenticated && (
            <nav className="hidden md:flex items-center gap-1">
              {NAV_LINKS.map(({ href, label, icon: Icon }) => {
                const active = pathname === href;
                return (
                  <Link
                    key={href}
                    href={href}
                    className={`sidebar-link text-sm ${active ? "active" : ""}`}
                  >
                    <Icon size={15} />
                    {label}
                  </Link>
                );
              })}
            </nav>
          )}

          {/* Right Actions */}
          <div className="flex items-center gap-2">
            {isAuthenticated ? (
              <button
                onClick={logout}
                className="hidden md:flex items-center gap-2 text-sm font-medium px-3 py-2 rounded-lg transition-all"
                style={{ color: "var(--text-muted)" }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.color = "#fca5a5")
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.color = "var(--text-muted)")
                }
              >
                <LogOut size={15} />
                Logout
              </button>
            ) : (
              <div className="hidden md:flex items-center gap-2">
                <Link
                  href="/login"
                  className="sidebar-link text-sm"
                >
                  Login
                </Link>
                <Link
                  href="/signup"
                  className="btn-gradient text-sm flex items-center gap-1"
                >
                  Get Started <ChevronRight size={14} />
                </Link>
              </div>
            )}

            {/* Mobile Toggle */}
            <button
              className="md:hidden p-2 rounded-lg"
              style={{
                background: "rgba(99,102,241,0.1)",
                color: "#a5b4fc",
              }}
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label="Toggle menu"
            >
              {mobileOpen ? <X size={18} /> : <Menu size={18} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileOpen && (
          <div
            className="md:hidden pt-3 pb-2 mt-2 rounded-xl animate-fade-in"
            style={{
              borderTop: "1px solid rgba(99,102,241,0.15)",
            }}
          >
            {isAuthenticated ? (
              <>
                {NAV_LINKS.map(({ href, label, icon: Icon }) => (
                  <Link
                    key={href}
                    href={href}
                    className={`sidebar-link ${pathname === href ? "active" : ""}`}
                    onClick={() => setMobileOpen(false)}
                  >
                    <Icon size={15} />
                    {label}
                  </Link>
                ))}
                <button
                  onClick={() => { logout(); setMobileOpen(false); }}
                  className="sidebar-link w-full text-left mt-1"
                  style={{ color: "#fca5a5" }}
                >
                  <LogOut size={15} />
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link href="/login" className="sidebar-link" onClick={() => setMobileOpen(false)}>
                  Login
                </Link>
                <Link href="/signup" className="sidebar-link" onClick={() => setMobileOpen(false)}>
                  Sign Up
                </Link>
              </>
            )}
          </div>
        )}
      </div>
    </header>
  );
}
