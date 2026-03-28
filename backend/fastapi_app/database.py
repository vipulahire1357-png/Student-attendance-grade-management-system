"""
OnlyStudents Backend - Async Database Engine & Session Factory
Uses SQLAlchemy 2.0 async engine backed by asyncpg (PostgreSQL).
"""
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator

from .config import settings


# ── SQLAlchemy Async Engine ──────────────────────────────────────────────────
engine: AsyncEngine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# ── Session Factory ──────────────────────────────────────────────────────────
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# ── Declarative Base ─────────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """All ORM models inherit from this base."""
    pass


# ── Dependency Injection ──────────────────────────────────────────────────────
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields a database session per request and
    rolls back / closes it automatically on completion or error.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ── DB Lifecycle Helpers ──────────────────────────────────────────────────────
async def create_all_tables() -> None:
    """Create all tables (for development / first-run use only)."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def dispose_engine() -> None:
    """Dispose of the engine connection pool (called on app shutdown)."""
    await engine.dispose()
