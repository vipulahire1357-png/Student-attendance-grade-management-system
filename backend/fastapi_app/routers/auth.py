"""
Auth Router — Student signup, Company signup, and unified login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from ..database import get_db
from ..schemas.student_schema import StudentSignup, StudentProfile
from ..schemas.company_schema import CompanySignup, CompanyProfile
from ..services import auth_service, student_service, company_service

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ── Response Schemas ───────────────────────────────────────────────────────────
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str


class LoginRequest(BaseModel):
    email: str
    password: str
    role: str   # 'student' | 'company'


# ── Dependency: Current Student ───────────────────────────────────────────────
async def get_current_student(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Extract and validate the student from the JWT bearer token."""
    try:
        subject, role = auth_service.get_subject_and_role(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if role != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student access required")
    student = await student_service.get_student_by_id(db, int(subject))
    if not student or not student.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Student account inactive")
    return student


# ── Dependency: Current Company ────────────────────────────────────────────────
async def get_current_company(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Extract and validate the company from the JWT bearer token."""
    try:
        subject, role = auth_service.get_subject_and_role(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if role != "company":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Company access required")
    company = await company_service.get_company_by_id(db, int(subject))
    if not company or not company.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Company account inactive")
    return company


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/student/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student account",
)
async def student_signup(
    data: StudentSignup,
    db: AsyncSession = Depends(get_db),
):
    student = await student_service.create_student(db, data)
    access_token = auth_service.create_access_token(str(student.id), role="student")
    refresh_token = auth_service.create_refresh_token(str(student.id), role="student")
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role="student")


@router.post(
    "/company/signup",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new company account",
)
async def company_signup(
    data: CompanySignup,
    db: AsyncSession = Depends(get_db),
):
    company = await company_service.create_company(db, data)
    access_token = auth_service.create_access_token(str(company.id), role="company")
    refresh_token = auth_service.create_refresh_token(str(company.id), role="company")
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role="company")


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login for students or companies",
)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    if data.role == "student":
        user = await student_service.get_student_by_email(db, data.email)
    elif data.role == "company":
        user = await company_service.get_company_by_email(db, data.email)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="role must be 'student' or 'company'")

    if not user or not auth_service.verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated")

    access_token = auth_service.create_access_token(str(user.id), role=data.role)
    refresh_token = auth_service.create_refresh_token(str(user.id), role=data.role)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, role=data.role)
