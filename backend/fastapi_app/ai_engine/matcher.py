"""
AI Engine — Cosine Similarity Matcher
Uses pgvector's <=> (cosine distance) operator to find top-K matching
jobs for a student or top-K students for a job.
"""
from __future__ import annotations

import logging
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from fastapi import HTTPException, status

from ..config import settings
from ..models.skill import AIEmbedding
from ..models.job import Job
from ..models.student import Student

logger = logging.getLogger(__name__)


# ── Types ─────────────────────────────────────────────────────────────────────
class MatchResult:
    """Container for a single match result."""

    def __init__(self, entity_id: int, score: float, meta: dict):
        self.entity_id = entity_id
        self.score = score    # cosine similarity [0, 1]
        self.meta = meta

    def to_dict(self) -> dict:
        return {"entity_id": self.entity_id, "score": round(self.score, 4), **self.meta}


# ── Core Matching Function ────────────────────────────────────────────────────
async def _cosine_matches(
    db: AsyncSession,
    query_vector: list[float],
    target_entity_type: str,
    top_k: int,
    min_score: float,
) -> List[dict]:
    """
    Perform a cosine similarity search using pgvector's <=> operator.

    Returns rows sorted by similarity (highest first) where similarity >= min_score.

    Note: pgvector's <=> returns *distance* (0 = identical, 2 = opposite).
    Similarity = 1 - distance.
    """
    # Build a raw SQL query using pgvector
    sql = text(
        """
        SELECT
            entity_id,
            1 - (embedding <=> CAST(:query_vec AS vector)) AS similarity
        FROM ai_embeddings
        WHERE entity_type = :entity_type
          AND 1 - (embedding <=> CAST(:query_vec AS vector)) >= :min_score
        ORDER BY similarity DESC
        LIMIT :top_k
        """
    )

    vector_str = "[" + ",".join(str(v) for v in query_vector) + "]"
    result = await db.execute(
        sql,
        {
            "query_vec": vector_str,
            "entity_type": target_entity_type,
            "min_score": min_score,
            "top_k": top_k,
        },
    )
    return [{"entity_id": row.entity_id, "similarity": float(row.similarity)} for row in result]


# ── Public API ────────────────────────────────────────────────────────────────
async def match_student_to_job(
    db: AsyncSession,
    student_id: int,
    job_id: int,
) -> dict:
    """
    Compute the cosine similarity score between a specific student and job.

    Returns:
        { student_id, job_id, score }
    """
    # Fetch embeddings
    s_result = await db.execute(
        select(AIEmbedding).where(
            AIEmbedding.entity_type == "student",
            AIEmbedding.entity_id == student_id,
        )
    )
    s_emb = s_result.scalar_one_or_none()
    if not s_emb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No embedding found for student {student_id}. Generate embeddings first.",
        )

    j_result = await db.execute(
        select(AIEmbedding).where(
            AIEmbedding.entity_type == "job",
            AIEmbedding.entity_id == job_id,
        )
    )
    j_emb = j_result.scalar_one_or_none()
    if not j_emb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No embedding found for job {job_id}. Generate embeddings first.",
        )

    # Cosine similarity via raw SQL (single pair)
    sql = text(
        """
        SELECT 1 - (
            CAST(:s_vec AS vector) <=> CAST(:j_vec AS vector)
        ) AS similarity
        """
    )
    s_vec_str = "[" + ",".join(str(v) for v in s_emb.embedding) + "]"
    j_vec_str = "[" + ",".join(str(v) for v in j_emb.embedding) + "]"

    result = await db.execute(sql, {"s_vec": s_vec_str, "j_vec": j_vec_str})
    row = result.fetchone()
    score = round(float(row.similarity), 4) if row else 0.0

    return {"student_id": student_id, "job_id": job_id, "score": score}


async def recommended_jobs_for_student(
    db: AsyncSession,
    student_id: int,
    top_k: int = None,
    min_score: float = None,
) -> List[dict]:
    """
    Return top-K recommended jobs for a student, ranked by cosine similarity.

    Args:
        student_id: The student to find recommendations for.
        top_k: Number of results (defaults to settings.MATCH_TOP_K).
        min_score: Minimum similarity threshold (defaults to settings.MATCH_THRESHOLD).

    Returns:
        List of dicts with job details and match scores, sorted by score desc.
    """
    top_k = top_k or settings.MATCH_TOP_K
    min_score = min_score if min_score is not None else settings.MATCH_THRESHOLD

    # Get student embedding
    s_result = await db.execute(
        select(AIEmbedding).where(
            AIEmbedding.entity_type == "student",
            AIEmbedding.entity_id == student_id,
        )
    )
    s_emb = s_result.scalar_one_or_none()
    if not s_emb:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No embedding found for student {student_id}. Please generate embeddings first.",
        )

    matches = await _cosine_matches(
        db=db,
        query_vector=s_emb.embedding,
        target_entity_type="job",
        top_k=top_k,
        min_score=min_score,
    )

    if not matches:
        return []

    # Fetch job details for matched IDs
    matched_job_ids = [m["entity_id"] for m in matches]
    score_map = {m["entity_id"]: m["similarity"] for m in matches}

    jobs_result = await db.execute(
        select(Job).where(Job.id.in_(matched_job_ids), Job.is_active == True)
    )
    jobs = {job.id: job for job in jobs_result.scalars().all()}

    recommendations = []
    for job_id, sim in sorted(score_map.items(), key=lambda x: -x[1]):
        job = jobs.get(job_id)
        if job:
            recommendations.append(
                {
                    "job_id": job.id,
                    "title": job.title,
                    "company_id": job.company_id,
                    "job_type": job.job_type,
                    "location": job.location,
                    "remote_allowed": job.remote_allowed,
                    "experience_level": job.experience_level,
                    "match_score": round(sim, 4),
                }
            )

    logger.info(
        "Recommended %d jobs for student_id=%d (min_score=%.2f)",
        len(recommendations),
        student_id,
        min_score,
    )
    return recommendations
