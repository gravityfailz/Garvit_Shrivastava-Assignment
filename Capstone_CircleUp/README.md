# CircleUp

A platform to discover and organize social activities — cricket matches,
cafe meetups, weekend trips, study groups, and more.

---

## Tech Stack

| Layer    | Technology                         |
| -------- | ---------------------------------- |
| Backend  | Python 3.12, FastAPI               |
| Frontend | HTML, CSS, Vanilla JavaScript      |
| Database | PostgreSQL 16                      |
| API Docs | Swagger / OpenAPI (auto-generated) |
| Auth     | JWT (Bearer token, see below)      |

---

## Authentication Strategy

**JWT (JSON Web Tokens)** are used for authentication.

- On login, the server returns a signed Bearer token.
- The frontend stores this in `localStorage` and sends it as
  `Authorization: Bearer <token>` on every request.
- On logout, the token's `jti` (unique JWT ID) is recorded in a
  `token_blacklist` table — giving real server-side invalidation.
- Protected endpoints return `401` (never a stack trace) if the token
  is missing, expired, or blacklisted.

---

## Prerequisites

- Python 3.10+
- PostgreSQL 14+ running locally
- `pip` / `pip3`

---

## Setup

### 1. Create the PostgreSQL database

```sql
CREATE DATABASE circleup;
```

### 2. Install backend dependencies

```bash
cd Capstone_CircleUp/backend
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL and SECRET_KEY
```

### 4. Create tables

```bash
python -m app.init_db
```

### 5. Start the API server

```bash
uvicorn app.main:app --reload
```

API is live at: http://localhost:8000  
Swagger docs: http://localhost:8000/docs  
ReDoc: http://localhost:8000/redoc

---

## Frontend

Open `frontend/index.html` in your browser, **or** run a simple HTTP
server from the `frontend/` directory:

```bash
cd Capstone_CircleUp/frontend
python -m http.server 3000
# Then open http://localhost:3000
```

---

## Running Tests

```bash
cd Capstone_CircleUp/backend
pytest
```

With coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

Tests use an in-memory SQLite database — no real PostgreSQL needed to run them.

---

## Database Schema

See `backend/schema.sql` for the complete, documented schema.

---

## API Endpoints (Week 1)

| Method | Endpoint                    | Auth | Description             |
| ------ | --------------------------- | ---- | ----------------------- |
| POST   | /api/auth/register          | No   | Create account          |
| POST   | /api/auth/login             | No   | Get JWT token           |
| POST   | /api/auth/logout            | Yes  | Invalidate token        |
| GET    | /api/users/me               | Yes  | View own profile        |
| PUT    | /api/users/me               | Yes  | Update own profile      |
| POST   | /api/activities             | Yes  | Create activity         |
| GET    | /api/activities             | Yes  | List all activities     |
| GET    | /api/activities/{id}        | Yes  | View activity detail    |
| PUT    | /api/activities/{id}        | Yes  | Edit activity (owner)   |
| POST   | /api/activities/{id}/cancel | Yes  | Cancel activity (owner) |
