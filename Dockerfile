FROM python:3.13-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy ML module (project root level)
COPY skyguard/ /app/skyguard/

# Copy backend requirements & ML requirements
COPY backend/requirements.txt /app/requirements.txt
COPY ml-development/requirements.txt /app/ml-requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r ml-requirements.txt

# Copy backend application code
COPY backend/app/ /app/app/
COPY backend/alembic/ /app/alembic/
COPY backend/alembic.ini /app/alembic.ini

# Set PYTHONPATH so 'skyguard' module is importable
ENV PYTHONPATH=/app

EXPOSE 8080

CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
