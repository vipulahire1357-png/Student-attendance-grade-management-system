"""Pydantic schemas for Student endpoints."""
from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, HttpUrl, field_validator


# ── Skill inside a Student profile ──────────────────────────────────────────
class SkillOut(BaseModel):
    skill_id: int
    name: str
    category: Optional[str] = None
    proficiency: str

    model_config = {"from_attributes": True}


# ── Project inside a Student profile ────────────────────────────────────────
class ProjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    repo_url: Optional[str] = None
    live_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_featured: bool
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Student Signup ───────────────────────────────────────────────────────────
class StudentSignup(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    username: str
    university: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v

    @field_validator("username")
    @classmethod
    def username_format(cls, v: str) -> str:
        v = v.strip().lower()
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        return v


# ── Student Update ───────────────────────────────────────────────────────────
class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    university: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    gpa: Optional[float] = None
    location: Optional[str] = None


# ── Student Profile Response ─────────────────────────────────────────────────
class StudentProfile(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    university: Optional[str] = None
    degree: Optional[str] = None
    graduation_year: Optional[int] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    resume_url: Optional[str] = None
    gpa: Optional[float] = None
    location: Optional[str] = None
    is_verified: bool
    created_at: datetime
    skills: List[SkillOut] = []
    projects: List[ProjectOut] = []

    model_config = {"from_attributes": True}


# ── Upload Project ───────────────────────────────────────────────────────────
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    repo_url: Optional[str] = None
    live_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    is_featured: bool = False


# ── Add Skill ────────────────────────────────────────────────────────────────
class AddSkill(BaseModel):
    skill_id: int
    proficiency: str = "beginner"

    @field_validator("proficiency")
    @classmethod
    def validate_proficiency(cls, v: str) -> str:
        allowed = {"beginner", "intermediate", "advanced", "expert"}
        if v not in allowed:
            raise ValueError(f"proficiency must be one of {allowed}")
        return v
