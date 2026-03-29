"""
Student Service — business logic for student-related operations.
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload          # ← ADDED
from fastapi import HTTPException, status

from ..models.student import Student
from ..models.skill import Project, StudentSkill
from ..schemas.student_schema import StudentSignup, StudentUpdate, ProjectCreate, AddSkill
from ..services.auth_service import hash_password


async def create_student(db: AsyncSession, data: StudentSignup) -> Student:
    """Create and persist a new student account."""
    # Check email uniqueness
    result = await db.execute(select(Student).where(Student.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A student account with this email already exists.",
        )

    # Check username uniqueness
    result = await db.execute(select(Student).where(Student.username == data.username.lower()))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken.",
        )

    student = Student(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        username=data.username.lower().strip(),
        university=data.university,
        degree=data.degree,
        graduation_year=data.graduation_year,
    )
    db.add(student)
    await db.flush()
    await db.refresh(student)
    return student


async def get_student_by_id(db: AsyncSession, student_id: int) -> Student:
    """Fetch a student by PK with relationships; raises 404 if not found."""
    result = await db.execute(                   # ← UPDATED (added selectinload)
        select(Student)
        .options(
            selectinload(Student.projects),
            selectinload(Student.skills),
        )
        .where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found.")
    return student


async def get_student_by_email(db: AsyncSession, email: str) -> Optional[Student]:
    """Return a student by email, or None."""
    result = await db.execute(select(Student).where(Student.email == email))
    return result.scalar_one_or_none()


async def update_student(
    db: AsyncSession, student_id: int, data: StudentUpdate
) -> Student:
    """Partially update student profile fields."""
    student = await get_student_by_id(db, student_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    await db.flush()
    await db.refresh(student)
    return student


async def add_project(
    db: AsyncSession, student_id: int, data: ProjectCreate
) -> Project:
    """Add a new project to a student's portfolio."""
    project = Project(
        student_id=student_id,
        title=data.title,
        description=data.description,
        repo_url=data.repo_url,
        live_url=data.live_url,
        thumbnail_url=data.thumbnail_url,
        is_featured=data.is_featured,
    )
    db.add(project)
    await db.flush()
    await db.refresh(project)
    return project


async def add_skill(
    db: AsyncSession, student_id: int, data: AddSkill
) -> StudentSkill:
    """Add a skill to a student's profile."""
    # Check for duplicate
    result = await db.execute(
        select(StudentSkill).where(
            StudentSkill.student_id == student_id,
            StudentSkill.skill_id == data.skill_id,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Skill already added to profile.",
        )

    student_skill = StudentSkill(
        student_id=student_id,
        skill_id=data.skill_id,
        proficiency=data.proficiency,
    )
    db.add(student_skill)
    await db.flush()
    await db.refresh(student_skill)
    return student_skill


async def get_learning_paths(db: AsyncSession) -> List[dict]:
    """Return a simplified list of learning paths (stub — extend with LearningPath model)."""
    # TODO: implement full LearningPath ORM query once the model is added
    return [
        {"id": 1, "title": "Full-Stack with React & FastAPI", "difficulty": "intermediate"},
        {"id": 2, "title": "Machine Learning Fundamentals", "difficulty": "beginner"},
        {"id": 3, "title": "Cloud Engineering with AWS", "difficulty": "advanced"},
    ]