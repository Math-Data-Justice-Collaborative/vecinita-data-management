# Contributing

## Repository Layout

```
apps/
  frontend/              # React/Next.js UI
  backend/
    proxy/               # FastAPI API gateway
    scraper-service/     # Data collection
    model-service/       # ML inference
    embedding-service/   # Text vectorization
packages/
  shared-schemas/        # Pydantic API types
  service-clients/       # Typed HTTP clients
  shared-config/         # Configuration
  shared-logging/        # Logging
infra/                   # Docker and Kubernetes
scripts/                 # Dev utilities
docs/                    # Documentation
```

## Local Development

### Prerequisites

- Python >= 3.11
- Node.js >= 18
- Docker and Docker Compose

### Start Everything

```bash
docker compose -f infra/docker-compose.yml up --build
```

### Run a Single Backend Service

```bash
cd apps/backend/proxy

# Install shared packages
pip install -e ../../packages/shared-schemas
pip install -e ../../packages/shared-config
pip install -e ../../packages/shared-logging

# Install the service
pip install -e ".[dev]"

# Start
uvicorn src.main:app --reload --port 8000
```

### Run the Frontend

```bash
cd apps/frontend
npm install
npm run dev
```

## Code Standards

### Python

- Format: [ruff](https://github.com/astral-sh/ruff)
- Line length: 100
- Python >= 3.11 syntax (use `str | None` instead of `Optional[str]`)

### TypeScript / JavaScript

- Format: Prettier (configured per service)
- Lint: ESLint

## Adding a New Shared Schema

1. Add your Pydantic model to `packages/shared-schemas/shared_schemas/`
2. Export it from `shared_schemas/__init__.py`
3. Reinstall: `pip install -e packages/shared-schemas`

## Adding a New Service Client

1. Add your async client to `packages/service-clients/service_clients/`
2. Export it from `service_clients/__init__.py`
3. Add a test in `packages/service-clients/tests/`

## Pull Requests

- Open against `main`
- Include tests for any logic changes
- Do not import from another `apps/` service's internals
