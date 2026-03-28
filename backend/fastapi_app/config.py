"""
OnlyStudents Backend - Application Configuration
Reads environment variables from .env file.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # ── App ────────────────────────────────────────────────
    APP_NAME: str = "OnlyStudents API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # ── Database ───────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/onlystudents"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # ── Redis ──────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL_SECONDS: int = 300  # 5 minutes default

    # ── JWT ────────────────────────────────────────────────
    SECRET_KEY: str = "CHANGE_THIS_IN_PRODUCTION_USE_openssl_rand_-hex_32"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── CORS ───────────────────────────────────────────────
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",   # student website
        "http://localhost:3001",   # company website
        "http://localhost:8000",   # FastAPI docs
    ]

    # ── File Storage (S3) ─────────────────────────────────
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_S3_BUCKET: str = "onlystudents-uploads"
    AWS_S3_REGION: str = "ap-south-1"

    # ── AI Engine ─────────────────────────────────────────
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    MATCH_TOP_K: int = 10              # Top-K results for similarity search
    MATCH_THRESHOLD: float = 0.5       # Minimum cosine similarity score

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance (singleton)."""
    return Settings()


settings = get_settings()
