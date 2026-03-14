# vecinita-data-management

Monorepo for the Vecinita data management platform — a community-driven data collection and analysis system.

## Repository Structure

```
repo/
  apps/
    frontend/              # React/Next.js UI
    backend/
      proxy/               # API gateway / BFF (auth, routing, aggregation)
      scraper-service/     # Data collection and orchestration
      model-service/       # ML inference service
      embedding-service/   # Text vectorization service

  packages/
    shared-schemas/        # Pydantic/Zod shared types and API contracts
    service-clients/       # Typed HTTP clients for inter-service calls
    shared-config/         # Shared configuration utilities
    shared-logging/        # Shared logging utilities

  infra/
    docker-compose.yml     # Local development orchestration
    docker/                # Per-service Dockerfiles
    k8s/                   # Kubernetes manifests

  scripts/                 # Developer utility scripts
  docs/                    # Architecture and developer documentation
```

## Dependency Model

```
frontend  →  proxy
proxy     →  scraper-service
proxy     →  model-service
proxy     →  embedding-service

scraper-service  →  model-service
scraper-service  →  embedding-service
```

Rules enforced by convention:
- `apps` can depend on `packages`; `packages` must **not** depend on `apps`
- Lower-level services (`model-service`, `embedding-service`) do **not** depend on higher-level ones
- No circular dependencies
- Cross-service communication happens over HTTP/gRPC, **never** by importing another app's internals
- Shared code (schemas, clients, utilities) lives in `packages/`

## Services

| Service | Path | Description | Port |
|---------|------|-------------|------|
| frontend | `apps/frontend` | React UI | 3000 |
| proxy | `apps/backend/proxy` | API gateway / BFF | 8000 |
| scraper-service | `apps/backend/scraper-service` | Data scraping & orchestration | 8001 |
| model-service | `apps/backend/model-service` | ML model inference | 8002 |
| embedding-service | `apps/backend/embedding-service` | Text embedding / vectorization | 8003 |

## Shared Packages

| Package | Path | Description |
|---------|------|-------------|
| shared-schemas | `packages/shared-schemas` | API request/response types (Pydantic + Zod) |
| service-clients | `packages/service-clients` | Typed Python clients for service-to-service calls |
| shared-config | `packages/shared-config` | Shared configuration loading utilities |
| shared-logging | `packages/shared-logging` | Structured logging setup |

## Quick Start

### Local Development (Docker Compose)

```bash
# From the repo root
docker compose -f infra/docker-compose.yml up --build
```

This starts all services:
- Frontend: http://localhost:3000
- Proxy: http://localhost:8000
- Scraper: http://localhost:8001
- Model: http://localhost:8002
- Embedding: http://localhost:8003

### Running a Single Service

Each service has its own `README.md` with instructions. Example for the proxy:

```bash
cd apps/backend/proxy
pip install -e ../../packages/shared-schemas ../../packages/shared-config ../../packages/shared-logging
pip install -e ".[dev]"
uvicorn src.main:app --reload
```

## Contributing

See [docs/contributing.md](docs/contributing.md) for development guidelines, branching strategy, and PR process.

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.