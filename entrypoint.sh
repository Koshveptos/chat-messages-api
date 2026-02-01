
set -e


echo "Waiting for postgres..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Postgres started"


echo "Running Alembic migrations..."
alembic upgrade head


exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload