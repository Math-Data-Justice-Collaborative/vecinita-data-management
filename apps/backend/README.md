# Backend layout

Legacy **git submodules** for `scraper-service`, `embedding-service`, and `model-service` under this
directory were removed (feature `003-consolidate-scraper-dm`). Runtime integration uses **remote HTTP
APIs** configured via `SCRAPER_SERVICE_BASE_URL`, `EMBEDDING_SERVICE_BASE_URL`, and
`MODEL_SERVICE_BASE_URL` (see `packages/shared-config`) and `packages/service-clients`.

For Modal deploys and Docker builds of the scraper stack, use the dedicated repositories or the
**vecinita** monorepo paths:

- Scraper: `services/scraper` (Render blueprint in monorepo root `render.yaml`)
- Embedding / model: `services/embedding-modal`, `services/model-modal`, or deployed Modal endpoints
