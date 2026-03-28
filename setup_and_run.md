# OnlyStudents — Setup and Run Guide

> **Who is this guide for?**
> This guide is written for beginners. You do not need to be an expert. Every command is explained clearly so you know exactly what it does and why.

---

## What You Will Be Running

You will start **four separate things** on your computer:

| # | What | Where it runs |
|---|---|---|
| 1 | **PostgreSQL database** | Runs in the background |
| 2 | **FastAPI backend server** | `http://localhost:8000` |
| 3 | **Student website** | `http://localhost:3000` |
| 4 | **Company website** | `http://localhost:3001` |

All four must be running at the same time for the platform to work.

---

## Section 1 — System Requirements

Before you start, you need to install the following programs on your computer. These are the tools the project depends on.

### 1.1 Node.js (version 18 or higher)

Node.js runs the two Next.js websites.

**Download:** https://nodejs.org — choose the **LTS** version.

After installing, open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and check it works:

```bash
node -v
```

You should see something like: `v20.11.0`

```bash
npm -v
```

You should see something like: `10.2.4`

> **What is a terminal?**
> On Windows: Press `Win + R`, type `cmd`, press Enter.
> On Mac: Press `Cmd + Space`, type `Terminal`, press Enter.

---

### 1.2 Python (version 3.11 or higher)

Python runs the backend server.

**Download:** https://www.python.org/downloads — choose Python **3.11** or newer.

> **Important for Windows users:** During installation, check the box that says **"Add Python to PATH"**. This is required.

After installing, check it works:

```bash
python --version
```

You should see something like: `Python 3.11.8`

Also check pip (Python's package manager) is installed:

```bash
pip --version
```

You should see something like: `pip 24.0`

---

### 1.3 PostgreSQL (version 15 or higher)

PostgreSQL is the database that stores all data.

**Download:** https://www.postgresql.org/download

When installing PostgreSQL, it will ask you to set a **password for the default user** (`postgres`). **Remember this password** — you will need it later.

After installing, check it works by opening a new terminal and typing:

```bash
psql --version
```

You should see something like: `psql (PostgreSQL) 15.6`

---

### 1.4 Redis

Redis is used by the backend for caching.

**On Mac (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**On Windows:**
Download the Windows installer from: https://github.com/tporadowski/redis/releases
Run the `.msi` installer and it will install Redis as a Windows service that starts automatically.

**On Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis
```

Check it works after installing:
```bash
redis-cli ping
```
You should see: `PONG`

---

### 1.5 Git (for cloning the project)

**Download:** https://git-scm.com/downloads

Check it works:
```bash
git --version
```

You should see something like: `git version 2.43.0`

---

### Summary Checklist

Before moving forward, confirm all of these work:

```bash
node -v          # Should show v18 or higher
npm -v           # Should show a version number
python --version # Should show 3.11 or higher
pip --version    # Should show a version number
psql --version   # Should show 15 or higher
redis-cli ping   # Should print PONG
git --version    # Should show a version number
```

---

## Section 2 — Download the Project

### Option A — If you already have the project folder

Skip to **Section 3**. The project is already on your computer.

### Option B — Clone from Git

If you received a Git repository URL, open a terminal and run:

```bash
git clone <your-repository-url> os-3
cd os-3
```

Replace `<your-repository-url>` with the actual URL of the repository.

After this command, you will have a folder called `os-3` with all the project files inside.

---

## Section 3 — Backend Setup

The backend is the brain of the application. It handles all the data, authentication, and AI matching.

### Step 3.1 — Navigate to the backend folder

```bash
cd backend
```

> **Tip:** The `cd` command means "change directory". It moves you into a folder.

### Step 3.2 — Create a virtual environment

A virtual environment is an isolated Python workspace. It prevents the project's dependencies from conflicting with other Python projects on your computer.

```bash
python -m venv venv
```

This creates a folder called `venv` inside the `backend` folder.

### Step 3.3 — Activate the virtual environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On Mac / Linux:**
```bash
source venv/bin/activate
```

After running this, you should see `(venv)` at the start of your terminal prompt. This means the virtual environment is active.

### Step 3.4 — Install Python dependencies

Now install all the libraries the backend needs:

```bash
pip install -r requirements.txt
```

> **This may take 2–5 minutes.** The biggest download is `sentence-transformers` (the AI library). It is about 500 MB. Please be patient.

You will see a lot of lines scrolling by — this is normal. Wait until it finishes and returns you to the prompt.

### Step 3.5 — Create the environment variables file

The backend needs to know things like your database password and a secret key. These are stored in a file called `.env`.

Copy the example file to create your own:

**On Windows (Command Prompt):**
```bash
copy .env.example .env
```

**On Mac / Linux:**
```bash
cp .env.example .env
```

Now open the `.env` file in any text editor (Notepad, VS Code, etc.) and fill in these important values:

```
# Change this to your PostgreSQL password
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/onlystudents

# Generate a secret key by running this command in a terminal:
#   openssl rand -hex 32
# Then paste the output here:
SECRET_KEY=paste_your_generated_key_here
```

> **How to generate a SECRET_KEY:**
> On Mac/Linux, run: `openssl rand -hex 32`
> On Windows, you can use an online generator like https://generate-secret.vercel.app/32
> Copy the result and paste it as the value of SECRET_KEY.

The rest of the `.env` values can stay as their defaults for local development.

### Step 3.6 — Start the backend server

Make sure you are still inside the `backend/` folder with the virtual environment active, then run:

```bash
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

**What this command means:**
- `uvicorn` — the web server program
- `fastapi_app.main:app` — points to the `app` object in `backend/fastapi_app/main.py`
- `--reload` — automatically restarts the server when you make code changes
- `--host 0.0.0.0` — makes it accessible from your browser
- `--port 8000` — runs on port 8000

**What you should see in the terminal:**

```
INFO     | OnlyStudents API starting up...
INFO     | Database tables verified / created.
INFO     | Application startup complete.
INFO     | Uvicorn running on http://0.0.0.0:8000
```

**Test it works:** Open your browser and go to: http://localhost:8000/health

You should see:
```json
{
  "status": "ok",
  "app": "OnlyStudents API",
  "version": "1.0.0",
  "environment": "development"
}
```

**View the API documentation:** http://localhost:8000/docs

This shows every available API endpoint with a form to test each one.

> **Keep this terminal window open.** The server must keep running while you use the application.

---

## Section 4 — Database Setup

The backend will automatically create the database tables when it starts (you will see this in the terminal). However, you first need to create the PostgreSQL database itself and enable the `pgvector` extension.

### Step 4.1 — Open the PostgreSQL command line

Open a **new terminal window** (keep the backend terminal open) and run:

```bash
psql -U postgres
```

It will ask for a password — enter the password you set when you installed PostgreSQL.

You should see a prompt like: `postgres=#`

### Step 4.2 — Create the database

At the `postgres=#` prompt, type:

```sql
CREATE DATABASE onlystudents;
```

Press Enter. You should see: `CREATE DATABASE`

### Step 4.3 — Connect to the new database

```sql
\c onlystudents
```

You should see: `You are now connected to database "onlystudents"`.

### Step 4.4 — Enable the pgvector extension

The AI matching engine needs the `pgvector` extension to store and search embedding vectors:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

You should see: `CREATE EXTENSION`

### Step 4.5 — Run the schema file

Now run the SQL schema to create all the tables and seed the default skill data.

First, exit psql:
```sql
\q
```

Then run the schema file from the terminal. Replace `path/to/os-3` with your actual project path:

**On Windows:**
```bash
psql -U postgres -d onlystudents -f path\to\os-3\database\schema.sql
```

**On Mac / Linux:**
```bash
psql -U postgres -d onlystudents -f /path/to/os-3/database/schema.sql
```

**Example (if your project is on the Desktop on Windows):**
```bash
psql -U postgres -d onlystudents -f "C:\Users\YourName\Desktop\os-3\database\schema.sql"
```

You will see a list of `CREATE TABLE`, `CREATE INDEX`, and `INSERT` messages. This is normal.

### Step 4.6 — Restart the backend server

Now restart the backend server (press `Ctrl + C` in the backend terminal, then run the `uvicorn` command again). The server will confirm the tables exist on startup.

---

## Section 5 — Run the Student Website

Open a **new terminal window**.

### Step 5.1 — Navigate to the student website folder

```bash
cd student-website
```

(Run this from inside the `os-3` project root folder.)

### Step 5.2 — Install JavaScript packages

```bash
npm install
```

This downloads all the JavaScript libraries the student website needs. It may take 1–2 minutes.

### Step 5.3 — Confirm the environment file exists

The `.env.local` file should already exist with this content:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If it does not exist, create it yourself using a text editor and paste that line in.

### Step 5.4 — Start the development server

```bash
npm run dev
```

**What you should see:**

```
  ▲ Next.js 16.2.1
  - Local:        http://localhost:3000
  - Ready in 2.1s
```

**Open in your browser:** http://localhost:3000

You will see the student-facing landing page of OnlyStudents.

> **Keep this terminal window open.** The student website must keep running.

---

## Section 6 — Run the Company Website

Open a **new terminal window**.

### Step 6.1 — Navigate to the company website folder

```bash
cd company-website
```

### Step 6.2 — Install JavaScript packages

```bash
npm install
```

### Step 6.3 — Confirm the environment file exists

The `.env.local` file should contain:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If it does not exist, create it yourself.

### Step 6.4 — Start the development server

The company website must run on port **3001** (not 3000, which the student site is using):

```bash
npm run dev -- -p 3001
```

**What you should see:**

```
  ▲ Next.js 15.3.0
  - Local:        http://localhost:3001
  - Ready in 2.3s
```

**Open in your browser:** http://localhost:3001

You will see the company-facing marketing and dashboard page.

> **Keep this terminal window open.** The company website must keep running.

---

## Section 7 — Testing the System

At this point you should have **four things running**:

| Service | URL | Terminal |
|---|---|---|
| Backend API | http://localhost:8000 | Terminal 1 |
| Student Website | http://localhost:3000 | Terminal 2 |
| Company Website | http://localhost:3001 | Terminal 3 |

### Test 1 — Register a Company

1. Open http://localhost:3001 in your browser
2. Click **"Get Started"** or **"Create Company Account"**
3. Fill in your company name, work email, password, and industry
4. Click **"Create Account"**
5. You should be taken to the **Company Dashboard**

### Test 2 — Post a Job

1. From the Company Dashboard, click **"Post a Job"** or the **Post Job** link in the navbar
2. Fill in a job title (e.g. `Junior Python Developer`), description, job type, and location
3. Click **"Post Job Listing"**
4. You should see a success message and the job appear on your dashboard

### Test 3 — Register a Student

1. Open a **new incognito/private browser tab** (so you stay logged in as the company in the other tab)
2. Go to http://localhost:3000
3. Click **"Sign Up"**
4. Fill in your name, username, email, password, and university
5. Click **"Create Account"**
6. You should be taken to the **Student Dashboard**

### Test 4 — Build a Student Profile

1. Navigate to your **Profile** page from the student dashboard
2. Add some skills (e.g. Python, FastAPI, PostgreSQL) with proficiency levels
3. Add a portfolio project with a title and description
4. Save your changes

### Test 5 — Generate AI Embeddings and Get Matched Jobs

This is the most important test — it activates the AI matching engine.

1. In the student website, find the **"Generate My AI Embedding"** button (or go to your profile and trigger it from there)
2. Alternatively, call the API directly using the Swagger docs at http://localhost:8000/docs:
   - Find `POST /ai/embeddings/student/{student_id}`
   - First get your student ID from `GET /students/profile`
   - Then call the embedding endpoint with your student ID

3. After generating the student embedding, go to the **Jobs** page in the student website — you should see AI-matched job recommendations with percentage scores

### Test 6 — Post an Industry Problem

1. Go back to the Company website (http://localhost:3001)
2. Click **"Post Problem"** in the navbar
3. Fill in a problem title, description, difficulty level, reward, and required skills
4. Click **"Publish Industry Challenge"**

### Test 7 — Submit a Solution

1. In the Student website, navigate to the **Problems** page
2. Find the problem the company posted
3. Click on it and submit a solution (text or URL)

### Test 8 — View Candidates with AI Score (Company)

1. In the Company website, click **"Candidates"** in the navbar
2. Select a job from the filter dropdown
3. You will see candidate cards
4. Click **"Run AI Match"** on any candidate card to see their AI similarity score for that specific job

---

## Section 8 — Common Errors and Fixes

### Error: "Connection refused" when starting the backend

**Cause:** PostgreSQL is not running.

**Fix on Mac:**
```bash
brew services start postgresql
```

**Fix on Windows:**
Open **Services** (search in start menu), find **PostgreSQL**, right-click, click Start.

**Fix on Linux:**
```bash
sudo systemctl start postgresql
```

---

### Error: "password authentication failed for user postgres"

**Cause:** The password in your `.env` file does not match your PostgreSQL password.

**Fix:** Open `backend/.env` and update this line with your correct password:
```
DATABASE_URL=postgresql+asyncpg://postgres:YOUR_CORRECT_PASSWORD@localhost:5432/onlystudents
```

---

### Error: "database onlystudents does not exist"

**Cause:** You have not created the database yet.

**Fix:** Follow Section 4.2 to create it:
```bash
psql -U postgres -c "CREATE DATABASE onlystudents;"
```

---

### Error: "extension vector does not exist"

**Cause:** The pgvector extension is not installed in PostgreSQL.

**Fix:** pgvector must be installed as a PostgreSQL extension. On some systems it comes pre-installed; on others you must install it separately.

**On Mac (Homebrew PostgreSQL):**
```bash
brew install pgvector
```

**On Ubuntu/Debian:**
```bash
sudo apt install postgresql-15-pgvector
```

Then run the SQL again:
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

---

### Error: "address already in use" when starting a server

**Cause:** Another program is already using that port.

**Fix:** Find out what is using the port and stop it.

**On Windows:**
```bash
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

**On Mac / Linux:**
```bash
lsof -i :8000
kill -9 <PID_NUMBER>
```

Replace `8000` with `3000` or `3001` depending on which port is blocked.

---

### Error: "Module not found" or "Cannot find module"

**Cause:** JavaScript packages have not been installed.

**Fix:** Run `npm install` inside the relevant website folder:
```bash
cd student-website
npm install

# or

cd company-website
npm install
```

---

### Error: "No embedding found for student X"

**Cause:** The AI matching endpoint was called before generating an embedding for that student.

**Fix:** Call the embedding generation endpoint first:
```
POST /ai/embeddings/student/{student_id}
```

You can do this through the Swagger UI at http://localhost:8000/docs (you need to be authenticated).

---

### Error: "NEXT_PUBLIC_API_URL is not defined" or API calls fail silently

**Cause:** The `.env.local` file is missing or incorrect.

**Fix:** Make sure the file exists in the correct location with the correct value.

For `student-website/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For `company-website/.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

After creating or editing these files, **restart the Next.js dev server** (Ctrl+C, then `npm run dev` again).

---

### Error: "redis.exceptions.ConnectionError"

**Cause:** Redis is not running.

**Fix:**

**On Mac:**
```bash
brew services start redis
```

**On Windows:**
Open Services (Win+R, type `services.msc`), find **Redis**, right-click, Start.

**On Linux:**
```bash
sudo systemctl start redis
```

---

## Section 9 — How to Deploy (Host Online)

Once the project is working locally, you can make it available on the internet. Here is the simplest beginner-friendly way to deploy each part.

### Deploy the Frontends — Vercel (Free)

Vercel is a hosting platform made by the same team that builds Next.js. It is very easy to use.

**Steps:**

1. Go to https://vercel.com and create a free account (sign up with GitHub is easiest)
2. Click **"Add New → Project"**
3. Import your repository from GitHub
4. **For the Student Website:**
   - Set the **Root Directory** to `student-website`
   - Add environment variable: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.com` (you will get this after deploying the backend)
   - Click **Deploy**
5. **Repeat** the same steps for the Company Website, but set the Root Directory to `company-website`

Vercel gives you a free `.vercel.app` URL for each deployment (e.g. `student-website.vercel.app`).

---

### Deploy the Backend — Render (Free Tier)

Render is a cloud platform that can run Python web servers.

**Steps:**

1. Go to https://render.com and create a free account
2. Click **"New → Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn fastapi_app.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables from your `.env` file in the Render dashboard under **Environment**
6. Click **Create Web Service**

Render gives you a free URL like `https://onlystudents-backend.onrender.com`.

> **Note:** Free Render services sleep after 15 minutes of inactivity and take ~30 seconds to wake up on first request. Upgrade to a paid plan for production use.

---

### Deploy the Database — Neon (Free PostgreSQL with pgvector)

Neon is a cloud PostgreSQL database that includes pgvector support on the free tier.

**Steps:**

1. Go to https://neon.tech and create a free account
2. Create a new project — choose a region close to your users
3. Neon gives you a connection string like:
   ```
   postgresql://user:password@host.neon.tech/dbname?sslmode=require
   ```
4. For the FastAPI backend, you need the `asyncpg` version:
   ```
   postgresql+asyncpg://user:password@host.neon.tech/dbname?ssl=require
   ```
5. Set this as your `DATABASE_URL` environment variable in Render
6. Run the schema by going to **Neon's SQL Editor** in the dashboard and pasting the contents of `database/schema.sql`

The `vector` extension is already enabled by default on Neon.

---

### Update Frontend URLs After Deploying

Once your backend is deployed on Render:

1. Go to your Vercel deployments
2. In the project settings, find **Environment Variables**
3. Update `NEXT_PUBLIC_API_URL` to your Render backend URL (e.g. `https://onlystudents-backend.onrender.com`)
4. Redeploy (Vercel will redeploy automatically when you save environment variable changes)

---

### Update CORS Settings for Production

When deploying, update `ALLOWED_ORIGINS` in the backend `.env` / Render environment variables to include your deployed frontend URLs:

```
ALLOWED_ORIGINS=["https://student-website.vercel.app","https://company-website.vercel.app"]
```

---

## Quick Reference — All Commands

### Start Everything Locally

Open **3 separate terminal windows** and run one command in each:

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate    # Mac/Linux
# OR
venv\Scripts\activate       # Windows
uvicorn fastapi_app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Student Website:**
```bash
cd student-website
npm run dev
```

**Terminal 3 — Company Website:**
```bash
cd company-website
npm run dev -- -p 3001
```

### Access Points

| What | URL |
|---|---|
| Student Website | http://localhost:3000 |
| Company Website | http://localhost:3001 |
| Backend API | http://localhost:8000 |
| API Swagger Docs | http://localhost:8000/docs |
| API Health Check | http://localhost:8000/health |

---

*If you run into any problems not covered here, check the `backend/README.md` for additional backend-specific notes.*
