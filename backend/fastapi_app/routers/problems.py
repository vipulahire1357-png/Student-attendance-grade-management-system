"""
Problems Router — browsing industry problems and student solution submission.
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..schemas.problem_schema import ProblemOut, SubmissionCreate, SubmissionOut
from ..models.problem import IndustryProblem, ProblemSubmission
from ..routers.auth import get_current_student

router = APIRouter(prefix="/problems", tags=["problems"])


# ── GET /problems ─────────────────────────────────────────────────────────────
@router.get(
    "",
    response_model=List[ProblemOut],
    summary="Browse all active industry problems",
)
async def list_problems(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    difficulty: Optional[str] = Query(None, description="Filter: easy | medium | hard | expert"),
    problem_type: Optional[str] = Query(None, description="Filter by problem type"),
    db: AsyncSession = Depends(get_db),
):
    """
    Public endpoint — return paginated list of active industry problems posted by companies.
    """
    query = select(IndustryProblem).where(IndustryProblem.is_active == True)
    if difficulty:
        query = query.where(IndustryProblem.difficulty == difficulty)
    if problem_type:
        query = query.where(IndustryProblem.problem_type == problem_type)
    query = query.offset(skip).limit(limit).order_by(IndustryProblem.created_at.desc())

    result = await db.execute(query)
    return list(result.scalars().all())


# ── GET /problems/{problem_id} ────────────────────────────────────────────────
@router.get(
    "/{problem_id}",
    response_model=ProblemOut,
    summary="Get details of a specific industry problem",
)
async def get_problem(
    problem_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(IndustryProblem).where(IndustryProblem.id == problem_id)
    )
    problem = result.scalar_one_or_none()
    if not problem:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


# ── POST /students/submit-solution (student-scoped) ───────────────────────────
# NOTE: This endpoint lives under /problems so the router owns the full lifecycle.
@router.post(
    "/submit-solution",
    response_model=SubmissionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a solution to an industry problem (student only)",
)
async def submit_solution(
    data: SubmissionCreate,
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """
    Allow an authenticated student to submit a solution to an industry problem.
    Students can submit via text, URL link, or file URL reference.
    """
    # Verify problem exists and is active
    p_result = await db.execute(
        select(IndustryProblem).where(
            IndustryProblem.id == data.problem_id,
            IndustryProblem.is_active == True,
        )
    )
    problem = p_result.scalar_one_or_none()
    if not problem:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Problem not found or is no longer active.")

    submission = ProblemSubmission(
        problem_id=data.problem_id,
        student_id=current_student.id,
        solution_text=data.solution_text,
        solution_url=data.solution_url,
        submission_type=data.submission_type,
    )
    db.add(submission)
    await db.flush()
    await db.refresh(submission)
    return submission
