"""
Auth Service — JWT token creation, verification, and password hashing.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config import settings

# ── Password Hashing ─────────────────────────────────────────────────────────
_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    """Return bcrypt hash of the plain-text password."""
    return _pwd_context.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    """Return True if plain matches the stored hash."""
    return _pwd_context.verify(plain, hashed)


# ── JWT Helpers ───────────────────────────────────────────────────────────────
def create_access_token(
    subject: str,
    role: str,
    expires_delta: Optional[timedelta] = None,
) -> str:
    """
    Create a signed JWT access token.

    Args:
        subject: Unique identifier (e.g. str(user.id)).
        role: 'student' | 'company'.
        expires_delta: Custom TTL; falls back to settings default.
    """
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str, role: str) -> str:
    """Create a long-lived refresh token."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": subject,
        "role": role,
        "type": "refresh",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Decode and verify a JWT token.

    Raises:
        JWTError: If the token is invalid or expired.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def get_subject_and_role(token: str) -> tuple[str, str]:
    """
    Extract (subject, role) from a valid JWT token.

    Raises:
        JWTError: On invalid/expired token.
        ValueError: If required claims are missing.
    """
    payload = decode_token(token)
    sub: Optional[str] = payload.get("sub")
    role: Optional[str] = payload.get("role")
    if sub is None or role is None:
        raise ValueError("Token is missing required claims")
    return sub, role
