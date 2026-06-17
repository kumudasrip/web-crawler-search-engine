# Phase 5 — Search API Implementation

Production-ready FastAPI backend with full search, analytics, and crawl endpoints.

## Endpoints

### 1. GET /search
Search the index for pages matching a query.

**Parameters**:
- `q` (required, string): Search query (1-500 chars)
- `limit` (optional, int): Max results (default 10, max 100)
- `offset` (optional, int): Pagination offset (default 0)

**Response**:
```json
{
  "query": "machine learning",
  "total": 5,
  "limit": 10,
  "offset": 0,
  "results": [
    {
      "page_id": 1,
      "title": "ML Guide",
      "url": "https://example.com/ml",
      "snippet": "Machine learning is...",
      "score": 0.85
    }
  ]
}
```

### 2. GET /page/{page_id}
Retrieve full content of a specific page.

**Response**:
```json
{
  "page_id": 1,
  "title": "Python Guide",
  "url": "https://example.com/guide",
  "content": "Full page content...",
  "http_status": 200,
  "crawl_time": "2026-06-17T12:00:00Z"
}
```

### 3. GET /analytics
Get crawler and search statistics.

**Response**:
```json
{
  "pages_crawled": 150,
  "unique_urls": 200,
  "pending_urls": 50,
  "failed_urls": 10,
  "search_queries": 500,
  "index_size": 12000
}
```

### 4. GET /crawl/status/{job_id}
Check status of a crawl job.

**Response**:
```json
{
  "job_id": 1,
  "status": "running",
  "seed_urls": ["https://example.com"],
  "pages_crawled": 45,
  "max_pages": 100,
  "started_at": "2026-06-17T12:00:00Z",
  "completed_at": null
}
```

### 5. POST /crawl
Start a new crawl job.

**Request**:
```json
{
  "seed_urls": ["https://example.com"],
  "max_depth": 2,
  "max_pages": 100
}
```

**Response**:
```json
{
  "job_id": 1,
  "status": "completed",
  "message": "Crawled 45 pages"
}
```

## Implementation Files

### API Layer
- `backend/app/api/schemas.py` — Pydantic request/response models
- `backend/app/api/routes.py` — FastAPI route handlers

### Service Layer
- `backend/app/services/search_service.py` — Search operations
- `backend/app/services/analytics_service.py` — Analytics queries
- `backend/app/services/crawler_service.py` — Crawling orchestration (reused)

### Main Application
- `backend/app/main.py` — FastAPI app initialization and configuration

### Tests
- `backend/tests/test_api.py` — Comprehensive API endpoint tests

## Features

✅ **Validation**: Pydantic schemas with field validation (min/max length, ranges)
✅ **Pagination**: Limit/offset support for search results
✅ **Error handling**: HTTP exceptions with meaningful error messages
✅ **OpenAPI docs**: Auto-generated at `/docs` (Swagger UI)
✅ **CORS enabled**: Allows requests from any origin
✅ **Health check**: GET /health and GET / endpoints
✅ **Type hints**: Full Python type annotations
✅ **Logging**: Request/response logging for debugging
✅ **Database integration**: Uses SQLAlchemy ORM with dependency injection

## Running the Server

### 1. Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Setup database
```bash
# Create PostgreSQL database
createdb crawler_db

# Or use Docker Compose
docker-compose -f infra/docker-compose.yml up -d
```

### 3. Run the server
```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the API
- OpenAPI docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/health

## Pydantic Models

### Request Models
- `SearchRequest` — Query parameters with validation
- `CrawlRequestBody` — Crawl job parameters
- Common validations:
  - Min/max length for strings
  - Range constraints for integers
  - Min/max items for arrays

### Response Models
- `SearchResponse` — Search results with pagination
- `SearchResultItem` — Individual search result
- `PageResponse` — Full page content
- `AnalyticsResponse` — Crawler/search statistics
- `CrawlStatusResponse` — Crawl job status
- `CrawlResponseBody` — Crawl job response

## Error Handling

All endpoints return consistent error responses:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

Common HTTP status codes:
- `200`: Success
- `404`: Resource not found
- `422`: Validation error (invalid parameters)
- `500`: Server error

## Integration with Other Layers

1. **Search**:
   - `SearchService` uses `IndexerService` to access the inverted index
   - `TfIdfRanker` ranks results by relevance
   - Snippets generated from page content

2. **Crawling**:
   - `CrawlerService` fetches and stores pages
   - Stores job metadata in `crawl_jobs` table
   - Returns job status and progress

3. **Analytics**:
   - Queries database for count statistics
   - Aggregates metrics from multiple tables
   - Extensible for custom metrics

## Testing

Run all tests:
```bash
pytest backend/tests/test_api.py -v
```

Test coverage includes:
- Valid and invalid queries
- Pagination edge cases
- Field validation
- Response schema compliance
- Error handling
- Database interactions

## Database Dependency Injection

The `get_db()` function provides session management:

```python
def get_db() -> Iterator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Each endpoint receives a fresh session that's automatically closed.

## OpenAPI Documentation

FastAPI automatically generates OpenAPI (Swagger) documentation at `/docs`.

Features:
- Interactive endpoint testing
- Parameter documentation
- Example requests/responses
- Schema definitions
- Authentication info

## Next Steps

Phase 6: Frontend React UI for search and analytics dashboard.
