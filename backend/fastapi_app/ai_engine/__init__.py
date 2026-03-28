"""AI engine package."""
from .embeddings import generate_embedding, upsert_embedding, get_embedding
from .matcher import match_student_to_job, recommended_jobs_for_student

__all__ = [
    "generate_embedding",
    "upsert_embedding",
    "get_embedding",
    "match_student_to_job",
    "recommended_jobs_for_student",
]
