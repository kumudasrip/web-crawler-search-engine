# Folder Structure

```
web-crawler-search-engine/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py
│   │   │   ├── dependencies.py
│   │   │   └── schemas.py
│   │   ├── crawler/
│   │   │   ├── fetcher.py
│   │   │   ├── parser.py
│   │   │   ├── deduplicator.py
│   │   │   └── scheduler.py
│   │   ├── indexer/
│   │   │   ├── tokenizer.py
│   │   │   ├── index_builder.py
│   │   │   └── ranker.py
│   │   ├── models/
│   │   │   ├── page.py
│   │   │   ├── inverted_index.py
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   ├── crawl_service.py
│   │   │   ├── search_service.py
│   │   │   └── analytics_service.py
│   │   ├── workers/
│   │   │   ├── redis_worker.py
│   │   │   └── retry_worker.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── logger.py
│   │   │   └── database.py
│   │   └── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchBox.tsx
│   │   │   ├── SearchResults.tsx
│   │   │   └── AnalyticsDashboard.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   └── DashboardPage.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── package.json
│   └── tailwind.config.js
├── infra/
│   ├── docker-compose.yml
│   ├── postgres.env
│   ├── redis.env
│   └── app.env
├── scripts/
│   ├── init_db.sh
│   ├── seed_urls.py
│   └── run_workers.sh
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_DESIGN.md
│   ├── DATABASE_SCHEMA.md
│   └── ROADMAP.md
└── README.md
```

## Notes

- `backend/app/api` holds FastAPI route definitions and request/response schemas.
- `backend/app/crawler` contains crawler, parser, deduplication, and scheduler logic.
- `backend/app/indexer` handles tokenization, index building, and ranking.
- `backend/app/services` contains business logic for crawl orchestration, search, and analytics.
- `infra` includes local environment files and Docker compose for PostgreSQL/Redis.
- `scripts` includes setup helpers and worker launch scripts.
