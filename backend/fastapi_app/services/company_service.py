"""
Company Service — business logic for company-related operations.
"""
import re
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status

from ..models.company import Company
from ..schemas.company_schema import CompanySignup, CompanyUpdate
from ..services.auth_service import hash_password


def _slugify(name: str) -> str:
    """Convert company name to a URL-safe slug."""
    slug = name.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    return slug[:100]


async def create_company(db: AsyncSession, data: CompanySignup) -> Company:
    """Create and persist a new company account."""
    # Email uniqueness
    result = await db.execute(select(Company).where(Company.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A company with this email already exists.",
        )

    # Ensure unique slug
    base_slug = _slugify(data.company_name)
    slug = base_slug
    counter = 1
    while True:
        result = await db.execute(select(Company).where(Company.slug == slug))
        if not result.scalar_one_or_none():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    company = Company(
        email=data.email,
        password_hash=hash_password(data.password),
        company_name=data.company_name,
        slug=slug,
        industry=data.industry,
        website_url=data.website_url,
    )
    db.add(company)
    await db.flush()
    await db.refresh(company)
    return company


async def get_company_by_id(db: AsyncSession, company_id: int) -> Company:
    """Fetch a company by PK; raises 404 if not found."""
    result = await db.execute(select(Company).where(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found.")
    return company


async def get_company_by_email(db: AsyncSession, email: str) -> Optional[Company]:
    """Return a company by email, or None."""
    result = await db.execute(select(Company).where(Company.email == email))
    return result.scalar_one_or_none()


async def update_company(
    db: AsyncSession, company_id: int, data: CompanyUpdate
) -> Company:
    """Partially update company profile fields."""
    company = await get_company_by_id(db, company_id)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(company, field, value)
    await db.flush()
    await db.refresh(company)
    return company
