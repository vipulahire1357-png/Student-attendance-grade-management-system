"""Student ORM model."""
from sqlalchemy import (
    Boolean, Column, Float, Integer, String, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Student(Base):
    __tablename__ = "students"

    id              = Column(Integer, primary_key=True, index=True)
    email           = Column(String(255), unique=True, nullable=False, index=True)
    password_hash   = Column(Text, nullable=False)
    full_name       = Column(String(255), nullable=False)
    username        = Column(String(100), unique=True, nullable=False, index=True)
    bio             = Column(Text, nullable=True)
    avatar_url      = Column(Text, nullable=True)
    university      = Column(String(255), nullable=True)
    degree          = Column(String(255), nullable=True)
    graduation_year = Column(Integer, nullable=True)
    github_url      = Column(Text, nullable=True)
    linkedin_url    = Column(Text, nullable=True)
    portfolio_url   = Column(Text, nullable=True)
    resume_url      = Column(Text, nullable=True)
    gpa             = Column(Float, nullable=True)
    location        = Column(String(255), nullable=True)
    is_active       = Column(Boolean, default=True)
    is_verified     = Column(Boolean, default=False)
    created_at      = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at      = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    skills          = relationship("StudentSkill", back_populates="student", cascade="all, delete-orphan")
    projects        = relationship("Project", back_populates="student", cascade="all, delete-orphan")
    applications    = relationship("Application", back_populates="student", cascade="all, delete-orphan")
    submissions     = relationship("ProblemSubmission", back_populates="student", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Student id={self.id} username={self.username!r}>"
