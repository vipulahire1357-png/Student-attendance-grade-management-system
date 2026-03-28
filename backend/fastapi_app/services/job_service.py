"""
Job Service — business logic for job postings and applications.
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status

from ..models.job import Job, Application
from ..models.student import Student
from ..schemas.job_schema import JobCreate, ApplicationCreate


async def create_job(
    db: AsyncSession, company_id: int, data: JobCreate
) -> Job:
    """Create a new job posting for a company."""
    job = Job(
        company_id=company_id,
        title=data.title,
        description=data.description,
        requirements=data.requirements,
        responsibilities=data.responsibilities,
        job_type=data.job_type,
        location=data.location,
        remote_allowed=data.remote_allowed,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        currency=data.currency,
        experience_level=data.experience_level,
        expires_at=data.expires_at,
    )
    db.add(job)
    await db.flush()
    await db.refresh(job)
    return job


async def get_job_by_id(db: AsyncSession, job_id: int) -> Job:
    """Fetch a job posting by PK; raises 404 if not found."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found.")
    return job


async def list_active_jobs(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 20,
    job_type: Optional[str] = None,
    location: Optional[str] = None,
) -> List[Job]:
    """Return paginated list of active job postings with optional filters."""
    query = select(Job).where(Job.is_active == True)
    if job_type:
        query = query.where(Job.job_type == job_type)
    if location:
        query = query.where(Job.location.ilike(f"%{location}%"))
    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def apply_to_job(
    db: AsyncSession, student_id: int, data: ApplicationCreate
) -> Application:
    """Submit a student's application to a job."""
    # Ensure job exists
    await get_job_by_id(db, data.job_id)

    # Check for duplicate application
    result = await db.execute(
        select(Application).where(
            Application.job_id == data.job_id,
            Application.student_id == student_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied to this job.",
        )

    application = Application(
        job_id=data.job_id,
        student_id=student_id,
        cover_letter=data.cover_letter,
        resume_url=data.resume_url,
    )
    db.add(application)
    await db.flush()
    await db.refresh(application)
    return application


async def get_company_candidates(
    db: AsyncSession,
    company_id: int,
    job_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 50,
) -> List[dict]:
    """
    Return candidate list for a company's jobs.
    Optionally filtered by a specific job.
    """
    query = (
        select(Application, Student)
        .join(Student, Application.student_id == Student.id)
        .join(Job, Application.job_id == Job.id)
        .where(Job.company_id == company_id)
    )
    if job_id:
        query = query.where(Application.job_id == job_id)
    query = query.offset(skip).limit(limit).order_by(Application.applied_at.desc())
    result = await db.execute(query)

    candidates = []
    for application, student in result.all():
        candidates.append({
            "application_id": application.id,
            "student_id": student.id,
            "full_name": student.full_name,
            "email": student.email,
            "university": student.university,
            "degree": student.degree,
            "ai_match_score": application.ai_match_score,
            "status": application.status,
            "applied_at": application.applied_at,
        })
    return candidates
