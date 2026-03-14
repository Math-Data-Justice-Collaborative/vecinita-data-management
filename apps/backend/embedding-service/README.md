# Embedding Service

Text embedding and vectorization service for the Vecinita platform.

## Responsibilities

- Generating vector embeddings from text input
- Supporting semantic search and similarity workflows

## Architecture

```
proxy           → embedding-service
scraper-service → embedding-service
```

The embedding service is a **lower-level service**. It does not call scraper, proxy, or model-service.  
It only depends on shared packages.

## Development

### Prerequisites

- Python >= 3.11

### Setup

```bash
cd apps/backend/embedding-service

pip install -e ../../packages/shared-schemas
pip install -e ../../packages/shared-config
pip install -e ../../packages/shared-logging
pip install -e ".[dev]"
```

### Run locally

```bash
uvicorn src.main:app --reload --port 8003
```

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Bind host | `0.0.0.0` |
| `PORT` | Bind port | `8003` |
| `EMBEDDING_MODEL` | Embedding model name or path | `sentence-transformers/all-MiniLM-L6-v2` |

## Tests

```bash
pytest tests/
```

## Docker

```bash
docker build -f ../../../infra/docker/embedding.Dockerfile -t vecinita-embedding .
docker run -p 8003:8003 vecinita-embedding
```
