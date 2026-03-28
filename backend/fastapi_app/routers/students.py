"""
Students Router — profile management, projects, skills, and learning paths.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas.student_schema import (
    StudentProfile, StudentUpdate, ProjectCreate, ProjectOut, AddSkill
)
from ..services import student_service
from ..routers.auth import get_current_student

router = APIRouter(prefix="/students", tags=["students"])


# ── GET /students/profile ─────────────────────────────────────────────────────
@router.get(
    "/profile",
    response_model=StudentProfile,
    summary="Get the authenticated student's full profile",
)
async def get_profile(
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Return the complete profile of the currently authenticated student."""
    return await student_service.get_student_by_id(db, current_student.id)


# ── PATCH /students/profile ───────────────────────────────────────────────────
@router.patch(
    "/profile",
    response_model=StudentProfile,
    summary="Update the authenticated student's profile",
)
async def update_profile(
    data: StudentUpdate,
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Partially update profile fields for the authenticated student."""
    return await student_service.update_student(db, current_student.id, data)


# ── POST /students/upload-project ─────────────────────────────────────────────
@router.post(
    "/upload-project",
    response_model=ProjectOut,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new project to the student's portfolio",
)
async def upload_project(
    data: ProjectCreate,
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Create a new portfolio project for the authenticated student."""
    return await student_service.add_project(db, current_student.id, data)


# ── GET /students/projects ────────────────────────────────────────────────────
@router.get(
    "/projects",
    response_model=List[ProjectOut],
    summary="List all projects for the authenticated student",
)
async def list_my_projects(
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Return all portfolio projects for the authenticated student."""
    student = await student_service.get_student_by_id(db, current_student.id)
    return student.projects


# ── POST /students/skills ─────────────────────────────────────────────────────
@router.post(
    "/skills",
    status_code=status.HTTP_201_CREATED,
    summary="Add a skill to the student's profile",
)
async def add_skill(
    data: AddSkill,
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Attach a skill (with proficiency level) to the authenticated student."""
    student_skill = await student_service.add_skill(db, current_student.id, data)
    return {
        "message": "Skill added successfully",
        "student_skill_id": student_skill.id,
        "skill_id": student_skill.skill_id,
        "proficiency": student_skill.proficiency,
    }


# ── GET /students/learning-paths ──────────────────────────────────────────────
@router.get(
    "/learning-paths",
    summary="Get personalised learning path recommendations",
)
async def get_learning_paths(
    current_student=Depends(get_current_student),
    db: AsyncSession = Depends(get_db),
):
    """Return a curated list of learning paths relevant to the student."""
    paths = await student_service.get_learning_paths(db)
    return {"student_id": current_student.id, "learning_paths": paths}


# ── GET /students/{student_id} (public) ───────────────────────────────────────
@router.get(
    "/{student_id}",
    response_model=StudentProfile,
    summary="Get a student's public profile by ID",
)
async def get_student_profile(
    student_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Publicly accessible student profile endpoint (used by companies)."""
    return await student_service.get_student_by_id(db, student_id)
