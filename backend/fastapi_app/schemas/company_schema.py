"""Pydantic schemas for Company endpoints."""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator


# ── Company Signup ───────────────────────────────────────────────────────────
class CompanySignup(BaseModel):
    email: EmailStr
    password: str
    company_name: str
    industry: Optional[str] = None
    website_url: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


# ── Company Update ───────────────────────────────────────────────────────────
class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    linkedin_url: Optional[str] = None


# ── Company Profile Response ─────────────────────────────────────────────────
class CompanyProfile(BaseModel):
    id: int
    email: EmailStr
    company_name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    founded_year: Optional[int] = None
    headquarters: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}
