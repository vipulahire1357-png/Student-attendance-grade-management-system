"""
OnlyStudents — FastAPI Application Entry Point

Registers all routers, CORS middleware, lifespan events,
global exception handlers, and health-check endpoint.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from dotenv import load_dotenv
import os

load_dotenv()

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .config import settings
from .database import create_all_tables, dispose_engine

# ── Routers ───────────────────────────────────────────────────────────────────
from .routers.auth import router as auth_router
from .routers.students import router as students_router
from .routers.companies import router as companies_router
from .routers.jobs import router as jobs_router
from .routers.applications import router as applications_router
from .routers.problems import router as problems_router
from .routers.ai_matching import router as ai_router

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run startup tasks before yielding, then shutdown tasks after."""
    logger.info("🚀 OnlyStudents API starting up...")

    # Create tables if they don't exist (use Alembic migrations in production)
    await create_all_tables()
    logger.info("✅ Database tables verified / created.")

    yield  # ── application is running ──

    logger.info("🛑 OnlyStudents API shutting down...")
    await dispose_engine()
    logger.info("✅ Database engine disposed.")


# ── FastAPI App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "**OnlyStudents** — The AI-powered Student–Industry Matching Platform.\n\n"
        "Connects students with companies through skill-based matching, "
        "real-world industry problems, and AI-driven job recommendations."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# ── CORS Middleware ───────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global Exception Handlers ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get(
    "/health",
    tags=["system"],
    summary="Health check — confirms the API is alive",
)
async def health_check() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", tags=["system"], summary="Root — redirect hint")
async def root() -> dict:
    return {
        "message": f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}",
        "docs": "/docs",
        "health": "/health",
    }


# ── Register All Routers ──────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(students_router)
app.include_router(companies_router)
app.include_router(jobs_router)
app.include_router(applications_router)
app.include_router(problems_router)
app.include_router(ai_router)

logger.info(
    "Registered routers: auth, students, companies, jobs, applications, problems, ai_matching"
)
