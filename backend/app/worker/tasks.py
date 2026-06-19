import logging
from backend.app.worker.queue import get_redis_conn
from backend.app.core import get_db, SessionLocal
from backend.app.services.crawler_service import CrawlerService

logger = logging.getLogger(__name__)


def crawl_job(seed_url: str, job_meta: dict | None = None) -> dict:
    """Worker task: crawl a single seed URL (or small set) and store results.

    Designed to be enqueued into Redis/RQ as a distributed worker task.
    """
    session = SessionLocal()
    try:
        crawler = CrawlerService(session)
        pages = crawler.crawl_and_store([seed_url])
        return {"seed": seed_url, "pages_crawled": len(pages)}
    except Exception as exc:
        logger.exception('crawl_job failed for %s: %s', seed_url, exc)
        raise
    finally:
        session.close()
