import logging
from collections import deque
from typing import Deque, Dict, Iterable, List, Optional, Set
from urllib.parse import urlparse

from .fetcher import FetchResult, PageFetcher
from .parser import PageParser
from .robots import RobotsTxtManager
from .types import Page
from .normalizer import UrlNormalizer


class Crawler:
    def __init__(
        self,
        fetcher: Optional[PageFetcher] = None,
        parser: Optional[PageParser] = None,
        robots_manager: Optional[RobotsTxtManager] = None,
        max_depth: int = 2,
        max_pages: int = 100,
        allowed_domains: Optional[Set[str]] = None,
    ) -> None:
        self.fetcher = fetcher or PageFetcher()
        self.parser = parser or PageParser()
        self.robots_manager = robots_manager or RobotsTxtManager()
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.allowed_domains = allowed_domains
        self.logger = logging.getLogger(__name__)

    def crawl(self, seed_urls: Iterable[str]) -> List[Page]:
        queue: Deque[Dict[str, int]] = deque()
        visited: Set[str] = set()
        results: List[Page] = []

        for raw_url in seed_urls:
            try:
                normalized = UrlNormalizer.normalize(raw_url)
                queue.append({'url': normalized, 'depth': 0})
            except ValueError:
                self.logger.warning('Seed URL was invalid and skipped: %s', raw_url)

        while queue and len(results) < self.max_pages:
            item = queue.popleft()
            url = item['url']
            depth = item['depth']

            if url in visited:
                continue
            visited.add(url)

            if self.allowed_domains and self._is_external(url):
                self.logger.debug('Skipping external URL: %s', url)
                continue

            if not self.robots_manager.can_fetch(url):
                self.logger.info('Blocked by robots.txt: %s', url)
                continue

            fetch_result = self.fetcher.fetch(url)
            page = self._build_page(fetch_result)
            results.append(page)

            if not fetch_result.success:
                continue

            if depth < self.max_depth:
                links = self.parser.extract_links(fetch_result.normalized_url, fetch_result.content or '')
                for link in links:
                    if link not in visited:
                        queue.append({'url': link, 'depth': depth + 1})

        return results

    def _build_page(self, fetch_result: FetchResult) -> Page:
        if not fetch_result.success or not fetch_result.content:
            return Page(
                url=fetch_result.url,
                normalized_url=fetch_result.normalized_url,
                title='',
                text='',
                links=[],
                status_code=fetch_result.status_code,
                fetch_success=False,
                error_message=fetch_result.error_message,
            )

        title = self.parser.extract_title(fetch_result.content)
        text = self.parser.extract_text(fetch_result.content)
        links = self.parser.extract_links(fetch_result.normalized_url, fetch_result.content)

        return Page(
            url=fetch_result.url,
            normalized_url=fetch_result.normalized_url,
            title=title,
            text=text,
            links=links,
            status_code=fetch_result.status_code,
            fetch_success=True,
        )

    def _is_external(self, url: str) -> bool:
        if not self.allowed_domains:
            return False

        normalized = UrlNormalizer.normalize(url)
        parsed = urlparse(normalized)
        netloc = parsed.netloc.lower()
        return netloc not in {domain.lower() for domain in self.allowed_domains}
