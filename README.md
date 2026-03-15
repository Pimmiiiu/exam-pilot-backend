# ExamPilot Backend

A production-ready FastAPI backend for an online exam platform with AI-powered explanations, leaderboard, and analytics.

## Features

- **Authentication**: JWT-based register/login with role-based access (student/admin)
- **Exam Management**: Browse exams, view questions with choices
- **Exam Submission**: Submit answers, auto-scoring
- **Results & AI Explanations**: Detailed results with AI-generated explanations for wrong answers (OpenAI-compatible)
- **Leaderboard**: Real-time score rankings
- **Analytics**: Per-user progress tracking, weak topic detection
- **Admin**: Create exams/questions, bulk import via CSV

## Tech Stack

- **FastAPI** 0.115 + **Pydantic** v2
- **SQLAlchemy** 2.0 + **Alembic** migrations
- **PostgreSQL** (via psycopg2-binary)
- **Redis** for caching AI explanations
- **python-jose** for JWT, **passlib/bcrypt** for passwords
- **httpx** for async LLM API calls

## Quick Start

### Using Docker Compose

```bash
cp .env.example .env
# Edit .env with your secrets
docker compose -f docker/docker-compose.yml up --build
```

### Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up PostgreSQL and Redis, then:
cp .env.example .env
# Edit .env

alembic upgrade head
uvicorn main:app --reload
```

API docs available at http://localhost:8000/docs

## Project Structure

```
app/
  api/          # FastAPI routers
  core/         # Config, JWT, security, dependencies
  domain/       # Entities and repository interfaces (clean architecture)
  usecases/     # Business logic
  infrastructure/ # DB models, repository impls, Redis, LLM client
  schemas/      # Pydantic request/response models
main.py         # App entry point
alembic/        # DB migrations
docker/         # Dockerfile and docker-compose
```

## Environment Variables

See `.env.example` for all required variables.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login, get tokens |
| GET | /auth/me | Current user info |
| GET | /exams | List all exams |
| GET | /exams/{id} | Exam detail with questions |
| POST | /exams/submit | Submit exam answers |
| GET | /results/{attempt_id} | Get attempt result |
| GET | /leaderboard | Top scorers |
| GET | /users/progress | User analytics |
| POST | /admin/exams | Create exam (admin) |
| POST | /admin/questions | Add question (admin) |
| POST | /admin/questions/import | Bulk import CSV (admin) |
| GET | /health | Health check |
