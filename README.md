# Chat API Project

This is a test assignment for implementing a chat and messages API using FastAPI, SQLAlchemy, PostgreSQL, Alembic for migrations, pytest for tests, and Docker for containerization.

## Project Structure
- `app/`: Core application code (models, schemas, api routers, core config/database/logging).
- `tests/`: Unit and integration tests (api tests, cascade delete, concurrency, pagination).
- `alembic/`: Database migrations.
- `logs/`: Application logs (persistent, not committed to Git).
- `Dockerfile`: Multi-stage build for prod and test.
- `docker-compose.yml`: Services for db, api, and test.

## Requirements
- Docker and docker-compose.
- Poetry for local development (optional, as Docker handles deps).

## Quick Start for Reviewer
### 1. Run the Application (API + DB)
```bash
docker-compose up --build api db