import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.schemas import (
    SearchResponse,
    SearchResultItem,
    PageResponse,
    AnalyticsResponse,
    CrawlStatusResponse,
    CrawlRequestBody,
    CrawlResponseBody,
)
from backend.app.core import get_db
from backend.app.indexer import IndexerService
from backend.app.services import SearchService, AnalyticsService, CrawlerService

router = APIRouter(prefix='/api', tags=['search'])
logger = logging.getLogger(__name__)


@router.get('/search', response_model=SearchResponse)
def search(
    q: str = Query(..., min_length=1, max_length=500, description='Search query'),
    limit: int = Query(10, ge=1, le=100, description='Max results'),
    offset: int = Query(0, ge=0, description='Pagination offset'),
    db: Session = Depends(get_db),
) -> dict:
    """
    Search the index for pages matching the query.

    - **q**: Search query (required)
    - **limit**: Max results (default 10, max 100)
    - **offset**: Pagination offset (default 0)

    Returns ranked results with snippets.
    """
    try:
        indexer_service = IndexerService(db)
        search_service = SearchService(db, indexer_service)
        results, total = search_service.search(q, limit, offset)

        return SearchResponse(
            query=q,
            total=total,
            limit=limit,
            offset=offset,
            results=[SearchResultItem(**r) for r in results],
        )
    except Exception as exc:
        logger.exception('Search error: %s', exc)
        raise HTTPException(status_code=500, detail='Search failed') from exc


@router.get('/page/{page_id}', response_model=PageResponse)
def get_page(page_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Get full page content by page ID.

    Returns page title, URL, content, and metadata.
    """
    try:
        indexer_service = IndexerService(db)
        search_service = SearchService(db, indexer_service)
        page_data = search_service.get_page(page_id)

        if not page_data:
            raise HTTPException(status_code=404, detail='Page not found')

        return PageResponse(**page_data)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception('Get page error: %s', exc)
        raise HTTPException(status_code=500, detail='Failed to fetch page') from exc


@router.get('/analytics', response_model=AnalyticsResponse)
def get_analytics(db: Session = Depends(get_db)) -> dict:
    """
    Get crawler and search analytics.

    Returns metrics on crawled pages, URLs, and search queries.
    """
    try:
        analytics_service = AnalyticsService(db)
        data = analytics_service.get_analytics()
        return AnalyticsResponse(**data)
    except Exception as exc:
        logger.exception('Analytics error: %s', exc)
        raise HTTPException(status_code=500, detail='Failed to fetch analytics') from exc


@router.get('/crawl/status/{job_id}', response_model=CrawlStatusResponse)
def get_crawl_status(job_id: int, db: Session = Depends(get_db)) -> dict:
    """
    Get status of a specific crawl job.

    Returns job status, progress, and metadata.
    """
    try:
        analytics_service = AnalyticsService(db)
        job_data = analytics_service.get_crawl_job_status(job_id)

        if not job_data:
            raise HTTPException(status_code=404, detail='Crawl job not found')

        return CrawlStatusResponse(**job_data)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception('Get crawl status error: %s', exc)
        raise HTTPException(status_code=500, detail='Failed to fetch crawl status') from exc


@router.post('/crawl', response_model=CrawlResponseBody)
def start_crawl(body: CrawlRequestBody, db: Session = Depends(get_db)) -> dict:
    """
    Start a new crawl job.

    Accepts seed URLs, crawl depth, and max pages.
    Returns job ID and status.
    """
    try:
        crawler_service = CrawlerService(
            db,
            max_depth=body.max_depth,
            max_pages=body.max_pages,
        )

        # Store crawl job metadata
        from backend.app.models.crawl_job import CrawlJob

        job = CrawlJob(
            name=f'crawl_{db.query(CrawlJob).count() + 1}',
            seed_urls=body.seed_urls,
            max_depth=body.max_depth,
            max_pages=body.max_pages,
            status='running',
        )
        db.add(job)
        db.commit()

        # Start crawling
        pages = crawler_service.crawl_and_store(body.seed_urls)

        job.status = 'completed'
        db.commit()

        return CrawlResponseBody(
            job_id=job.id,
            status='completed',
            message=f'Crawled {len(pages)} pages',
        )
    except Exception as exc:
        logger.exception('Crawl error: %s', exc)
        raise HTTPException(status_code=500, detail='Crawl failed') from exc


# --- Redis / Worker endpoints -------------------------------------------------
@router.post('/crawler/enqueue')
def enqueue_urls(seed_urls: list[str], db: Session = Depends(get_db)) -> dict:
    """Enqueue seed URLs into the Redis crawler queue for distributed workers."""
    try:
        from redis import Redis
        from rq import Queue, Retry

        redis_url = getattr(__import__('os'), 'environ').get('REDIS_URL', 'redis://localhost:6379/0')
        conn = Redis.from_url(redis_url)
        q = Queue('crawler', connection=conn)

        job_ids = []
        for url in seed_urls:
            # enqueue the worker task by import path so remote workers can execute it
            job = q.enqueue('backend.app.worker.tasks.crawl_job', url, retry=Retry(max=3))
            job_ids.append(job.id)

        return {'enqueued': len(job_ids), 'job_ids': job_ids}
    except Exception as exc:
        logger.exception('Enqueue error: %s', exc)
        raise HTTPException(status_code=500, detail='Failed to enqueue URLs') from exc


@router.get('/crawler/metrics')
def crawler_metrics(db: Session = Depends(get_db)) -> dict:
    """Return crawler-related metrics: queue size, failed jobs, pages crawled, throughput."""
    try:
        from redis import Redis
        from rq import Queue, FailedJobRegistry

        redis_url = getattr(__import__('os'), 'environ').get('REDIS_URL', 'redis://localhost:6379/0')
        conn = Redis.from_url(redis_url)
        q = Queue('crawler', connection=conn)
        registry = FailedJobRegistry('crawler', connection=conn)

        analytics_service = AnalyticsService(db)
        core_metrics = analytics_service.get_analytics()

        # Basic Redis/RQ metrics
        queue_size = q.count
        failed_count = len(registry)

        # Optionally include popular queries and throughput
        popular = getattr(analytics_service, 'get_popular_queries', lambda n=5: [])(5)

        return {
            'queue_size': queue_size,
            'failed_count': failed_count,
            'pages_crawled': core_metrics.get('pages_crawled', 0),
            'popular_queries': popular,
        }
    except Exception as exc:
        logger.exception('Metrics error: %s', exc)
        raise HTTPException(status_code=500, detail='Failed to fetch crawler metrics') from exc


@router.get('/crawler/failed')
def crawler_failed(db: Session = Depends(get_db)) -> dict:
    """List failed jobs from RQ failed job registry (IDs only)."""
    try:
        from redis import Redis
        from rq import FailedJobRegistry

        redis_url = getattr(__import__('os'), 'environ').get('REDIS_URL', 'redis://localhost:6379/0')
        conn = Redis.from_url(redis_url)
        registry = FailedJobRegistry('crawler', connection=conn)
        failed = list(registry.get_job_ids())
        return {'failed_job_ids': failed, 'count': len(failed)}
    except Exception as exc:
        logger.exception('Failed registry error: %s', exc)
        raise HTTPException(status_code=500, detail='Failed to fetch failed jobs') from exc
