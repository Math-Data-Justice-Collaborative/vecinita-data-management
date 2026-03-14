# Proxy Service

API gateway and Backend-for-Frontend (BFF) for the Vecinita platform.

## Responsibilities

- Authentication and session management
- Request routing to downstream services
- Response aggregation
- Rate limiting and access control

## Architecture

```
frontend → proxy → scraper-service
               → model-service
               → embedding-service
```

The proxy is the **only** entry point the frontend interacts with.  
All downstream service URLs are configured via environment variables.

## Development

### Prerequisites

- Python >= 3.11
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

```bash
cd apps/backend/proxy

# Install shared packages first
pip install -e ../../packages/shared-schemas
pip install -e ../../packages/shared-config
pip install -e ../../packages/shared-logging

# Install the service in editable mode
pip install -e ".[dev]"
```

### Run locally

```bash
uvicorn src.main:app --reload --port 8000
```

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Bind host | `0.0.0.0` |
| `PORT` | Bind port | `8000` |
| `SCRAPER_SERVICE_URL` | Scraper service base URL | `http://localhost:8001` |
| `MODEL_SERVICE_URL` | Model service base URL | `http://localhost:8002` |
| `EMBEDDING_SERVICE_URL` | Embedding service base URL | `http://localhost:8003` |

## Tests

```bash
pytest tests/
```

## Docker

```bash
docker build -f ../../../infra/docker/proxy.Dockerfile -t vecinita-proxy .
docker run -p 8000:8000 vecinita-proxy
```
