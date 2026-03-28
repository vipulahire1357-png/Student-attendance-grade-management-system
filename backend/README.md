# OnlyStudents — Backend

FastAPI-powered backend for the OnlyStudents platform. Provides JWT auth, student/company management, AI-based talent matching via pgvector cosine similarity, and industry problem challenges.

---

## Prerequisites

| Tool | Version |
|------|---------|
| Python | ≥ 3.11 |
| PostgreSQL | ≥ 15 with **pgvector** extension |
| Redis | ≥ 7 |

---

## Quick Start

### 1. Clone & enter the backend directory
```bash
cd backend
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
# Connect to PostgreSQL and run:
psql -U postgres -c "CREATE DATABASE onlystudents;"
psql -U postgres -d onlystudents -f ../database/schema.sql
```

> **pgvector** must be installed in your PostgreSQL instance.  
> Install guide: https://github.com/pgvector/pgvector

### 5. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your actual values
```

Generate a secure JWT secret key:
```bash
openssl rand -hex 32
```

### 6. Run the development server
```bash
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be live at **http://localhost:8000**

- Interactive docs (Swagger UI): http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health check: http://localhost:8000/health

---

## Project Structure

```
backend/
├── fastapi_app/
│   ├── main.py            # FastAPI app, CORS, routers, lifespan
│   ├── config.py          # Pydantic settings (reads from .env)
│   ├── database.py        # Async SQLAlchemy engine + session DI
│   │
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── student.py
│   │   ├── company.py
│   │   ├── job.py         # Job + Application
│   │   ├── problem.py     # IndustryProblem + ProblemSubmission
│   │   └── skill.py       # Skill, StudentSkill, SkillProof, Project, AIEmbedding
│   │
│   ├── schemas/           # Pydantic v2 request/response schemas
│   │   ├── student_schema.py
│   │   ├── company_schema.py
│   │   ├── job_schema.py
│   │   └── problem_schema.py
│   │
│   ├── routers/           # FastAPI route handlers
│   │   ├── auth.py        # POST /auth/student/signup, /company/signup, /login
│   │   ├── students.py    # GET /students/profile, POST /upload-project, etc.
│   │   ├── companies.py   # POST /companies/post-job, /post-problem, GET /candidates
│   │   ├── jobs.py        # GET /jobs
│   │   ├── applications.py# POST /applications, GET /applications/my
│   │   ├── problems.py    # GET /problems, POST /problems/submit-solution
│   │   └── ai_matching.py # POST /ai/match-student-job, GET /ai/recommended-jobs/{id}
│   │
│   ├── services/          # Business logic layer
│   │   ├── auth_service.py    # JWT + bcrypt
│   │   ├── student_service.py
│   │   ├── company_service.py
│   │   └── job_service.py
│   │
│   └── ai_engine/         # AI talent matching
│       ├── embeddings.py  # sentence-transformers + pgvector upsert
│       └── matcher.py     # cosine similarity queries via pgvector
│
├── requirements.txt
└── .env.example
```

---

## API Reference (Summary)

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/student/signup` | Register student |
| POST | `/auth/company/signup` | Register company |
| POST | `/auth/login` | Login (student or company) |

### Students
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/students/profile` | Student JWT |
| PATCH | `/students/profile` | Student JWT |
| POST | `/students/upload-project` | Student JWT |
| GET | `/students/projects` | Student JWT |
| POST | `/students/skills` | Student JWT |
| GET | `/students/learning-paths` | Student JWT |
| GET | `/students/{id}` | Public |

### Companies
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/companies/profile` | Company JWT |
| PATCH | `/companies/profile` | Company JWT |
| POST | `/companies/post-job` | Company JWT |
| POST | `/companies/post-problem` | Company JWT |
| GET | `/companies/candidates` | Company JWT |
| GET | `/companies/{id}` | Public |

### Jobs & Applications
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/jobs` | Public |
| GET | `/jobs/{id}` | Public |
| POST | `/applications` | Student JWT |
| GET | `/applications/my` | Student JWT |
| PATCH | `/applications/{id}/status` | Company JWT |

### Problems
| Method | Endpoint | Auth |
|--------|----------|------|
| GET | `/problems` | Public |
| GET | `/problems/{id}` | Public |
| POST | `/problems/submit-solution` | Student JWT |

### AI Matching
| Method | Endpoint | Auth |
|--------|----------|------|
| POST | `/ai/match-student-job` | Company JWT |
| GET | `/ai/recommended-jobs/{student_id}` | Public |
| POST | `/ai/embeddings/student/{id}` | Student JWT |
| POST | `/ai/embeddings/job/{id}` | Company JWT |

---

## AI Matching Flow

1. **Generate student embedding** → `POST /ai/embeddings/student/{student_id}`  
   Encodes the student's skills + bio using `sentence-transformers/all-MiniLM-L6-v2`.

2. **Generate job embedding** → `POST /ai/embeddings/job/{job_id}`  
   Encodes the job title + description + requirements.

3. **Get recommendations** → `GET /ai/recommended-jobs/{student_id}`  
   Runs a pgvector HNSW cosine similarity search and returns ranked jobs.

4. **Point match** → `POST /ai/match-student-job`  
   Returns an exact 0–1 score for a specific student–job pair.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | — | PostgreSQL asyncpg connection URL |
| `REDIS_URL` | `redis://localhost:6379/0` | Redis URL |
| `SECRET_KEY` | — | JWT signing secret (use `openssl rand -hex 32`) |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | sentence-transformers model name |
| `EMBEDDING_DIMENSION` | `384` | Vector dimension |
| `MATCH_TOP_K` | `10` | Default top-K for recommendations |
| `MATCH_THRESHOLD` | `0.5` | Minimum cosine similarity score |

See `.env.example` for the full list.
