# Todo App FastAPI

Task management application built with FastAPI, PostgreSQL and JWT authentication.

## System Requirements

- Python 3.8+
- PostgreSQL
- UV package manager

## Installation

### 1. Install UV and setup project

```bash
# From project root directory
# Install UV
pip install uv

# Install dependencies and add virtual environment
uv sync
```

### 2. Database Setup

Create PostgreSQL database:
```sql
CREATE DATABASE todoapp;
CREATE USER todouser WITH PASSWORD 'todopass';
GRANT ALL PRIVILEGES ON DATABASE todoapp TO todouser;
```

### 3. Environment Variables

Copy `.env.example` to `.env` and update:
```bash
DATABASE_URL=postgresql://todouser:todopass@localhost/todoapp
SECRET_KEY=your-super-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Run Migrations

```bash
# From project root directory
cd app/
uv run alembic upgrade head
```

### 5. Start Server

```bash
# From project root directory
uv run fastapi dev
```

Server will run at: http://localhost:8000

## API Documentation

Access Swagger UI at: http://localhost:8000/docs

## Sample Accounts

After running migrations, you can login with:

**Admin:**
- Username: `admin`
- Password: `secret`

**Regular Users:**
- Username: `john_doe` 
- Password: `secret`
- Username: `jane_smith`
- Password: `secret`

## Main API Endpoints

### Authentication
- `POST /token` - Login and get JWT token

### Users
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/users/` - Get users list (requires authentication)

### Companies
- `POST /api/v1/companies/` - Create new company
- `GET /api/v1/companies/` - Get companies list
- `GET /api/v1/companies/{id}` - Get company info

### Tasks
- `POST /api/v1/tasks/` - Create new task
- `GET /api/v1/tasks/` - Get user's tasks list
- `GET /api/v1/tasks/{id}` - Get task info
- `PUT /api/v1/tasks/{id}` - Update task
- `PATCH /api/v1/tasks/{id}/status` - Update task status

## Project Structure

```
app/
├── alembic/           # Database migrations
├── models/            # SQLAlchemy models
├── routers/           # API routes
├── schemas/           # Pydantic schemas
├── auth.py           # JWT authentication
├── database.py       # Database configuration
└── main.py           # FastAPI app
```

## Troubleshooting

### Migration Errors
If you encounter errors when running `alembic upgrade head`, check:
1. Database has been created
2. Connection info in `.env` is correct
3. PostgreSQL service is running