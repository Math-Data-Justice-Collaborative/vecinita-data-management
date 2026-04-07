# vecinita-data-management

Monorepo for the Vecinita data management platform — a community-driven data collection and analysis system.

## Repository Structure

```
repo/
  apps/
    frontend/              # React/Vite UI  (submodule: vecinita-data-management-frontend)
    backend/
      scraper-service/     # Modal serverless scraping pipeline  (submodule: vecinita-scraper)
      model-service/       # Modal / local LLM inference service (submodule: vecinita-model)
      embedding-service/   # Modal serverless text vectorization  (submodule: vecinita-embedding)

  packages/
    shared-schemas/        # Pydantic/Zod shared types and API contracts
    service-clients/       # Typed HTTP clients for inter-service calls
    shared-config/         # Shared configuration utilities
    shared-logging/        # Shared logging utilities

  infra/
    docker-compose.yml     # Local development orchestration (model + frontend)
    docker/                # Per-service Dockerfiles (repo-root-context builds)
    k8s/                   # Kubernetes manifests

  scripts/                 # Developer utility scripts
  docs/                    # Architecture and developer documentation
```

## Dependency Model

```
frontend  →  scraper-service
frontend  →  model-service
frontend  →  embedding-service

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

| Service | Path | Description | Deployment | Port |
|---------|------|-------------|------------|------|
| frontend | `apps/frontend` | React/Vite UI | Docker web service | 10000 |
| scraper-service | `apps/backend/scraper-service` | Scraping API and worker pipeline | Modal / Docker web service | 10000 |
| model-service | `apps/backend/model-service` | LLM inference (Ollama) | Modal / local Docker | 8000 |
| embedding-service | `apps/backend/embedding-service` | Text embedding / vectorization | Modal | — |

> **embedding-service** remains a Modal serverless deployment. **scraper-service** can still be
> deployed to Modal, but it now also includes a Docker web-service path for Render.

## Shared Packages

| Package | Path | Description |
|---------|------|-------------|
| shared-schemas | `packages/shared-schemas` | API request/response types (Pydantic + Zod) |
| service-clients | `packages/service-clients` | Typed Python clients for service-to-service calls |
| shared-config | `packages/shared-config` | Shared configuration loading utilities |
| shared-logging | `packages/shared-logging` | Structured logging setup |

## Quick Start

### Clone with Submodules

Each service lives in its own repository, wired into this monorepo as a git submodule.
After cloning, initialise all submodules before running anything:

```bash
git clone https://github.com/Math-Data-Justice-Collaborative/vecinita-data-management.git
cd vecinita-data-management
git submodule update --init --recursive
```

To pull the latest commits from all submodule remotes at once:

```bash
git submodule update --remote --merge
```

### Local Development (Docker Compose)

The compose stack includes the **model-service** (with Ollama) and **frontend**.
The scraper and embedding services are Modal deployments — set their public URLs in your `.env`
before starting compose.

```bash
# From the repo root
docker compose -f infra/docker-compose.yml up --build
```

This starts:
- Frontend:      http://localhost:3000
- Model service: http://localhost:8000 (backed by Ollama on :11434)

For the model service (requires a running Ollama instance):

```bash
cd apps/backend/model-service
docker compose up   # uses the service's own docker-compose.yml (includes Ollama)
```

### Deploying Modal Services

```bash
# Scraper
cd apps/backend/scraper-service
pip install modal
modal deploy

# Embedding
cd apps/backend/embedding-service
pip install modal
modal deploy main.py
```

After deployment, copy the Modal endpoint URLs into your frontend `.env` as
`VITE_VECINITA_SCRAPER_API_URL` (required) and optionally
`VITE_VECINITA_MODEL_API_URL` / `VITE_VECINITA_EMBEDDING_API_URL`.

## Contributing

See [docs/contributing.md](docs/contributing.md) for development guidelines, branching strategy, and PR process.

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.