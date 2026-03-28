"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import Navbar from "@/components/Navbar";
import { Loader2 } from "lucide-react";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !isAuthenticated) {
      router.replace("/login");
    }
  }, [loading, isAuthenticated, router]);

  if (loading) {
    return (
      <div
        className="min-h-screen flex items-center justify-center"
        style={{ background: "var(--bg-primary)" }}
      >
        <div className="flex items-center gap-3" style={{ color: "var(--text-muted)" }}>
          <Loader2 size={20} className="animate-spin" />
          <span>Loading...</span>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return null;

  return (
    <div style={{ background: "var(--bg-primary)", minHeight: "100vh" }}>
      <Navbar />
      <main className="pt-20 px-4 pb-12 max-w-7xl mx-auto">{children}</main>
    </div>
  );
}
