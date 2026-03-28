"""
Jobs Router — browsing job listings and submitting applications.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.job_schema import JobOut, ApplicationCreate, ApplicationOut
from ..services import job_service
from ..routers.auth import get_current_student

router = APIRouter(prefix="/jobs", tags=["jobs"])


# ── GET /jobs ─────────────────────────────────────────────────────────────────
@router.get(
    "",
    response_model=List[JobOut],
    summary="Browse all active job listings",
)
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    job_type: Optional[str] = Query(None, description="Filter by job type"),
    location: Optional[str] = Query(None, description="Filter by location keyword"),
    db: AsyncSession = Depends(get_db),
):
    """
    Public endpoint — return paginated, filterable list of active job postings.
    No authentication required.
    """
    return await job_service.list_active_jobs(db, skip=skip, limit=limit, job_type=job_type, location=location)


# ── GET /jobs/{job_id} ────────────────────────────────────────────────────────
@router.get(
    "/{job_id}",
    response_model=JobOut,
    summary="Get a specific job listing by ID",
)
async def get_job(
    job_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await job_service.get_job_by_id(db, job_id)
