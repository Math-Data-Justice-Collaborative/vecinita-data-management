# Architecture

## Overview

Vecinita is a community-driven data management platform built as a monorepo.

## Services

### frontend

React/Vite web application (`vecinita-data-management-frontend`). Communicates with backends
directly via `VITE_*` environment variables (scraper, model, embedding).

### model-service

LLM inference service (`vecinita-model`) using **Ollama**. Deployed to **Modal** for production.
Local compose builds from `infra/docker/model-service.Dockerfile`, which clones the upstream repo.

### scraper-service

Serverless web-scraping pipeline (`vecinita-scraper`). Deployed to **Modal** and as a Docker image
from the vecinita monorepo `services/scraper` directory (see monorepo `render.yaml`).

### embedding-service

Text vectorization service (`vecinita-embedding`). Deployed exclusively to **Modal**.

## Deployment Model

```
frontend  ─────────────────────────────────────────────────► scraper  (Modal)
              │                                VITE_*        model     (Modal / local Ollama)
              │                                              embedding (Modal)
```

All arrows represent **runtime HTTP calls**, not code imports.

## Dependency Graph

```
frontend
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
|--------|--------|----------|-------|
| frontend | scraper | HTTPS | direct via `VITE_*` env var |
| frontend | model | HTTPS | direct via `VITE_*` env var |
| frontend | embedding | HTTPS | direct via `VITE_*` env var |
