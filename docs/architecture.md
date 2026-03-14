# Architecture

## Overview

Vecinita is a community-driven data management platform built as a monorepo.

## Services

### frontend

React/Vite web application (`vecinita-data-management-frontend`). Communicates with backends
directly via `VITE_*` environment variables (scraper, model, embedding) or through the proxy.

### proxy

FastAPI multi-backend proxy (`vecinita-modal-proxy`). Deployed on **Render** as a Docker container.
Keeps Modal credentials server-side and routes requests by path prefix:

| Path prefix | Routes to |
|-------------|----------|
| `/jobs/...` | scraper (path unchanged) |
| `/model/...` | model (strips `/model`) |
| `/embedding/...` | embedding (strips `/embedding`) |

### model-service

LLM inference service (`vecinita-model`) using **Ollama**. Deployed to **Modal** for production.
Can also be run locally with Docker Compose (ships its own `docker-compose.yml` that includes an
Ollama sidecar).

### scraper-service

Serverless web-scraping pipeline (`vecinita-scraper`). Deployed exclusively to **Modal**.
Uses Modal queues for job management and integrates with Supabase for storage.
See `apps/backend/scraper-service/DEPLOYMENT.md`.

### embedding-service

Text vectorization service (`vecinita-embedding`). Deployed exclusively to **Modal**.
Uses FastEmbed for open-source embeddings.
See `apps/backend/embedding-service/README.md`.

## Deployment Model

```
frontend  ─────────────────────────────────────────────────► scraper  (Modal)
              │                                VITE_*        model     (Modal / local Ollama)
              │                                              embedding (Modal)
              ▼
           proxy  ──── /jobs/...      ──►  scraper   (Modal)
          (Render) ──── /model/...    ──►  model     (Modal / local Ollama)
                   ──── /embedding/.. ──►  embedding (Modal)
```

All arrows represent **runtime HTTP calls**, not code imports.

## Dependency Graph

```
frontend
  └── proxy (Render)
        ├── scraper-service   (Modal)
        ├── model-service     (Modal / local Ollama)
        └── embedding-service (Modal)
```

## Shared Packages

| Package | Purpose |
|---------|---------|
| `shared-schemas` | Pydantic models for all API contracts |
| `service-clients` | Typed async HTTP clients |
| `shared-config` | Base settings using pydantic-settings |
| `shared-logging` | Structured JSON logging |

## Dependency Rules

1. `apps` may depend on `packages`
2. `packages` must **never** depend on `apps`
3. Lower-level services (`model-service`, `embedding-service`) must **not** depend on higher-level ones
4. No circular dependencies

## Communication Patterns

| Caller | Callee | Protocol | Notes |
|--------|--------|----------|---------|
| frontend | proxy | HTTPS | via Render public URL |
| frontend | scraper | HTTPS | direct via `VITE_*` env var |
| frontend | model | HTTPS | direct via `VITE_*` env var |
| frontend | embedding | HTTPS | direct via `VITE_*` env var |
| proxy | scraper | HTTPS | via `VECINITA_SCRAPER_API_URL` |
| proxy | model | HTTPS | via `VECINITA_MODEL_API_URL` |
| proxy | embedding | HTTPS | via `VECINITA_EMBEDDING_API_URL` |
