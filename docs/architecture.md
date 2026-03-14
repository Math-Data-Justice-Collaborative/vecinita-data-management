# Architecture

## Overview

Vecinita is a community-driven data management platform built as a monorepo.

## Services

### frontend

React/Next.js web application. Communicates **only** with the proxy service.

### proxy

FastAPI API gateway and Backend-for-Frontend (BFF). Handles:
- Authentication and session management  
- Request routing to backend services
- Response aggregation

### scraper-service

Data collection and orchestration service. Calls:
- `model-service` — for ML inference on scraped content
- `embedding-service` — for vectorizing scraped content

### model-service

ML model inference. Standalone lower-level service. Does **not** call any other service.

### embedding-service

Text vectorization. Standalone lower-level service. Does **not** call any other service.

## Dependency Graph

```
frontend
  └── proxy
        ├── scraper-service
        │     ├── model-service
        │     └── embedding-service
        ├── model-service
        └── embedding-service
```

All arrows represent **runtime HTTP calls**, not code imports.  
Cross-service calls use typed clients from `packages/service-clients`.

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

| Caller | Callee | Protocol |
|--------|--------|----------|
| frontend | proxy | HTTPS |
| proxy | scraper-service | HTTP (internal) |
| proxy | model-service | HTTP (internal) |
| proxy | embedding-service | HTTP (internal) |
| scraper-service | model-service | HTTP (internal) |
| scraper-service | embedding-service | HTTP (internal) |
