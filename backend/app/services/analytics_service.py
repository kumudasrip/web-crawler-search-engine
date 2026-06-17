import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.app.models.crawl_job import CrawlJob
from backend.app.models.page import Page as PageModel
from backend.app.models.url import Url as UrlModel


class AnalyticsService:
    """Service layer for analytics and metrics."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.logger = logging.getLogger(__name__)

    def get_analytics(self) -> dict:
        """Get overall crawler and search analytics."""
        pages_crawled = self.db.query(PageModel).filter_by(status='crawled').count()
        unique_urls = self.db.query(UrlModel).count()
        pending_urls = self.db.query(UrlModel).filter_by(status='pending').count()
        failed_urls = self.db.query(PageModel).filter_by(status='failed').count()

        # TODO: Track search queries in a separate table
        search_queries = 0

        # Index size (unique terms)
        # TODO: Implement when term index is available
        index_size = 0

        return {
            'pages_crawled': pages_crawled,
            'unique_urls': unique_urls,
            'pending_urls': pending_urls,
            'failed_urls': failed_urls,
            'search_queries': search_queries,
            'index_size': index_size,
        }

    def get_crawl_job_status(self, job_id: int) -> Optional[dict]:
        """Get status of a specific crawl job."""
        job = self.db.query(CrawlJob).filter_by(id=job_id).one_or_none()
        if not job:
            return None

        return {
            'job_id': job.id,
            'status': job.status,
            'seed_urls': job.seed_urls or [],
            'pages_crawled': self.db.query(PageModel).count(),  # Simplified
            'max_pages': job.max_pages,
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
        }
