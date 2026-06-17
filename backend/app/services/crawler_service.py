import hashlib
import logging
from typing import List, Optional

from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.crawler.crawler import Crawler
from backend.app.crawler.fetcher import PageFetcher
from backend.app.crawler.parser import PageParser
from backend.app.crawler.robots import RobotsTxtManager
from backend.app.models.page import Page as PageModel
from backend.app.models.url import Url as UrlModel
from backend.app.models.page_term import PageTerm


class CrawlerService:
    def __init__(
        self,
        db: Session,
        max_depth: int = 2,
        max_pages: int = 100,
        allowed_domains: Optional[set[str]] = None,
    ) -> None:
        self.db = db
        self.logger = logging.getLogger(__name__)
        self.crawler = Crawler(
            fetcher=PageFetcher(),
            parser=PageParser(),
            robots_manager=RobotsTxtManager(),
            max_depth=max_depth,
            max_pages=max_pages,
            allowed_domains=allowed_domains,
        )

    def crawl_and_store(self, seed_urls: List[str]) -> List[PageModel]:
        pages = self.crawler.crawl(seed_urls)
        stored_pages = []

        for page in pages:
            if not page.normalized_url:
                continue

            url_hash = hashlib.sha256(page.normalized_url.encode('utf-8')).hexdigest()
            url_model = self._get_or_create_url(page.normalized_url, url_hash)

            if not url_model:
                self.logger.warning('Failed to ensure URL record for %s', page.normalized_url)
                continue

            page_model = self._create_or_update_page(page, url_model.id, url_hash)
            if page_model:
                stored_pages.append(page_model)

        self.db.commit()
        return stored_pages

    def _get_or_create_url(self, normalized_url: str, url_hash: str) -> Optional[UrlModel]:
        existing = self.db.query(UrlModel).filter_by(normalized_url=normalized_url).one_or_none()
        if existing:
            return existing

        url_model = UrlModel(
            url=normalized_url,
            normalized_url=normalized_url,
            url_hash=url_hash,
            status='crawled',
            last_crawled_at=None,
        )
        self.db.add(url_model)
        try:
            self.db.flush()
            return url_model
        except IntegrityError:
            self.db.rollback()
            return self.db.query(UrlModel).filter_by(normalized_url=normalized_url).one_or_none()

    def _create_or_update_page(self, page, url_id: int, url_hash: str) -> Optional[PageModel]:
        content_hash = hashlib.sha256((page.text or '').encode('utf-8')).hexdigest() if page.text else None
        existing_page = self.db.query(PageModel).filter_by(url_id=url_id).one_or_none()

        if existing_page and existing_page.content_hash == content_hash:
            self.logger.debug('Skipping unchanged page for %s', page.normalized_url)
            return existing_page

        if existing_page:
            existing_page.title = page.title
            existing_page.content = page.text
            existing_page.content_hash = content_hash
            existing_page.http_status = page.status_code
            existing_page.status = 'crawled' if page.fetch_success else 'failed'
            self.db.add(existing_page)
            return existing_page

        page_model = PageModel(
            url_id=url_id,
            title=page.title,
            content=page.text,
            content_hash=content_hash,
            http_status=page.status_code,
            status='crawled' if page.fetch_success else 'failed',
        )
        self.db.add(page_model)
        return page_model
