# API Design

## Backend API

### `GET /search`

- Query parameters:
  - `q` (string, required): search query
  - `limit` (integer, optional): max results, default 10
  - `offset` (integer, optional): pagination offset, default 0

- Response:
  - `results`: array of search result objects
  - `total`: total matched documents
  - `query`: original query

- Search result object:
  - `title` (string)
  - `url` (string)
  - `snippet` (string)
  - `score` (float)

### `POST /crawl`

- Request body:
  - `seed_urls` (array of strings): starting URLs
  - `max_depth` (integer, optional)
  - `max_pages` (integer, optional)

- Response:
  - `queued_urls` (integer)

### `GET /analytics`

- Response:
  - `pages_crawled` (integer)
  - `pending_urls` (integer)
  - `failed_urls` (integer)
  - `search_count` (integer)
  - `last_crawl_time` (string)

### `GET /status`

- Response:
  - `uptime` (string)
  - `queue_size` (integer)
  - `worker_count` (integer)

## Search Workflow

1. Client sends `GET /search?q=machine+learning`.
2. Backend normalizes query terms.
3. Search service retrieves matching `page_id`s from the inverted index.
4. Calculate TF-IDF score per document.
5. Sort and paginate results.
6. Return JSON payload.

## Crawler Workflow

1. Client requests `POST /crawl` with seed URLs.
2. Backend enqueues URLs into Redis.
3. Worker consumes URLs, fetches pages, extracts content, and stores page records.
4. Indexer processes the page text and updates inverted index entries.
5. Analytics counters are updated.
