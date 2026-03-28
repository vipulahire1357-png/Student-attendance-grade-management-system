"""IndustryProblem & ProblemSubmission ORM models."""
from sqlalchemy import (
    Boolean, Column, Float, ForeignKey, Integer, String, Text, TIMESTAMP, ARRAY
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class IndustryProblem(Base):
    __tablename__ = "industry_problems"

    id              = Column(Integer, primary_key=True, index=True)
    company_id      = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    title           = Column(String(255), nullable=False)
    description     = Column(Text, nullable=False)
    problem_type    = Column(String(100), nullable=True)   # research / design / engineering / data / marketing
    difficulty      = Column(String(50), nullable=True)    # easy / medium / hard / expert
    reward          = Column(Text, nullable=True)
    deadline        = Column(TIMESTAMP(timezone=True), nullable=True)
    required_skills = Column(ARRAY(String), nullable=True)
    is_active       = Column(Boolean, default=True)
    max_submissions = Column(Integer, nullable=True)
    created_at      = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at      = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    company     = relationship("Company", back_populates="problems")
    submissions = relationship("ProblemSubmission", back_populates="problem", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<IndustryProblem id={self.id} title={self.title!r}>"


class ProblemSubmission(Base):
    __tablename__ = "problem_submissions"

    id              = Column(Integer, primary_key=True, index=True)
    problem_id      = Column(Integer, ForeignKey("industry_problems.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id      = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    solution_text   = Column(Text, nullable=True)
    solution_url    = Column(Text, nullable=True)
    submission_type = Column(String(50), nullable=True)   # text / link / file
    status          = Column(String(50), default="submitted")  # submitted / under_review / accepted / rejected
    feedback        = Column(Text, nullable=True)
    score           = Column(Float, nullable=True)
    submitted_at    = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at      = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    problem = relationship("IndustryProblem", back_populates="submissions")
    student = relationship("Student", back_populates="submissions")

    def __repr__(self) -> str:
        return f"<ProblemSubmission id={self.id} problem_id={self.problem_id}>"
