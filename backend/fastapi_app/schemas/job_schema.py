"""Pydantic schemas for Job & Application endpoints."""
from __future__ import annotations
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, field_validator


# ── Job Create (Company posts a job) ────────────────────────────────────────
class JobCreate(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    job_type: Optional[str] = None           # full-time / part-time / internship / contract / remote
    location: Optional[str] = None
    remote_allowed: bool = False
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    currency: str = "USD"
    experience_level: Optional[str] = None   # entry / mid / senior / lead
    expires_at: Optional[datetime] = None

    @field_validator("job_type")
    @classmethod
    def validate_job_type(cls, v: Optional[str]) -> Optional[str]:
        allowed = {"full-time", "part-time", "internship", "contract", "remote", None}
        if v not in allowed:
            raise ValueError(f"job_type must be one of {allowed - {None}}")
        return v


# ── Job Response ─────────────────────────────────────────────────────────────
class JobOut(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    job_type: Optional[str] = None
    location: Optional[str] = None
    remote_allowed: bool
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    currency: str
    experience_level: Optional[str] = None
    is_active: bool
    expires_at: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Application Create (Student applies) ─────────────────────────────────────
class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None


# ── Application Response ──────────────────────────────────────────────────────
class ApplicationOut(BaseModel):
    id: int
    job_id: int
    student_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: str
    ai_match_score: Optional[float] = None
    applied_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Candidate preview (for companies) ────────────────────────────────────────
class CandidateOut(BaseModel):
    application_id: int
    student_id: int
    full_name: str
    email: str
    university: Optional[str] = None
    degree: Optional[str] = None
    ai_match_score: Optional[float] = None
    status: str
    applied_at: datetime

    model_config = {"from_attributes": True}
