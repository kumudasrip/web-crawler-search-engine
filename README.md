# Distributed Web Crawler + Search Engine

A production-quality portfolio project for building a distributed web crawler, document store, inverted index search engine, TF-IDF ranking, and search frontend.

## Tech Stack

- Backend: Python + FastAPI
- Frontend: React + TypeScript + Tailwind CSS
- Database: PostgreSQL
- Queue / Distributed crawling: Redis
- Search: Inverted index + TF-IDF

## Project Goals

1. Crawl webpages from seed URLs.
2. Extract page title, content, and links.
3. Store crawled pages in PostgreSQL.
4. Build an inverted index for fast search.
5. Rank results using TF-IDF.
6. Expose search APIs with FastAPI.
7. Provide a React search UI.
8. Support distributed crawling with Redis queues and worker processes.
9. Track crawl analytics and status.
10. Maintain a clean architecture with type hints, logging, and documentation.

## Workspace Structure

- `backend/` — FastAPI application, crawler, indexer, workers, and API layer.
- `frontend/` — React search UI and analytics dashboard.
- `infra/` — Deployment manifests and environment configuration.
- `docs/` — Architecture diagrams, API design, roadmap, and database schema.
- `scripts/` — helper scripts for local setup and migrations.

## Next Steps

1. Define database schema and migrations.
2. Build backend packages for crawler, storage, indexing, search, and analytics.
3. Create search API and worker queue integration.
4. Scaffold frontend UI with search and analytics pages.
5. Add documentation for architecture, API, and deployment.
