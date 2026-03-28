"""
Companies Router — profile management, job posting, problem posting, and candidates.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.company_schema import CompanyProfile, CompanyUpdate
from ..schemas.job_schema import JobCreate, JobOut, CandidateOut
from ..schemas.problem_schema import ProblemCreate, ProblemOut
from ..services import company_service, job_service
from ..routers.auth import get_current_company
from ..models.problem import IndustryProblem

router = APIRouter(prefix="/companies", tags=["companies"])


# ── GET /companies/profile ────────────────────────────────────────────────────
@router.get(
    "/profile",
    response_model=CompanyProfile,
    summary="Get the authenticated company's profile",
)
async def get_company_profile(
    current_company=Depends(get_current_company),
    db: AsyncSession = Depends(get_db),
):
    return await company_service.get_company_by_id(db, current_company.id)


# ── PATCH /companies/profile ──────────────────────────────────────────────────
@router.patch(
    "/profile",
    response_model=CompanyProfile,
    summary="Update the authenticated company's profile",
)
async def update_company_profile(
    data: CompanyUpdate,
    current_company=Depends(get_current_company),
    db: AsyncSession = Depends(get_db),
):
    return await company_service.update_company(db, current_company.id, data)


# ── POST /companies/post-job ──────────────────────────────────────────────────
@router.post(
    "/post-job",
    response_model=JobOut,
    status_code=status.HTTP_201_CREATED,
    summary="Post a new job listing",
)
async def post_job(
    data: JobCreate,
    current_company=Depends(get_current_company),
    db: AsyncSession = Depends(get_db),
):
    """Create a new job posting associated with the authenticated company."""
    return await job_service.create_job(db, current_company.id, data)


# ── POST /companies/post-problem ──────────────────────────────────────────────
@router.post(
    "/post-problem",
    response_model=ProblemOut,
    status_code=status.HTTP_201_CREATED,
    summary="Post a real-world industry problem for students to solve",
)
async def post_problem(
    data: ProblemCreate,
    current_company=Depends(get_current_company),
    db: AsyncSession = Depends(get_db),
):
    """Create a new industry problem challenge for students."""
    problem = IndustryProblem(
        company_id=current_company.id,
        title=data.title,
        description=data.description,
        problem_type=data.problem_type,
        difficulty=data.difficulty,
        reward=data.reward,
        deadline=data.deadline,
        required_skills=data.required_skills,
        max_submissions=data.max_submissions,
    )
    db.add(problem)
    await db.flush()
    await db.refresh(problem)
    return problem


# ── GET /companies/candidates ─────────────────────────────────────────────────
@router.get(
    "/candidates",
    summary="List all candidates who applied for this company's jobs",
)
async def get_candidates(
    job_id: Optional[int] = Query(None, description="Filter by specific job ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_company=Depends(get_current_company),
    db: AsyncSession = Depends(get_db),
):
    """
    Return a paginated list of candidates for the authenticated company's jobs.
    Optionally filtered by job_id. Results include AI match scores.
    """
    candidates = await job_service.get_company_candidates(
        db,
        company_id=current_company.id,
        job_id=job_id,
        skip=skip,
        limit=limit,
    )
    return {
        "company_id": current_company.id,
        "total": len(candidates),
        "candidates": candidates,
    }


# ── GET /companies/{company_id} (public) ──────────────────────────────────────
@router.get(
    "/{company_id}",
    response_model=CompanyProfile,
    summary="Get a company's public profile",
)
async def get_public_company_profile(
    company_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await company_service.get_company_by_id(db, company_id)
