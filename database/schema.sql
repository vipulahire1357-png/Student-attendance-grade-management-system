-- ============================================================
-- OnlyStudents Platform - PostgreSQL Schema
-- Requires: pgvector extension
-- ============================================================

-- Enable pgvector extension for AI embedding storage
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- STUDENTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS students (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    full_name       VARCHAR(255) NOT NULL,
    username        VARCHAR(100) UNIQUE NOT NULL,
    bio             TEXT,
    avatar_url      TEXT,
    university      VARCHAR(255),
    degree          VARCHAR(255),
    graduation_year INTEGER,
    github_url      TEXT,
    linkedin_url    TEXT,
    portfolio_url   TEXT,
    resume_url      TEXT,
    gpa             FLOAT,
    location        VARCHAR(255),
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- COMPANIES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS companies (
    id              SERIAL PRIMARY KEY,
    email           VARCHAR(255) UNIQUE NOT NULL,
    password_hash   TEXT NOT NULL,
    company_name    VARCHAR(255) NOT NULL,
    slug            VARCHAR(100) UNIQUE NOT NULL,
    description     TEXT,
    logo_url        TEXT,
    website_url     TEXT,
    industry        VARCHAR(255),
    size            VARCHAR(50),   -- e.g. "1-10", "11-50", "51-200", "201-500", "500+"
    founded_year    INTEGER,
    headquarters    VARCHAR(255),
    linkedin_url    TEXT,
    is_active       BOOLEAN DEFAULT TRUE,
    is_verified     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SKILLS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS skills (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) UNIQUE NOT NULL,
    category    VARCHAR(100),   -- e.g. "programming", "design", "soft-skills"
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- STUDENT SKILLS (Many-to-Many)
-- ============================================================
CREATE TABLE IF NOT EXISTS student_skills (
    id          SERIAL PRIMARY KEY,
    student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    skill_id    INTEGER NOT NULL REFERENCES skills(id) ON DELETE CASCADE,
    proficiency VARCHAR(50) DEFAULT 'beginner',  -- beginner / intermediate / advanced / expert
    verified    BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (student_id, skill_id)
);

-- ============================================================
-- LEARNING PATHS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS learning_paths (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    difficulty      VARCHAR(50),   -- beginner / intermediate / advanced
    estimated_hours INTEGER,
    target_skill_id INTEGER REFERENCES skills(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- LEARNING MODULES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS learning_modules (
    id              SERIAL PRIMARY KEY,
    path_id         INTEGER NOT NULL REFERENCES learning_paths(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    content         TEXT,
    resource_url    TEXT,
    order_index     INTEGER NOT NULL DEFAULT 0,
    duration_mins   INTEGER,
    module_type     VARCHAR(50),  -- video / article / quiz / project
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- JOBS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS jobs (
    id              SERIAL PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    description     TEXT NOT NULL,
    requirements    TEXT,
    responsibilities TEXT,
    job_type        VARCHAR(50),   -- full-time / part-time / internship / contract / remote
    location        VARCHAR(255),
    remote_allowed  BOOLEAN DEFAULT FALSE,
    salary_min      NUMERIC(12, 2),
    salary_max      NUMERIC(12, 2),
    currency        VARCHAR(10) DEFAULT 'USD',
    experience_level VARCHAR(50),  -- entry / mid / senior / lead
    is_active       BOOLEAN DEFAULT TRUE,
    expires_at      TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- APPLICATIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS applications (
    id              SERIAL PRIMARY KEY,
    job_id          INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    student_id      INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    cover_letter    TEXT,
    resume_url      TEXT,
    status          VARCHAR(50) DEFAULT 'pending',  -- pending / reviewed / shortlisted / rejected / hired
    ai_match_score  FLOAT,
    notes           TEXT,
    applied_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (job_id, student_id)
);

-- ============================================================
-- PROJECTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS projects (
    id              SERIAL PRIMARY KEY,
    student_id      INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    description     TEXT,
    tech_stack      TEXT[],
    repo_url        TEXT,
    live_url        TEXT,
    thumbnail_url   TEXT,
    is_featured     BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- SKILL PROOFS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS skill_proofs (
    id              SERIAL PRIMARY KEY,
    student_skill_id INTEGER NOT NULL REFERENCES student_skills(id) ON DELETE CASCADE,
    proof_type      VARCHAR(50),   -- certificate / project / submission / endorsement
    proof_url       TEXT,
    description     TEXT,
    verified        BOOLEAN DEFAULT FALSE,
    verified_by     VARCHAR(100),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- INDUSTRY PROBLEMS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS industry_problems (
    id              SERIAL PRIMARY KEY,
    company_id      INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    description     TEXT NOT NULL,
    problem_type    VARCHAR(100),  -- research / design / engineering / data / marketing
    difficulty      VARCHAR(50),   -- easy / medium / hard / expert
    reward          TEXT,          -- e.g. "Internship offer", "$500 prize"
    deadline        TIMESTAMPTZ,
    required_skills TEXT[],
    is_active       BOOLEAN DEFAULT TRUE,
    max_submissions INTEGER,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- PROBLEM SUBMISSIONS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS problem_submissions (
    id              SERIAL PRIMARY KEY,
    problem_id      INTEGER NOT NULL REFERENCES industry_problems(id) ON DELETE CASCADE,
    student_id      INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    solution_text   TEXT,
    solution_url    TEXT,         -- link to repo, doc, or file
    submission_type VARCHAR(50),  -- text / link / file
    status          VARCHAR(50) DEFAULT 'submitted',  -- submitted / under_review / accepted / rejected
    feedback        TEXT,
    score           FLOAT,
    submitted_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- AI EMBEDDINGS TABLE (pgvector)
-- ============================================================
CREATE TABLE IF NOT EXISTS ai_embeddings (
    id              SERIAL PRIMARY KEY,
    entity_type     VARCHAR(50) NOT NULL,   -- 'student' | 'job' | 'problem'
    entity_id       INTEGER NOT NULL,
    embedding       vector(384),            -- sentence-transformers/all-MiniLM-L6-v2 produces 384-dim
    model_name      VARCHAR(100) DEFAULT 'all-MiniLM-L6-v2',
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (entity_type, entity_id)
);

-- ============================================================
-- INDEXES
-- ============================================================

-- Embedding HNSW index for fast cosine similarity search
CREATE INDEX IF NOT EXISTS idx_embeddings_vector
    ON ai_embeddings USING hnsw (embedding vector_cosine_ops);

CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company_id);
CREATE INDEX IF NOT EXISTS idx_jobs_active ON jobs(is_active);
CREATE INDEX IF NOT EXISTS idx_applications_student ON applications(student_id);
CREATE INDEX IF NOT EXISTS idx_problems_company ON industry_problems(company_id);
CREATE INDEX IF NOT EXISTS idx_submissions_student ON problem_submissions(student_id);
CREATE INDEX IF NOT EXISTS idx_student_skills_student ON student_skills(student_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_entity ON ai_embeddings(entity_type, entity_id);

-- ============================================================
-- SEED: Default Skills
-- ============================================================
INSERT INTO skills (name, category) VALUES
    ('Python', 'programming'),
    ('JavaScript', 'programming'),
    ('TypeScript', 'programming'),
    ('React', 'frontend'),
    ('Next.js', 'frontend'),
    ('FastAPI', 'backend'),
    ('Node.js', 'backend'),
    ('PostgreSQL', 'database'),
    ('MongoDB', 'database'),
    ('Redis', 'database'),
    ('Docker', 'devops'),
    ('Kubernetes', 'devops'),
    ('Machine Learning', 'ai-ml'),
    ('Deep Learning', 'ai-ml'),
    ('NLP', 'ai-ml'),
    ('Data Science', 'data'),
    ('SQL', 'data'),
    ('UI/UX Design', 'design'),
    ('Figma', 'design'),
    ('Communication', 'soft-skills'),
    ('Leadership', 'soft-skills'),
    ('Problem Solving', 'soft-skills')
ON CONFLICT (name) DO NOTHING;
