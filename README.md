# Web Crawler Search Engine

A Python + React application implementing a web crawler, page store, search API, and frontend search UI. The repository contains working FastAPI endpoints, a crawler with URL normalization and robots.txt support, an in-memory inverted index, Redis/RQ worker helpers, and a React/Vite frontend.

## Features

- FastAPI backend with search, page retrieval, analytics, crawl control, and Redis queue endpoints.
- Web crawler with HTML fetching, retry/backoff, robots.txt respect, link extraction, and BFS-style depth-limited traversal.
- URL normalization and deduplication using normalized URLs and SHA-256 hashes.
- PostgreSQL persistence using SQLAlchemy for pages, URLs, crawl jobs, and page terms.
- In-memory inverted index and term persistence via `IndexerService`.
- React frontend with search results, pagination, analytics dashboard, and navigation.
- Redis/RQ worker support with task enqueuing and a worker start script.
- Basic analytics endpoint reporting crawled pages, unique URLs, pending URLs, and failed URLs.

## System Architecture

The system is split into frontend and backend.

- Frontend: React + TypeScript + Vite renders search pages and analytics, calling backend REST APIs.
- Backend: FastAPI serves the API and constructs the crawl/index/search flow.
- Database: PostgreSQL stores normalized URLs, page content, crawl jobs, and term frequencies.
- Queue: Redis + RQ modules provide queue connectivity and worker task scaffolding.

The backend uses SQLAlchemy for database access, BeautifulSoup for HTML parsing, and `requests` for fetching pages.

## Tech Stack

- Backend: Python, FastAPI, SQLAlchemy
- Frontend: React, TypeScript, Vite, Tailwind CSS
- Database: PostgreSQL (configured by `DATABASE_URL`)
- Queue: Redis / RQ
- HTTP client: `requests`
- Parsing: BeautifulSoup
- Testing: pytest, FastAPI TestClient

## Project Structure

- `backend/`
  - `app/main.py` — FastAPI application entrypoint with CORS and router registration.
  - `app/api/` — API routes and Pydantic schemas.
  - `app/core/` — database engine, session, and dependency injection.
  - `app/crawler/` — crawler, fetcher, normalizer, parser, robots.txt manager, and types.
  - `app/indexer/` — tokenizer, stop-word filtering, inverted index, and indexer service.
  - `app/models/` — SQLAlchemy models for URLs, pages, crawl jobs, and page terms.
  - `app/services/` — crawler, search, and analytics service implementations.
  - `app/worker/` — Redis queue helpers, RQ worker startup, task definition, and scheduler stub.
  - `tests/` — backend tests for API contracts, crawler/parser/indexer behavior.
- `frontend/`
  - `src/App.tsx` — React router and page wiring.
  - `src/components/` — UI components for search, analytics, and pagination.
  - `src/pages/` — homepage, search results page, and analytics page.
  - `src/services/api.ts` — frontend API client for backend endpoints.
  - `src/types/` — shared frontend data contracts.
  - `src/utils/` — formatting helpers.
- `docs/` — database schema definition and architecture notes.

## How It Works

### Crawling

- `backend/app/services/crawler_service.py` uses `Crawler` to fetch pages.
- `Crawler` builds a BFS queue from seed URLs, normalizes them, and visits each page up to `max_depth` and `max_pages`.
- `PageFetcher` uses `requests.get` with retry/backoff and a custom User-Agent.
- `RobotsTxtManager` fetches `robots.txt` and checks whether each URL is allowed.
- `PageParser` extracts the page title, visible text, and normalized outbound links with BeautifulSoup.

### Storage

- Normalized URLs are stored in the `urls` table with `normalized_url`, `url_hash`, and crawl metadata.
- Pages are stored in the `pages` table with a foreign key to the URL.
- `content_hash` is computed to skip saving unchanged pages.
- Terms are persisted per page in `page_terms`.

### Indexing

- `IndexerService.index_page()` combines title and content, tokenizes text, removes stop words, and indexes terms in-memory.
- The in-memory index maps terms to page IDs and frequencies using `InvertedIndex`.
- `IndexerService.rebuild_index_from_db()` can rebuild the in-memory index from persisted pages.

### Search

- `SearchService.search()` tokenizes the query, removes stop words, and uses `IndexerService.search()` to find matching page IDs.
- It performs an AND-style search across query terms.
- Search results are fetched from the database and returned with snippets and scores.

### Ranking

- Search now uses a complete TF-IDF ranker implementation.
- `TfIdfRanker` computes term frequency, inverse document frequency, TF-IDF scores, and normalized cosine-style ranking.
- Multi-word queries are supported and results are sorted by relevance.

### Frontend

- `frontend/src/App.tsx` defines routes for home, search, and analytics.
- `SearchResultsPage` calls `/api/search` and renders paginated results.
- `AnalyticsDashboard` calls `/api/analytics` and `/api/crawler/metrics` for dashboard metrics.
- The UI supports search input, result listing, and basic analytics display.

### Analytics

- `AnalyticsService.get_analytics()` returns counts for crawled pages, unique URLs, pending URLs, and failed URLs.
- `search_queries` and `index_size` are currently placeholders set to `0`.
- `CrawlerService` does not currently update detailed analytics counters or search event logs.

### Redis Workers

- `backend/app/worker/queue.py` creates Redis/RQ queue connections.
- `backend/app/worker/tasks.py` defines `crawl_job()` for worker execution.
- `backend/app/worker/start_worker.py` can launch an RQ worker for the `crawler` queue.
- `backend/app/worker/scheduler.py` contains a recurring enqueue helper, but it is not wired into a running scheduler process by default.
- The API provides `/api/crawler/enqueue`, `/api/crawler/metrics`, and `/api/crawler/failed` endpoints.

## API Endpoints

- `GET /health` — health check.
- `GET /` — root info with endpoint summary.
- `GET /api/search?q={query}&limit={n}&offset={n}` — search pages.
- `GET /api/page/{page_id}` — fetch full page content by ID.
- `GET /api/analytics` — crawl and search analytics overview.
- `GET /api/crawl/status/{job_id}` — status for a crawl job.
- `POST /api/crawl` — start a crawl job with `seed_urls`, `max_depth`, and `max_pages`.
- `POST /api/crawler/enqueue` — enqueue seed URLs into Redis/RQ.
- `GET /api/crawler/metrics` — fetch queue and crawler metrics.
- `GET /api/crawler/failed` — list failed RQ job IDs.

## Database Schema

Implemented models:

- `urls`
  - `id`, `url`, `normalized_url`, `url_hash`, `status`, retry fields, crawl timestamps.
  - tracks deduplicated normalized URLs and crawl state.
- `pages`
  - `id`, `url_id`, `title`, `content`, `content_hash`, `http_status`, `status`, `crawl_time`.
  - stores page content and metadata for crawled pages.
- `page_terms`
  - `id`, `page_id`, `term`, `frequency`, `last_updated`.
  - stores term frequencies for indexed pages.
- `crawl_jobs`
  - `id`, `name`, `seed_urls`, `max_depth`, `max_pages`, `status`, timestamps.
  - stores crawl job metadata.

The `docs/POSTGRES_SCHEMA.sql` file contains a broader schema design, but the active Python models use a simpler schema and do not implement every field from the SQL document.

## Algorithms Used

- Inverted Index: `InvertedIndex` stores terms mapped to page IDs and frequencies for fast term lookup.
- Tokenization: `Tokenizer` splits page text into lowercase tokens and normalizes punctuation.
- Stop-word filtering: `StopWordManager` removes common English stop words before indexing and search.
- URL normalization: `UrlNormalizer` normalizes scheme, host, path, query sorting, and default ports.
- Queue processing: Redis/RQ connection helpers and a worker task are implemented for enqueuing crawl jobs.
- Retry/backoff: `PageFetcher` retries requests on failure and uses exponential backoff.
- Deduplication: URLs are deduplicated by normalized URL and `content_hash` avoids re-saving unchanged page content.

## Current Limitations

- Analytics endpoints return placeholder values for `search_queries` and `index_size`.
- `backend/app/worker/scheduler.py` is a scheduler helper but not integrated as a running scheduled process.
- Search currently performs an AND-style match, and full phrase/OR query support is not implemented.
- The documented SQL schema in `docs/POSTGRES_SCHEMA.sql` includes fields not present in the current SQLAlchemy models.
- There is no persisted search query event tracking or click analytics in the backend.

## Future Improvements

- Implement positional inverted indexes for phrase search.
- Support OR queries, wildcard queries, and boolean search operators.
- Persist search query history and click analytics.
- Integrate the Redis scheduler for periodic crawling.
- Expand analytics with index size, search latency, and query popularity metrics.
- Add PageRank-based ranking alongside TF-IDF.
- Containerize the application using Docker Compose.

## Running Locally

1. Install backend dependencies:

   ```bash
   pip install -r backend/requirements.txt
   pip install -r backend/requirements-redis.txt
   ```

2. Configure environment variables:

   - `DATABASE_URL` (default: `postgresql://crawler:crawlerpass@localhost:5432/crawler_db`)
   - `REDIS_URL` (default: `redis://localhost:6379/0`)

3. Start PostgreSQL and Redis.

4. Run the backend app from the repository root:

   ```bash
   uvicorn backend.app.main:app --reload
   ```

5. Install frontend dependencies and run the UI:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

6. Open the frontend in the browser and use the search and analytics UI.
