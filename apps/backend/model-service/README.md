# Model Service

ML model inference service for the Vecinita platform.

## Responsibilities

- Running ML model inference on input data
- Returning structured predictions

## Architecture

```
proxy           → model-service
scraper-service → model-service
```

The model service is a **lower-level service**. It does not call scraper, proxy, or embedding-service.  
It only depends on shared packages.

## Development

### Prerequisites

- Python >= 3.11

### Setup

```bash
cd apps/backend/model-service

pip install -e ../../packages/shared-schemas
pip install -e ../../packages/shared-config
pip install -e ../../packages/shared-logging
pip install -e ".[dev]"
```

### Run locally

```bash
uvicorn src.main:app --reload --port 8002
```

### Environment Variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Bind host | `0.0.0.0` |
| `PORT` | Bind port | `8002` |
| `MODEL_PATH` | Path to the model weights | `./models/default` |

## Tests

```bash
pytest tests/
```

## Docker

```bash
docker build -f ../../../infra/docker/model.Dockerfile -t vecinita-model .
docker run -p 8002:8002 vecinita-model
```
