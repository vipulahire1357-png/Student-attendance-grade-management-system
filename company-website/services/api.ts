/**
 * API Service Layer — OnlyStudents Company Website
 * All Axios calls to the FastAPI backend live here.
 */
import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

// ── Axios Instance ────────────────────────────────────────────────────────────
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 15_000,
});

// Token storage keys
const TOKEN_KEY = "os_company_access_token";
const REFRESH_KEY = "os_company_refresh_token";
const ROLE_KEY = "os_company_role";

// ── Request Interceptor: attach Bearer token ──────────────────────────────────
api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem(TOKEN_KEY);
    if (token && config.headers) {
      config.headers["Authorization"] = `Bearer ${token}`;
    }
  }
  return config;
});

// ── Response Interceptor: handle 401 globally ─────────────────────────────────
api.interceptors.response.use(
  (res) => res,
  (error: AxiosError) => {
    if (error.response?.status === 401 && typeof window !== "undefined") {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(REFRESH_KEY);
      localStorage.removeItem(ROLE_KEY);
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;

// ── Helpers ───────────────────────────────────────────────────────────────────
export const authStorage = {
  save: (accessToken: string, refreshToken: string, role: string) => {
    localStorage.setItem(TOKEN_KEY, accessToken);
    localStorage.setItem(REFRESH_KEY, refreshToken);
    localStorage.setItem(ROLE_KEY, role);
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(ROLE_KEY);
  },
  getToken: () =>
    typeof window !== "undefined" ? localStorage.getItem(TOKEN_KEY) : null,
};

// ── Types ─────────────────────────────────────────────────────────────────────
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  role: string;
}

export interface CompanySignup {
  email: string;
  password: string;
  company_name: string;
  industry?: string;
  website_url?: string;
}

export interface CompanyProfile {
  id: number;
  email: string;
  company_name: string;
  slug: string;
  description?: string;
  logo_url?: string;
  website_url?: string;
  industry?: string;
  size?: string;
  founded_year?: number;
  headquarters?: string;
  linkedin_url?: string;
  is_verified: boolean;
  created_at: string;
}

export interface CompanyUpdate {
  company_name?: string;
  description?: string;
  logo_url?: string;
  website_url?: string;
  industry?: string;
  size?: string;
  founded_year?: number;
  headquarters?: string;
  linkedin_url?: string;
}

export interface JobCreate {
  title: string;
  description: string;
  requirements?: string;
  responsibilities?: string;
  job_type?: string;
  location?: string;
  remote_allowed?: boolean;
  salary_min?: number;
  salary_max?: number;
  currency?: string;
  experience_level?: string;
  expires_at?: string;
}

export interface JobOut {
  id: number;
  company_id: number;
  title: string;
  description: string;
  requirements?: string;
  responsibilities?: string;
  job_type?: string;
  location?: string;
  remote_allowed: boolean;
  salary_min?: number;
  salary_max?: number;
  currency: string;
  experience_level?: string;
  is_active: boolean;
  expires_at?: string;
  created_at: string;
}

export interface ProblemCreate {
  title: string;
  description: string;
  problem_type?: string;
  difficulty?: string;
  reward?: string;
  deadline?: string;
  required_skills?: string[];
  max_submissions?: number;
}

export interface ProblemOut {
  id: number;
  company_id: number;
  title: string;
  description: string;
  problem_type?: string;
  difficulty?: string;
  reward?: string;
  deadline?: string;
  required_skills?: string[];
  is_active: boolean;
  max_submissions?: number;
  created_at: string;
}

export interface CandidateOut {
  student_id: number;
  full_name: string;
  email: string;
  university?: string;
  degree?: string;
  match_score?: number;
  job_title?: string;
  job_id?: number;
}

export interface MatchRequest {
  student_id: number;
  job_id: number;
}

export interface MatchResponse {
  student_id: number;
  job_id: number;
  score: number;
}

// ── Auth API ──────────────────────────────────────────────────────────────────
export const authAPI = {
  signup: (data: CompanySignup) =>
    api.post<TokenResponse>("/auth/company/signup", data),

  login: (email: string, password: string) =>
    api.post<TokenResponse>("/auth/login", {
      email,
      password,
      role: "company",
    }),
};

// ── Companies API ─────────────────────────────────────────────────────────────
export const companyAPI = {
  getProfile: () => api.get<CompanyProfile>("/companies/profile"),

  updateProfile: (data: CompanyUpdate) =>
    api.patch<CompanyProfile>("/companies/profile", data),

  postJob: (data: JobCreate) =>
    api.post<JobOut>("/companies/post-job", data),

  postProblem: (data: ProblemCreate) =>
    api.post<ProblemOut>("/companies/post-problem", data),

  getCandidates: (params?: { job_id?: number; skip?: number; limit?: number }) =>
    api.get("/companies/candidates", { params }),
};

// ── Jobs API ──────────────────────────────────────────────────────────────────
export const jobsAPI = {
  listJobs: (params?: {
    skip?: number;
    limit?: number;
    job_type?: string;
    location?: string;
  }) => api.get<JobOut[]>("/jobs", { params }),

  getJob: (id: number) => api.get<JobOut>(`/jobs/${id}`),
};

// ── Problems API ──────────────────────────────────────────────────────────────
export const problemsAPI = {
  listProblems: () => api.get<ProblemOut[]>("/problems"),
};

// ── AI API ────────────────────────────────────────────────────────────────────
export const aiAPI = {
  matchStudentJob: (data: MatchRequest) =>
    api.post<MatchResponse>("/ai/match-student-job", data),

  generateJobEmbedding: (jobId: number) =>
    api.post(`/ai/embeddings/job/${jobId}`),
};
