"""
AI Matching Router — generate embeddings, match students to jobs, and recommendations.

Endpoints:
  POST /ai/match-student-job       — compute cosine similarity between a student and job
  GET  /ai/recommended-jobs/{student_id} — top-K job recommendations for a student
  POST /ai/embeddings/student/{student_id} — generate/refresh student embedding
  POST /ai/embeddings/job/{job_id}         — generate/refresh job embedding
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel

from ..database import get_db
from ..ai_engine.embeddings import (
    upsert_embedding,
    build_student_text,
    build_job_text,
)
from ..ai_engine.matcher import match_student_to_job, recommended_jobs_for_student
from ..models.student import Student
from ..models.job import Job
from ..models.skill import StudentSkill, Skill
from ..routers.auth import get_current_student, get_current_company
from ..config import settings

router = APIRouter(prefix="/ai", tags=["ai-matching"])


# ── Request / Response Schemas ────────────────────────────────────────────────
class MatchRequest(BaseModel):
    student_id: int
    job_id: int


class MatchResponse(BaseModel):
    student_id: int
    job_id: int
    score: float


class EmbeddingResponse(BaseModel):
    entity_type: str
    entity_id: int
    model: str
    message: str


# ── POST /ai/match-student-job ────────────────────────────────────────────────
@router.post(
    "/match-student-job",
    response_model=MatchResponse,
    summary="Compute cosine similarity score between a student and a job",
)
async def match_student_job(
    data: MatchRequest,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_company),  # only companies can call this
):
    """
    Compute a 0–1 cosine similarity score between a student's skill embedding
    and a job's description embedding. Higher is better.
    Embeddings must have been generated beforehand.
    """
    result = await match_student_to_job(db, data.student_id, data.job_id)
    return MatchResponse(**result)


# ── GET /ai/recommended-jobs/{student_id} ─────────────────────────────────────
@router.get(
    "/recommended-jobs/{student_id}",
    summary="Get top-K recommended jobs for a student based on AI matching",
)
async def get_recommended_jobs(
    student_id: int,
    top_k: int = Query(default=10, ge=1, le=50, description="Number of recommendations"),
    min_score: float = Query(
        default=None,
        ge=0.0,
        le=1.0,
        description="Minimum similarity threshold (defaults to server setting)",
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Return top-K job recommendations for the specified student using
    pre-computed pgvector cosine similarity search.
    This endpoint is public so the student website can call it directly.
    """
    recommendations = await recommended_jobs_for_student(
        db,
        student_id=student_id,
        top_k=top_k,
        min_score=min_score,
    )
    return {
        "student_id": student_id,
        "total": len(recommendations),
        "recommendations": recommendations,
    }


# ── POST /ai/embeddings/student/{student_id} ──────────────────────────────────
@router.post(
    "/embeddings/student/{student_id}",
    response_model=EmbeddingResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate or refresh the embedding for a student",
)
async def generate_student_embedding(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_student),
):
    """
    Build a text representation of the student's skills and bio,
    then encode it with sentence-transformers and upsert into pgvector.
    """
    # Fetch student
    s_result = await db.execute(select(Student).where(Student.id == student_id))
    student = s_result.scalar_one_or_none()
    if not student:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Student not found")

    # Fetch skill names
    ss_result = await db.execute(
        select(Skill.name)
        .join(StudentSkill, StudentSkill.skill_id == Skill.id)
        .where(StudentSkill.student_id == student_id)
    )
    skill_names = [row[0] for row in ss_result.all()]

    text = build_student_text(
        skills=skill_names,
        bio=student.bio or "",
        location=student.location or "",
    )

    await upsert_embedding(db, entity_type="student", entity_id=student_id, text=text)

    return EmbeddingResponse(
        entity_type="student",
        entity_id=student_id,
        model=settings.EMBEDDING_MODEL,
        message="Student embedding generated and stored successfully.",
    )


# ── POST /ai/embeddings/job/{job_id} ──────────────────────────────────────────
@router.post(
    "/embeddings/job/{job_id}",
    response_model=EmbeddingResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate or refresh the embedding for a job posting",
)
async def generate_job_embedding(
    job_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_company),  # only the owning company can trigger this
):
    """
    Build a text representation of the job description and requirements,
    encode it, and upsert into pgvector ai_embeddings.
    """
    j_result = await db.execute(select(Job).where(Job.id == job_id))
    job = j_result.scalar_one_or_none()
    if not job:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Job not found")

    text = build_job_text(
        title=job.title,
        description=job.description,
        requirements=job.requirements or "",
        location=job.location or "",
    )

    await upsert_embedding(db, entity_type="job", entity_id=job_id, text=text)

    return EmbeddingResponse(
        entity_type="job",
        entity_id=job_id,
        model=settings.EMBEDDING_MODEL,
        message="Job embedding generated and stored successfully.",
    )
