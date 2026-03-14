# Frontend

React/Next.js user interface for the Vecinita data management platform.

## Overview

The frontend communicates exclusively with the **proxy** service. It does not call backend services directly.

```
frontend → proxy → (scraper-service | model-service | embedding-service)
```

## Development

### Prerequisites

- Node.js >= 18
- npm or yarn

### Setup

```bash
cd apps/frontend
npm install
```

### Run locally

```bash
npm run dev
```

Starts the development server at http://localhost:3000.

### Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_PROXY_URL` | URL of the proxy service | `http://localhost:8000` |

## Build

```bash
npm run build
npm start
```

## Docker

```bash
docker build -f ../../infra/docker/frontend.Dockerfile -t vecinita-frontend .
docker run -p 3000:3000 vecinita-frontend
```
