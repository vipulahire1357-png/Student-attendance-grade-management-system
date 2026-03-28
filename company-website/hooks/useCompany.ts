"use client";

import { useQuery } from "@tanstack/react-query";
import { companyAPI, CompanyProfile, CandidateOut } from "@/services/api";

// ── Company Profile ───────────────────────────────────────────────────────────
export function useCompanyProfile() {
  return useQuery<CompanyProfile>({
    queryKey: ["company-profile"],
    queryFn: async () => {
      const res = await companyAPI.getProfile();
      return res.data;
    },
    retry: 1,
  });
}

// ── Candidates ────────────────────────────────────────────────────────────────
export function useCandidates(jobId?: number) {
  return useQuery<{ company_id: number; total: number; candidates: CandidateOut[] }>({
    queryKey: ["candidates", jobId],
    queryFn: async () => {
      const res = await companyAPI.getCandidates(jobId ? { job_id: jobId } : {});
      return res.data;
    },
    retry: 1,
  });
}
