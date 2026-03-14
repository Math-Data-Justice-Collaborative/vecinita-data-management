# Scraper Service

Data collection and orchestration service for the Vecinita platform.

## Responsibilities

- Scraping data from external sources
- Orchestrating calls to `model-service` and `embedding-service`
- Storing processed records

## Architecture

```
scraper-service → model-service      (via ModelClient)
scraper-service → embedding-service  (via EmbeddingClient)
```

The scraper calls downstream services using typed clients from `packages/service-clients`.
It does **not** import internals from model-service or embedding-service directly.

## Development

### Prerequisites

- Python >= 3.11

### Setup

```bash
cd apps/backend/scraper-service

pip install -e ../../packages/shared-schemas
pip install -e ../../packages/service-clients
pip install -e ../../packages/shared-config
pip install -e ../../packages/shared-logging
pip install -e ".[dev]"
```

### Run locally

```bash
uvicorn src.main:app --reload --port 8001
```

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Bind host | `0.0.0.0` |
| `PORT` | Bind port | `8001` |
| `MODEL_SERVICE_URL` | Model service base URL | `http://localhost:8002` |
| `EMBEDDING_SERVICE_URL` | Embedding service base URL | `http://localhost:8003` |

## Tests

```bash
pytest tests/
```

## Docker

```bash
docker build -f ../../../infra/docker/scraper.Dockerfile -t vecinita-scraper .
docker run -p 8001:8001 vecinita-scraper
```
