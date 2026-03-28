"""
Applications Router — students apply to jobs; companies update statuses.
"""
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..schemas.job_schema import ApplicationCreate, ApplicationOut
from ..services import job_service
from ..models.job import Application
from ..routers.auth import get_current_student, get_current_company

router = APIRouter(prefix="/applications", tags=["applications"])


# ── POST /applications ────────────────────────────────────────────────────────
@router.post(
    "",
    response_model=ApplicationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Apply to a job (student only)",
)
async def apply_to_job(
    data: ApplicationCreate,
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Submit a job application on behalf of the authenticated student."""
    return await job_service.apply_to_job(db, current_student.id, data)


# ── GET /applications/my ──────────────────────────────────────────────────────
@router.get(
    "/my",
    response_model=List[ApplicationOut],
    summary="List the authenticated student's applications",
)
async def my_applications(
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Return all job applications submitted by the authenticated student."""
    result = await db.execute(
        select(Application)
        .where(Application.student_id == current_student.id)
        .order_by(Application.applied_at.desc())
    )
    return list(result.scalars().all())


# ── PATCH /applications/{application_id}/status ───────────────────────────────
@router.patch(
    "/{application_id}/status",
    response_model=ApplicationOut,
    summary="Update application status (company only)",
)
async def update_application_status(
    application_id: int,
    new_status: str,
    current_company=Depends(get_current_company),
    db: AsyncSession = Depends(get_db),
):
    """
    Allow a company to update the status of an application for one of their jobs.
    Allowed values: pending | reviewed | shortlisted | rejected | hired
    """
    allowed_statuses = {"pending", "reviewed", "shortlisted", "rejected", "hired"}
    if new_status not in allowed_statuses:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"status must be one of {allowed_statuses}",
        )

    result = await db.execute(
        select(Application).where(Application.id == application_id)
    )
    application = result.scalar_one_or_none()
    if not application:
        from fastapi import HTTPException
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    application.status = new_status
    await db.flush()
    await db.refresh(application)
    return application
