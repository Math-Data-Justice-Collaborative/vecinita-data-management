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
- [uv](https://github.com/astral-sh/uv) (proxy service)
- [modal](https://modal.com/docs/guide) CLI (scraper and embedding services)

### First-time setup

This monorepo uses git submodules. After cloning, initialise them:

```bash
git submodule update --init --recursive
```

To pull the latest upstream changes into all submodules later:

```bash
git submodule update --remote --merge
```

### Start Everything (proxy + model + frontend)

```bash
docker compose -f infra/docker-compose.yml up --build
```

### Run a Single Backend Service

**Proxy** (FastAPI, port 10000):

```bash
cd apps/backend/proxy
cp .env.example .env   # fill in Modal credentials and backend URLs
pip install uv
uv sync
uv run uvicorn app.main:app --reload --port 10000
```

**Model service** (local Ollama, port 8000):

```bash
cd apps/backend/model-service
docker compose up   # uses the service's own docker-compose.yml
```

**Scraper service** (Modal serverless):

```bash
cd apps/backend/scraper-service
cp .env.example .env
modal serve   # hot-reloads locally via Modal sandbox
```

**Embedding service** (Modal serverless):

```bash
cd apps/backend/embedding-service
modal serve main.py
```

### Run the Frontend

```bash
cd apps/frontend
npm install
npm run dev   # Vite dev server on http://localhost:5173
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
