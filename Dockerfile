FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=10000

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Render currently builds this repository from the repo root. Mirror the
# scraper-service Docker build here so root-level Dockerfile resolution works.
COPY apps/backend/scraper-service/pyproject.toml apps/backend/scraper-service/README.md ./
COPY apps/backend/scraper-service/src ./src

RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir .

EXPOSE 10000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=5 \
    CMD curl -f http://localhost:${PORT:-10000}/health || exit 1

CMD ["sh", "-c", "uvicorn vecinita_scraper.api.server:app --host 0.0.0.0 --port ${PORT:-10000}"]