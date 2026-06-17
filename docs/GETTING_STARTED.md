# Getting Started — Backend Development

Quick start guide for running the web crawler and search engine backend locally.

## Prerequisites

- Python 3.10+
- PostgreSQL (or Docker)
- pip/virtualenv

## Setup (5 minutes)

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Start PostgreSQL

**Option A: Using Docker Compose**
```bash
cd infra
docker-compose up -d
```

**Option B: Local PostgreSQL**
```bash
createdb crawler_db
createuser crawler
psql crawler_db -c "ALTER USER crawler WITH PASSWORD 'crawlerpass';"
```

### 4. Set environment variables
```bash
export DATABASE_URL="postgresql://crawler:crawlerpass@localhost:5432/crawler_db"
```

### 5. Initialize database
```bash
python scripts/init_db.py
```

### 6. Run the server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for interactive API docs.

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_api.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Development Workflow

### 1. Index some test data
```python
from app.services import CrawlerService
from app.core import SessionLocal

db = SessionLocal()
crawler = CrawlerService(db, max_pages=10)
pages = crawler.crawl_and_store(["https://example.com"])
db.close()
```

### 2. Test search
```bash
curl "http://localhost:8000/api/search?q=example&limit=5"
```

### 3. Check analytics
```bash
curl "http://localhost:8000/api/analytics"
```

## Troubleshooting

### Database connection error
```
psycopg2.OperationalError: could not connect to server
```

**Solution**: Check PostgreSQL is running:
```bash
# Docker
docker ps
docker logs <container_id>

# Local
psql -U postgres -c "\l"
```

### Import errors
```
ModuleNotFoundError: No module named 'app'
```

**Solution**: Run from the `backend` directory:
```bash
cd backend
python -m pytest tests/
```

### Port 8000 already in use
```
OSError: [Errno 48] Address already in use
```

**Solution**: Use a different port:
```bash
uvicorn app.main:app --port 8001
```

## Project Structure

```
backend/
├── app/
│   ├── api/           ← FastAPI routes & schemas
│   ├── crawler/       ← Web crawler modules
│   ├── indexer/       ← Search indexing
│   ├── models/        ← SQLAlchemy models
│   ├── services/      ← Business logic
│   ├── core/          ← Database config
│   └── main.py        ← FastAPI app
├── tests/             ← Unit & integration tests
├── db/
│   └── schema.sql     ← Database schema
├── migrations/        ← Database migrations
├── requirements.txt   ← Python dependencies
└── scripts/           ← Helper scripts
```

## Key Modules

| Module | Purpose |
|--------|---------|
| `crawler` | Fetch & parse web pages |
| `indexer` | Build inverted index + TF-IDF ranking |
| `services` | Orchestrate crawling, searching, analytics |
| `api` | FastAPI route handlers |
| `models` | SQLAlchemy ORM models |

## Common Tasks

### Index a new page manually
```python
from app.services import IndexerService
from app.core import SessionLocal

db = SessionLocal()
indexer = IndexerService(db)
indexer.index_page(1, "Python Guide", "python is a great language...")
db.close()
```

### Rebuild the full search index
```python
from app.services import IndexerService
from app.core import SessionLocal

db = SessionLocal()
indexer = IndexerService(db)
indexer.rebuild_index_from_db()
db.close()
```

### Check crawled pages
```bash
psql crawler_db -c "SELECT id, title, url FROM pages LIMIT 10;"
```

### Monitor search index
```bash
psql crawler_db -c "SELECT COUNT(*) as unique_terms FROM page_terms;"
```

## Performance Tips

1. **Batch inserts**: Index multiple pages in one transaction
2. **Connection pooling**: SQLAlchemy handles this automatically
3. **Caching**: Add Redis for query result caching
4. **Pagination**: Always use limit/offset for large result sets
5. **Indexing**: PostgreSQL indexes on frequently queried columns

## Next Steps

1. Crawl some seed URLs
2. Test search functionality
3. Deploy to Render/Railway
4. Add frontend (React)
5. Setup analytics dashboard
