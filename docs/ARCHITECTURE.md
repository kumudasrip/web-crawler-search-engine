# System Architecture

## Overview

This project is a mini search engine built from scratch.
It includes a distributed crawler, document store, inverted index, TF-IDF ranking, search API, and frontend.

## High-Level Architecture

Crawler
  ↓
Document Store
  ↓
Indexer
  ↓
Search Engine
  ↓
Frontend

### Components

- `Crawler`: fetches webpages from seed URLs, extracts title, text content, and outgoing links.
- `Document Store`: saves crawled pages and metadata in PostgreSQL.
- `Indexer`: tokenizes text, normalizes words, removes punctuation, and updates the inverted index.
- `Search Engine`: resolves query terms via the inverted index and ranks documents using TF-IDF.
- `Frontend`: React UI for search input, results, and analytics.
- `Redis Queue`: supports distributed crawler workers.

## Data Flow

1. Seed URL enters the crawler queue.
2. Worker fetches the page and extracts metadata.
3. Page is stored in PostgreSQL.
4. Indexer processes the page text and updates inverted index entries.
5. Search requests query the index and return ranked results.

## Distributed Crawling

- `URL Queue` in Redis stores pending URLs.
- Multiple worker processes consume URLs concurrently.
- Deduplication prevents duplicate crawls by normalized URL and hash.
- Retries are scheduled for failed crawls.

## Analytics

Captured metrics include:
- Total pages crawled
- Pending URLs
- Failed URLs
- Search query count

## Sequence Diagram

1. User enters search query.
2. Frontend calls `GET /search?q=...`.
3. FastAPI search endpoint queries search service.
4. Search service looks up words in the inverted index.
5. Results are ranked and returned.

---

## Architecture Decisions

- Python + FastAPI: lightweight backend with modern async support.
- PostgreSQL: reliable document storage and analytics.
- Redis: queue and distributed worker coordination.
- React + TypeScript: responsive search UI and dashboard.
- TF-IDF ranking: interviewer-friendly relevance scoring.

## Tradeoffs

- In-memory inverted index is fast but needs persistence or rebuilds.
- PostgreSQL supports ACID storage, but the inverted index may eventually move to a specialized search engine.
- Distributed crawling using Redis adds complexity but demonstrates resume-level system design.
