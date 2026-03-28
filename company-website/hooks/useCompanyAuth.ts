/**
 * useCompanyAuth.ts
 * Auth-specific React Query mutation hooks for company login / signup.
 * Kept separate from useCompany.ts (data hooks) to follow single-responsibility.
 */
"use client";

import { useMutation } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { authAPI, authStorage, type CompanySignup, type TokenResponse } from "@/services/api";

// ── Types ─────────────────────────────────────────────────────────────────────

export interface LoginPayload {
  email: string;
  password: string;
}

export interface AuthError {
  message: string;
  status?: number;
}

function parseError(err: unknown): AuthError {
  const e = err as { response?: { status?: number; data?: { detail?: string } } };
  return {
    message: e?.response?.data?.detail ?? "An unexpected error occurred.",
    status: e?.response?.status,
  };
}

// ── useLogin ──────────────────────────────────────────────────────────────────
/**
 * Mutation hook for company login.
 * On success, persists tokens and redirects to /dashboard.
 *
 * @example
 * const { mutate: login, isPending, error } = useLogin();
 * login({ email, password });
 */
export function useLogin() {
  const router = useRouter();

  return useMutation<TokenResponse, AuthError, LoginPayload>({
    mutationFn: async ({ email, password }) => {
      const res = await authAPI.login(email, password);
      return res.data;
    },
    onSuccess: (data) => {
      authStorage.save(data.access_token, data.refresh_token, data.role);
      router.push("/dashboard");
    },
    onError: (err: unknown) => parseError(err),
  });
}

// ── useSignup ─────────────────────────────────────────────────────────────────
/**
 * Mutation hook for company signup.
 * On success, persists tokens and redirects to /dashboard.
 *
 * @example
 * const { mutate: signup, isPending, error } = useSignup();
 * signup({ email, password, company_name, industry, website_url });
 */
export function useSignup() {
  const router = useRouter();

  return useMutation<TokenResponse, AuthError, CompanySignup>({
    mutationFn: async (payload: CompanySignup) => {
      const res = await authAPI.signup(payload);
      return res.data;
    },
    onSuccess: (data) => {
      authStorage.save(data.access_token, data.refresh_token, data.role);
      router.push("/dashboard");
    },
    onError: (err: unknown) => parseError(err),
  });
}

// ── useLogout ─────────────────────────────────────────────────────────────────
/**
 * Simple helper hook that clears auth state and redirects to /login.
 *
 * @example
 * const logout = useLogout();
 * <button onClick={logout}>Logout</button>
 */
export function useLogout() {
  const router = useRouter();

  return () => {
    authStorage.clear();
    router.replace("/login");
  };
}

// ── useIsAuthenticated ────────────────────────────────────────────────────────
/**
 * Lightweight synchronous check — returns true if a token is present
 * in localStorage. For reactive auth state, use AuthContext instead.
 *
 * @example
 * const isAuth = useIsAuthenticated();
 */
export function useIsAuthenticated(): boolean {
  if (typeof window === "undefined") return false;
  return !!authStorage.getToken();
}
