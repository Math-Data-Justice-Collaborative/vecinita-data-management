# Repo-root-context build for vecinita-modal-proxy.
# For standalone service-directory builds, use apps/backend/proxy/Dockerfile directly.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY apps/backend/proxy/pyproject.toml \
     apps/backend/proxy/uv.lock \
     apps/backend/proxy/README.md \
     ./
RUN uv sync --frozen --no-dev

COPY apps/backend/proxy/app ./app

EXPOSE 10000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-10000}"]