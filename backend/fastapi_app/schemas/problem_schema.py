"""Pydantic schemas for Industry Problem & Submission endpoints."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


# ── Problem Create ────────────────────────────────────────────────────────────
class ProblemCreate(BaseModel):
    title: str
    description: str
    problem_type: Optional[str] = None     # research / design / engineering / data / marketing
    difficulty: Optional[str] = None       # easy / medium / hard / expert
    reward: Optional[str] = None
    deadline: Optional[datetime] = None
    required_skills: Optional[List[str]] = None
    max_submissions: Optional[int] = None


# ── Problem Response ──────────────────────────────────────────────────────────
class ProblemOut(BaseModel):
    id: int
    company_id: int
    title: str
    description: str
    problem_type: Optional[str] = None
    difficulty: Optional[str] = None
    reward: Optional[str] = None
    deadline: Optional[datetime] = None
    required_skills: Optional[List[str]] = None
    is_active: bool
    max_submissions: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Submission Create ─────────────────────────────────────────────────────────
class SubmissionCreate(BaseModel):
    problem_id: int
    solution_text: Optional[str] = None
    solution_url: Optional[str] = None
    submission_type: str = "text"   # text / link / file


# ── Submission Response ───────────────────────────────────────────────────────
class SubmissionOut(BaseModel):
    id: int
    problem_id: int
    student_id: int
    solution_text: Optional[str] = None
    solution_url: Optional[str] = None
    submission_type: str
    status: str
    feedback: Optional[str] = None
    score: Optional[float] = None
    submitted_at: datetime

    model_config = {"from_attributes": True}
