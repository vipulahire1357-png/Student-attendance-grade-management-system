"""
AI Engine — Embedding Generator
Uses sentence-transformers to produce dense vector embeddings for
students (skills text) and jobs (description text), then stores them
in the ai_embeddings table via pgvector.
"""
from __future__ import annotations

import logging
from typing import Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..config import settings
from ..models.skill import AIEmbedding

logger = logging.getLogger(__name__)

# ── Model singleton (lazy-loaded on first use) ────────────────────────────────
_model: Optional[SentenceTransformer] = None


def _get_model() -> SentenceTransformer:
    """Return (and lazily initialise) the embedding model."""
    global _model
    if _model is None:
        logger.info("Loading sentence-transformer model: %s", settings.EMBEDDING_MODEL)
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
        logger.info("Model loaded successfully.")
    return _model


# ── Embedding Generation ──────────────────────────────────────────────────────
def generate_embedding(text: str) -> list[float]:
    """
    Generate a normalised embedding vector for the given text.

    Args:
        text: The input text to embed.

    Returns:
        A list of floats (length == EMBEDDING_DIMENSION).
    """
    model = _get_model()
    embedding: np.ndarray = model.encode(
        text,
        normalize_embeddings=True,   # unit-norm for cosine similarity via dot product
        show_progress_bar=False,
    )
    return embedding.tolist()


def build_student_text(skills: list[str], bio: str = "", location: str = "") -> str:
    """
    Compose a representative text blob for a student to encode.
    The richer the text, the better the matching quality.
    """
    parts = []
    if bio:
        parts.append(bio)
    if skills:
        parts.append("Skills: " + ", ".join(skills))
    if location:
        parts.append(f"Location: {location}")
    return " | ".join(parts) if parts else "Student profile"


def build_job_text(
    title: str,
    description: str,
    requirements: str = "",
    location: str = "",
) -> str:
    """Compose a representative text blob for a job posting."""
    parts = [f"Job title: {title}", description]
    if requirements:
        parts.append(f"Requirements: {requirements}")
    if location:
        parts.append(f"Location: {location}")
    return " | ".join(parts)


# ── Persistence Helpers ───────────────────────────────────────────────────────
async def upsert_embedding(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
    text: str,
) -> AIEmbedding:
    """
    Generate an embedding for *text* and upsert it into ai_embeddings.

    Args:
        db: Async SQLAlchemy session.
        entity_type: 'student' | 'job' | 'problem'.
        entity_id: PK of the entity.
        text: Text to embed.

    Returns:
        The persisted AIEmbedding record.
    """
    vector = generate_embedding(text)

    result = await db.execute(
        select(AIEmbedding).where(
            AIEmbedding.entity_type == entity_type,
            AIEmbedding.entity_id == entity_id,
        )
    )
    record = result.scalar_one_or_none()

    if record:
        record.embedding = vector
        record.model_name = settings.EMBEDDING_MODEL
    else:
        record = AIEmbedding(
            entity_type=entity_type,
            entity_id=entity_id,
            embedding=vector,
            model_name=settings.EMBEDDING_MODEL,
        )
        db.add(record)

    await db.flush()
    await db.refresh(record)
    logger.info(
        "Upserted embedding for entity_type=%s entity_id=%d", entity_type, entity_id
    )
    return record


async def get_embedding(
    db: AsyncSession,
    entity_type: str,
    entity_id: int,
) -> Optional[list[float]]:
    """
    Retrieve a stored embedding vector, or None if not yet generated.
    """
    result = await db.execute(
        select(AIEmbedding).where(
            AIEmbedding.entity_type == entity_type,
            AIEmbedding.entity_id == entity_id,
        )
    )
    record = result.scalar_one_or_none()
    return record.embedding if record else None
