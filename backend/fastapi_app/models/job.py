"""Job & Application ORM models."""
from sqlalchemy import (
    Boolean, Column, Float, ForeignKey, Integer, Numeric, String, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Job(Base):
    __tablename__ = "jobs"

    id               = Column(Integer, primary_key=True, index=True)
    company_id       = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    title            = Column(String(255), nullable=False)
    description      = Column(Text, nullable=False)
    requirements     = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    job_type         = Column(String(50), nullable=True)      # full-time / part-time / internship / contract / remote
    location         = Column(String(255), nullable=True)
    remote_allowed   = Column(Boolean, default=False)
    salary_min       = Column(Numeric(12, 2), nullable=True)
    salary_max       = Column(Numeric(12, 2), nullable=True)
    currency         = Column(String(10), default="USD")
    experience_level = Column(String(50), nullable=True)      # entry / mid / senior / lead
    is_active        = Column(Boolean, default=True)
    expires_at       = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at       = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    company      = relationship("Company", back_populates="jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Job id={self.id} title={self.title!r}>"


class Application(Base):
    __tablename__ = "applications"

    id             = Column(Integer, primary_key=True, index=True)
    job_id         = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id     = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    cover_letter   = Column(Text, nullable=True)
    resume_url     = Column(Text, nullable=True)
    status         = Column(String(50), default="pending")   # pending / reviewed / shortlisted / rejected / hired
    ai_match_score = Column(Float, nullable=True)
    notes          = Column(Text, nullable=True)
    applied_at     = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at     = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    job     = relationship("Job", back_populates="applications")
    student = relationship("Student", back_populates="applications")

    def __repr__(self) -> str:
        return f"<Application id={self.id} job_id={self.job_id} student_id={self.student_id}>"
