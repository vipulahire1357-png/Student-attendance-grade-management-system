"""Skill, StudentSkill, SkillProof, Project & AIEmbedding ORM models."""
from sqlalchemy import (
    Boolean, Column, Float, ForeignKey, Integer, String, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector

from ..database import Base
from ..config import settings


class Skill(Base):
    __tablename__ = "skills"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), unique=True, nullable=False)
    category    = Column(String(100), nullable=True)
    created_at  = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # ── Relationships ─────────────────────────────────────
    student_skills = relationship("StudentSkill", back_populates="skill")

    def __repr__(self) -> str:
        return f"<Skill id={self.id} name={self.name!r}>"


class StudentSkill(Base):
    __tablename__ = "student_skills"

    id          = Column(Integer, primary_key=True, index=True)
    student_id  = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id    = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency = Column(String(50), default="beginner")   # beginner / intermediate / advanced / expert
    verified    = Column(Boolean, default=False)
    created_at  = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # ── Relationships ─────────────────────────────────────
    student = relationship("Student", back_populates="skills")
    skill   = relationship("Skill", back_populates="student_skills")
    proofs  = relationship("SkillProof", back_populates="student_skill", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<StudentSkill student_id={self.student_id} skill_id={self.skill_id}>"


class SkillProof(Base):
    __tablename__ = "skill_proofs"

    id               = Column(Integer, primary_key=True, index=True)
    student_skill_id = Column(Integer, ForeignKey("student_skills.id", ondelete="CASCADE"), nullable=False)
    proof_type       = Column(String(50), nullable=True)   # certificate / project / submission / endorsement
    proof_url        = Column(Text, nullable=True)
    description      = Column(Text, nullable=True)
    verified         = Column(Boolean, default=False)
    verified_by      = Column(String(100), nullable=True)
    created_at       = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # ── Relationships ─────────────────────────────────────
    student_skill = relationship("StudentSkill", back_populates="proofs")

    def __repr__(self) -> str:
        return f"<SkillProof id={self.id} type={self.proof_type!r}>"


class Project(Base):
    __tablename__ = "projects"

    id            = Column(Integer, primary_key=True, index=True)
    student_id    = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    title         = Column(String(255), nullable=False)
    description   = Column(Text, nullable=True)
    repo_url      = Column(Text, nullable=True)
    live_url      = Column(Text, nullable=True)
    thumbnail_url = Column(Text, nullable=True)
    is_featured   = Column(Boolean, default=False)
    created_at    = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at    = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    # ── Relationships ─────────────────────────────────────
    student = relationship("Student", back_populates="projects")

    def __repr__(self) -> str:
        return f"<Project id={self.id} title={self.title!r}>"


class AIEmbedding(Base):
    """Stores pgvector embeddings for students, jobs, and problems."""
    __tablename__ = "ai_embeddings"

    id          = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String(50), nullable=False)          # 'student' | 'job' | 'problem'
    entity_id   = Column(Integer, nullable=False, index=True)
    embedding   = Column(Vector(settings.EMBEDDING_DIMENSION), nullable=True)
    model_name  = Column(String(100), default=settings.EMBEDDING_MODEL)
    created_at  = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at  = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<AIEmbedding entity_type={self.entity_type!r} entity_id={self.entity_id}>"
