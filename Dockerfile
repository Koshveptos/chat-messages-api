FROM python:3.13-slim AS base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./

RUN pip install poetry && \
    poetry config virtualenvs.create false


FROM base AS prod
RUN poetry install --only main --no-root
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


FROM base AS test-stage
RUN poetry install --with dev --no-root
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./
COPY tests ./tests
