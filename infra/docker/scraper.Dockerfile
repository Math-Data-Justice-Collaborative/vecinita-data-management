# vecinita-scraper is a Modal serverless service and is NOT run as a local container.
#
# To deploy to Modal:
#   cd apps/backend/scraper-service
#   pip install modal
#   modal deploy
#
# To run locally with Modal:
#   modal serve
#
# This Dockerfile installs dependencies for linting/testing purposes only.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY apps/backend/scraper-service/pyproject.toml ./
COPY apps/backend/scraper-service/src ./src

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir .

# No CMD: this service runs via Modal, not as a containerised process.
# See apps/backend/scraper-service/DEPLOYMENT.md for deployment instructions.
