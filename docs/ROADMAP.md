# Development Roadmap

## Phase 1: MVP

1. Scaffold backend and frontend structure.
2. Implement basic crawler with `requests` and `beautifulsoup4`.
3. Store crawled pages in PostgreSQL.
4. Build a simple inverted index and store term-document mappings.
5. Create FastAPI search endpoint.
6. Build a basic React search UI.

## Phase 2: Ranking

1. Add TF-IDF scoring to search results.
2. Improve tokenizer with normalization, stopword removal, and stemming support.
3. Add query phrase support and snippet generation.

## Phase 3: Distributed Crawling

1. Add Redis queue for URL scheduling.
2. Implement worker processes consuming URLs in parallel.
3. Add URL deduplication via normalized URL and hash.
4. Add retry logic for failed page fetches.

## Phase 4: Production Features

1. Implement crawl scheduler to refresh pages every 24 hours.
2. Add analytics dashboard with crawl metrics.
3. Harden backend with logging, error handling, and configuration.
4. Add Docker compose for local development.
5. Prepare deployment guidance for Render / Railway / Fly.io.

## Optional Enhancements

- Add author and meta-data extraction.
- Implement a search autocomplete service.
- Move search index to a specialized engine (e.g. Elasticsearch) later.
- Add user authentication for analytics dashboard.
