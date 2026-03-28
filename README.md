# OnlyStudents 🎓⚡

> **The AI-Powered Student–Industry Matching Platform**

OnlyStudents bridges the gap between talented students and forward-thinking companies by replacing traditional resume screening with **skill-verified profiles**, **real industry problem solving**, and **AI-driven semantic matching**.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Project Architecture](#2-project-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Folder Structure](#4-folder-structure)
5. [Core Features](#5-core-features)
6. [API Overview](#6-api-overview)
7. [Database Schema](#7-database-schema)
8. [AI Matching Engine](#8-ai-matching-engine)
9. [Environment Variables](#9-environment-variables)
10. [Future Improvements](#10-future-improvements)

---

## 1. Project Overview

The modern hiring process is broken. Companies wade through thousands of generic resumes while brilliant students — who lack traditional credentials — go unnoticed.

**OnlyStudents** solves this by building a two-sided platform:

| Side | Who | What they do |
|---|---|---|
| **Students** | University students, bootcamp grads, self-learners | Build verified skill profiles, solve real problems, get AI-matched to jobs |
| **Companies** | Startups, enterprises, research labs | Post jobs, post industry challenges, discover AI-ranked candidates |

### The Core Philosophy

- **Skill proof over diplomas** — Students prove skills by solving real problems, not just listing them.
- **Industry-driven education** — Companies post real challenges; students learn by doing.
- **AI talent matching** — A semantic AI engine matches students to roles based on meaning, not keywords.
- **Transparent scoring** — Every match comes with a 0–100% similarity score, shown to both parties.

---

## 2. Project Architecture

### System Architecture Diagram

```
+------------------------------------------------------------------+
|                           CLIENTS                                |
|                                                                  |
|   +----------------------+     +---------------------------+    |
|   |   Student Website    |     |    Company Website        |    |
|   |  Next.js  Port 3000  |     |  Next.js  Port 3001       |    |
|   +----------+-----------+     +-------------+-------------+    |
+--------------|--------------------------------|-------------------+
               |  HTTPS / Axios                |  HTTPS / Axios
               v                               v
+------------------------------------------------------------------+
|                  FastAPI Backend · Port 8000                     |
|                                                                  |
|  +----------+ +----------+ +----------+ +------------------+    |
|  |   Auth   | | Students | |Companies | | Jobs / Problems  |    |
|  |  Router  | |  Router  | |  Router  | |    Routers       |    |
|  +----------+ +----------+ +----------+ +------------------+    |
|                                                                  |
|  +-------------------------------------------------------------+ |
|  |              AI Matching Engine                             | |
|  |  sentence-transformers -> 384-dim embeddings -> pgvector   | |
|  +-------------------------------------------------------------+ |
+--------------------------------------+---------------------------+
                                       |  SQLAlchemy Async ORM
                                       v
+------------------------------------------------------------------+
|                   PostgreSQL Database                            |
|                                                                  |
|  students · companies · jobs · applications · skills             |
|  projects · industry_problems · problem_submissions              |
|  skill_proofs · learning_paths · ai_embeddings (pgvector)        |
+------------------------------------------------------------------+
                    |
                    v
          +------------------+
          |   Redis Cache    |
          |  Session / TTL   |
          +------------------+
```

### Component Roles

| Component | Technology | Port | Responsibility |
|---|---|---|---|
| **Backend API** | FastAPI (Python) | `8000` | REST API, authentication, business logic, AI engine |
| **Student Website** | Next.js 16 (TypeScript) | `3000` | Student dashboard, job board, problem solving, profile |
| **Company Website** | Next.js 15 (TypeScript) | `3001` | Company dashboard, job posting, candidate management |
| **Database** | PostgreSQL + pgvector | `5432` | Persistent data + 384-dim embedding vectors |
| **Cache** | Redis | `6379` | Session storage, query result caching |

---

## 3. Tech Stack

### Backend

| Technology | Version | Purpose |
|---|---|---|
| **FastAPI** | 0.111.0 | Async REST API framework |
| **Python** | 3.11+ | Backend language |
| **SQLAlchemy** | 2.0.30 | Async ORM for database access |
| **asyncpg** | 0.29.0 | Async PostgreSQL driver |
| **Alembic** | 1.13.1 | Database migrations |
| **Pydantic v2** | 2.7.1 | Data validation and settings |
| **python-jose** | 3.3.0 | JWT token creation and verification |
| **passlib[bcrypt]** | 1.7.4 | Password hashing |
| **Redis / aioredis** | 5.0.4 / 2.0.1 | Caching layer |
| **boto3** | 1.34.95 | AWS S3 file uploads |
| **Uvicorn** | 0.29.0 | ASGI server |

### AI Engine

| Technology | Version | Purpose |
|---|---|---|
| **sentence-transformers** | 2.7.0 | Generate 384-dim text embeddings |
| **all-MiniLM-L6-v2** | — | Embedding model (fast, high-quality) |
| **pgvector** | 0.2.5 | PostgreSQL vector similarity search |
| **NumPy** | 1.26.4 | Numerical operations on vectors |

### Student Website

| Technology | Version | Purpose |
|---|---|---|
| **Next.js** | 16.2.1 | React framework with App Router |
| **TypeScript** | 5+ | Type-safe JavaScript |
| **TailwindCSS** | 4+ | Utility-first CSS framework |
| **TanStack React Query** | 5.95.2 | Server state management and caching |
| **Axios** | 1.14.0 | HTTP client for API calls |
| **lucide-react** | — | Icon library |
| **clsx** | 2.1.1 | Conditional class name utility |

### Company Website

| Technology | Version | Purpose |
|---|---|---|
| **Next.js** | 15.3.0 | React framework with App Router |
| **TypeScript** | 5+ | Type-safe JavaScript |
| **TailwindCSS** | 3.4.1 | Utility-first CSS framework |
| **TanStack React Query** | 5.95.2 | Server state management |
| **Axios** | 1.14.0 | HTTP client for API calls |
| **react-hook-form** | 7.54.2 | Form state and validation |
| **recharts** | 2.15.0 | Data visualisation charts |
| **lucide-react** | — | Icon library |

### Database

| Technology | Purpose |
|---|---|
| **PostgreSQL** | Primary relational database |
| **pgvector extension** | Stores and queries 384-dim embedding vectors |
| **HNSW index** | Fast approximate nearest-neighbour vector search |

---

## 4. Folder Structure

```
os-3/
|
+-- backend/                        <- FastAPI REST API server
|   +-- fastapi_app/
|   |   +-- main.py                 <- App entry point; registers all routers
|   |   +-- config.py               <- Settings loaded from .env (pydantic-settings)
|   |   +-- database.py             <- Async SQLAlchemy engine + session factory
|   |   +-- models/                 <- SQLAlchemy ORM table definitions
|   |   |   +-- student.py          <- Student + Project models
|   |   |   +-- company.py          <- Company model
|   |   |   +-- job.py              <- Job + Application models
|   |   |   +-- problem.py          <- IndustryProblem + ProblemSubmission models
|   |   |   +-- skill.py            <- Skill + StudentSkill + AIEmbedding models
|   |   +-- schemas/                <- Pydantic request/response validation schemas
|   |   |   +-- student_schema.py
|   |   |   +-- company_schema.py
|   |   |   +-- job_schema.py
|   |   |   +-- problem_schema.py
|   |   +-- routers/                <- FastAPI route handlers (one file per domain)
|   |   |   +-- auth.py             <- POST /auth/student/signup, /auth/company/signup, /auth/login
|   |   |   +-- students.py         <- GET/PATCH /students/profile, skills, projects
|   |   |   +-- companies.py        <- GET/PATCH /companies/profile, post-job, post-problem
|   |   |   +-- jobs.py             <- GET /jobs (browse), GET /jobs/{id}
|   |   |   +-- applications.py     <- POST /applications, GET /applications/my
|   |   |   +-- problems.py         <- GET /problems, POST /problems/submit-solution
|   |   |   +-- ai_matching.py      <- POST /ai/match-student-job, GET /ai/recommended-jobs
|   |   +-- services/               <- Business logic layer (called by routers)
|   |   |   +-- auth_service.py     <- JWT creation, password hashing/verification
|   |   |   +-- student_service.py  <- CRUD for students, skills, projects, learning paths
|   |   |   +-- company_service.py  <- CRUD for companies
|   |   |   +-- job_service.py      <- Job creation, application handling, candidate listing
|   |   +-- ai_engine/              <- AI matching system
|   |       +-- embeddings.py       <- sentence-transformers encoding + pgvector upsert
|   |       +-- matcher.py          <- Cosine similarity search via pgvector <=> operator
|   +-- requirements.txt            <- All Python dependencies
|   +-- .env.example                <- Template for environment variables
|
+-- student-website/                <- Student-facing Next.js frontend (port 3000)
|   +-- app/
|   |   +-- page.tsx                <- Landing / home page
|   |   +-- login/page.tsx          <- Student login
|   |   +-- signup/page.tsx         <- Student registration
|   |   +-- dashboard/page.tsx      <- Student dashboard with AI job recommendations
|   |   +-- jobs/page.tsx           <- Browse all live job listings
|   |   +-- problems/page.tsx       <- Browse and solve industry problems
|   |   +-- profile/page.tsx        <- Student profile editor (skills, projects, bio)
|   |   +-- learning-paths/         <- Curated learning path browser
|   +-- components/                 <- Reusable React components
|   +-- services/                   <- Axios API client layer
|   +-- hooks/                      <- React Query custom hooks
|   +-- context/                    <- Auth context (JWT state management)
|   +-- .env.local                  <- NEXT_PUBLIC_API_URL=http://localhost:8000
|
+-- company-website/                <- Company-facing Next.js frontend (port 3001)
|   +-- app/
|   |   +-- page.tsx                <- Marketing landing page
|   |   +-- login/page.tsx          <- Company login
|   |   +-- signup/page.tsx         <- Company registration
|   |   +-- dashboard/page.tsx      <- Company dashboard (jobs, problems, stats)
|   |   +-- post-job/page.tsx       <- Job creation form
|   |   +-- post-problem/page.tsx   <- Industry challenge posting form
|   |   +-- candidates/page.tsx     <- Candidate browser with AI match scores
|   +-- components/
|   |   +-- Navbar.tsx
|   |   +-- JobForm.tsx             <- Reusable job posting form
|   |   +-- CandidateCard.tsx       <- Candidate card with AI score bar
|   +-- services/api.ts             <- Full typed Axios API client
|   +-- hooks/
|   |   +-- useCompany.ts           <- Company profile + candidates data hooks
|   |   +-- useCompanyAuth.ts       <- Login / signup / logout auth hooks
|   +-- context/AuthContext.tsx     <- Auth state + logout via React context
|   +-- .env.local                  <- NEXT_PUBLIC_API_URL=http://localhost:8000
|
+-- database/
    +-- schema.sql                  <- Complete PostgreSQL schema (run once to initialise)
```

---

## 5. Core Features

### Student Skill Proof System

Students build verified profiles that go beyond their resume:

- **Skill declarations** with proficiency levels (Beginner / Intermediate / Advanced / Expert)
- **Portfolio projects** — title, description, tech stack, GitHub and live links
- **Skill proofs** — attach certificates, project links, or submission evidence to each skill
- **Bio + university info** — all fed into the AI embedding for richer matching

### Real Industry Problems

Companies post real-world challenges instead of (or alongside) job listings:

- Challenges include a **difficulty rating**, **reward/prize**, **deadline**, and **required skills**
- Students submit solutions as text, links, or file references
- Submissions go through a review pipeline: `submitted → under_review → accepted / rejected`
- Companies can fast-track top solvers directly to interviews

### AI Talent Matching Engine

The heart of the platform — a semantic matching system built on vector embeddings:

1. **Embedding generation** — When a student saves their profile or a company posts a job, the system builds a rich text representation and encodes it using `sentence-transformers/all-MiniLM-L6-v2` into a 384-dimensional float vector.
2. **Storage** — Vectors are stored in the `ai_embeddings` table using the `pgvector` PostgreSQL extension.
3. **Similarity search** — When a company requests candidates, or a student requests job recommendations, the system runs a cosine similarity query using pgvector's `<=>` operator with an HNSW index for fast lookups.
4. **Scoring** — Each match returns a score from 0.0 to 1.0. The default threshold is **0.5** (50% similarity) and top-K defaults to **10** results.

### Job Board

- Companies post full job listings (title, description, requirements, responsibilities, salary, type, location, remote policy)
- Students browse and filter by job type and location
- Students apply with a cover letter and resume URL
- Application status flows: `pending → reviewed → shortlisted → rejected / hired`

### Learning Paths

- Curated learning paths mapped to specific skills
- Each path contains ordered learning modules (video / article / quiz / project)
- Students see paths relevant to the skills needed by their current matched jobs

---

## 6. API Overview

All endpoints are available at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

### Authentication — `/auth`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/student/signup` | None | Register a new student account |
| `POST` | `/auth/company/signup` | None | Register a new company account |
| `POST` | `/auth/login` | None | Login for students or companies — returns JWT tokens |

> All protected endpoints require `Authorization: Bearer <access_token>` header.

### Students — `/students`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/students/profile` | Student JWT | Get authenticated student's full profile |
| `PATCH` | `/students/profile` | Student JWT | Update bio, university, location, links |
| `POST` | `/students/upload-project` | Student JWT | Add a portfolio project |
| `GET` | `/students/projects` | Student JWT | List all portfolio projects |
| `POST` | `/students/skills` | Student JWT | Add a skill with proficiency level |
| `GET` | `/students/learning-paths` | Student JWT | Get personalised learning path recommendations |
| `GET` | `/students/{student_id}` | None | Public profile lookup by ID |

### Companies — `/companies`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/companies/profile` | Company JWT | Get authenticated company's profile |
| `PATCH` | `/companies/profile` | Company JWT | Update company details |
| `POST` | `/companies/post-job` | Company JWT | Create a new job listing |
| `POST` | `/companies/post-problem` | Company JWT | Post a real industry challenge |
| `GET` | `/companies/candidates` | Company JWT | List candidates for company's jobs |
| `GET` | `/companies/{company_id}` | None | Public company profile lookup |

### Jobs — `/jobs`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/jobs` | None | Browse active jobs (filter by type, location) |
| `GET` | `/jobs/{job_id}` | None | Get a specific job listing |

### Applications — `/applications`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/applications` | Student JWT | Apply to a job |
| `GET` | `/applications/my` | Student JWT | List student's own applications |
| `PATCH` | `/applications/{id}/status` | Company JWT | Update application status |

### Industry Problems — `/problems`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/problems` | None | Browse active industry problems |
| `GET` | `/problems/{problem_id}` | None | Get problem details |
| `POST` | `/problems/submit-solution` | Student JWT | Submit a solution to a problem |

### AI Matching — `/ai`

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/ai/match-student-job` | Company JWT | Cosine similarity score for a student–job pair |
| `GET` | `/ai/recommended-jobs/{student_id}` | None | Top-K job recommendations for a student |
| `POST` | `/ai/embeddings/student/{student_id}` | Student JWT | Generate/refresh student embedding |
| `POST` | `/ai/embeddings/job/{job_id}` | Company JWT | Generate/refresh job embedding |

---

## 7. Database Schema

The database has **12 tables** across 4 domains:

```
Users
  +-- students          (id, email, password_hash, full_name, username, bio, university ...)
  +-- companies         (id, email, password_hash, company_name, slug, industry ...)

Skills & Learning
  +-- skills            (id, name, category)
  +-- student_skills    (student_id, skill_id, proficiency, verified)
  +-- skill_proofs      (student_skill_id, proof_type, proof_url)
  +-- learning_paths    (id, title, difficulty, estimated_hours, target_skill_id)
  +-- learning_modules  (path_id, title, content, order_index, module_type)

Jobs & Applications
  +-- jobs              (company_id, title, description, job_type, salary_min, salary_max ...)
  +-- applications      (job_id, student_id, status, ai_match_score ...)
  +-- projects          (student_id, title, tech_stack[], repo_url, live_url ...)

Industry Problems
  +-- industry_problems    (company_id, title, difficulty, reward, deadline ...)
  +-- problem_submissions  (problem_id, student_id, solution_text, status, score ...)

AI
  +-- ai_embeddings     (entity_type, entity_id, embedding vector(384), model_name)
                         ^ HNSW index for fast cosine similarity via pgvector
```

---

## 8. AI Matching Engine

### How It Works — Step by Step

```
SETUP (one-time per entity):
   Student saves profile
        |
        v
   Build text blob:
   "Bio: {bio} | Skills: {skill1}, {skill2} | Location: {city}"
        |
        v
   sentence-transformers (all-MiniLM-L6-v2)
        |
        v
   384-dimensional float vector
        |
        v
   UPSERT into ai_embeddings table (pgvector)

MATCHING (on demand):
   Company requests: "Match student 42 to job 7"
        |
        v
   Fetch student vector  +  Fetch job vector
        |
        v
   Cosine similarity via pgvector <=> operator
        |
        v
   Score: 0.0 to 1.0  (e.g. 0.87 = 87% match)
        |
        v
   Return MatchResponse { student_id, job_id, score }

RECOMMENDATIONS (for students):
   Student requests: "Find me the best matching jobs"
        |
        v
   Fetch student vector
        |
        v
   pgvector HNSW index scan across all job vectors
        |
        v
   Return top-10 jobs sorted by similarity >= 0.5
```

### Embedding Model

- **Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimension**: 384 floats per vector
- **Type**: Bi-encoder (fast inference, no cross-attention overhead)
- **Normalised**: Yes — cosine similarity equals dot product on unit vectors

---

## 9. Environment Variables

### Backend (`backend/.env`)

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://postgres:password@localhost:5432/onlystudents` | PostgreSQL connection string |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection string |
| `SECRET_KEY` | *(must set)* | JWT signing secret — generate with `openssl rand -hex 32` |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | Access token lifetime (24 hours) |
| `REFRESH_TOKEN_EXPIRE_DAYS` | `30` | Refresh token lifetime |
| `ALLOWED_ORIGINS` | `["http://localhost:3000","http://localhost:3001"]` | CORS allowed frontend origins |
| `AWS_ACCESS_KEY_ID` | — | AWS credentials for S3 file uploads |
| `AWS_SECRET_ACCESS_KEY` | — | AWS credentials for S3 file uploads |
| `AWS_S3_BUCKET` | `onlystudents-uploads` | S3 bucket name |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | sentence-transformers model name |
| `EMBEDDING_DIMENSION` | `384` | Vector dimension (must match model) |
| `MATCH_TOP_K` | `10` | Max number of AI match results |
| `MATCH_THRESHOLD` | `0.5` | Minimum cosine similarity score |

### Student Website (`student-website/.env.local`)

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` |

### Company Website (`company-website/.env.local`)

| Variable | Value |
|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` |

---

## 10. Future Improvements

### Scalability
- **Horizontal scaling** — Deploy FastAPI behind a load balancer with multiple Uvicorn workers managed by Gunicorn.
- **Embedding background jobs** — Move embedding generation to a Celery/RQ task queue so it does not block HTTP requests.
- **Read replicas** — Add PostgreSQL read replicas for heavy query workloads.

### AI & Matching
- **Reranking** — Add a cross-encoder reranker on top of the bi-encoder for more precise final scores.
- **Incremental re-embedding** — Automatically trigger embedding regeneration when a student updates their profile.
- **Skill gap analysis** — Show students exactly which skills they are missing for each matched job.
- **Multi-modal matching** — Include portfolio project README text and GitHub activity in embeddings.

### Features
- **Real-time notifications** — WebSocket or SSE for new job matches and application status changes.
- **Video introductions** — Allow students to record a 60-second video that companies can review.
- **Company analytics dashboard** — Charts showing application funnel, match score distributions, and time-to-hire.
- **Endorsements** — Allow verified companies to endorse student skills after a successful hire.
- **Admin panel** — Moderation interface for verifying accounts and managing reported content.

### DevOps
- **Docker Compose** — Single `docker-compose up` command to start all four services locally.
- **GitHub Actions CI/CD** — Automated test, lint, and deploy pipeline on push.
- **Alembic migrations** — Replace `create_all_tables()` auto-create with proper versioned migrations.
- **Monitoring** — Integrate Sentry for error tracking and Prometheus/Grafana for metrics.

---

## License

MIT — feel free to fork, study, and build on top of this.

---

*Built with love for the future of fair, skill-based hiring.*
