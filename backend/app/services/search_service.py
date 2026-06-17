import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from backend.app.indexer import IndexerService, TfIdfRanker
from backend.app.models.page import Page as PageModel
from backend.app.models.url import Url as UrlModel


class SearchService:
    """Service layer for search operations."""

    def __init__(self, db: Session, indexer_service: IndexerService) -> None:
        self.db = db
        self.indexer_service = indexer_service
        self.ranker = TfIdfRanker(indexer_service.get_index())
        self.logger = logging.getLogger(__name__)

    def search(self, query: str, limit: int = 10, offset: int = 0) -> tuple[List[dict], int]:
        """
        Execute a search query.

        Args:
            query: Search query string.
            limit: Max results.
            offset: Pagination offset.

        Returns:
            Tuple of (results, total_count).
        """
        query_terms = self.indexer_service.tokenizer.tokenize(query.lower())
        query_terms = self.indexer_service.stop_word_manager.filter_stop_words(query_terms)

        if not query_terms:
            self.logger.warning('Query has no indexable terms: %s', query)
            return [], 0

        # Find pages with query terms
        page_ids = self.indexer_service.search(query_terms)
        total = len(page_ids)

        if not page_ids:
            return [], 0

        # Rank results
        ranked = self.ranker.rank_results(query_terms, list(page_ids))

        # Paginate
        paginated = ranked[offset : offset + limit]

        # Fetch full page details
        results = []
        for page_id, score in paginated:
            page = self.db.query(PageModel).filter_by(id=page_id).one_or_none()
            if not page:
                continue

            snippet = self._generate_snippet(page.content, query_terms)
            results.append(
                {
                    'page_id': page.id,
                    'title': page.title or 'Untitled',
                    'url': page.url.url if page.url else 'N/A',
                    'snippet': snippet,
                    'score': round(score, 4),
                }
            )

        return results, total

    def get_page(self, page_id: int) -> Optional[dict]:
        """Fetch a page by ID."""
        page = self.db.query(PageModel).filter_by(id=page_id).one_or_none()
        if not page:
            return None

        return {
            'page_id': page.id,
            'title': page.title or 'Untitled',
            'url': page.url.url if page.url else 'N/A',
            'content': page.content,
            'http_status': page.http_status,
            'crawl_time': page.crawl_time.isoformat() if page.crawl_time else None,
        }

    def _generate_snippet(self, content: str, query_terms: List[str], length: int = 150) -> str:
        """Generate a search result snippet highlighting query terms."""
        content_lower = content.lower()
        best_pos = 0

        # Find first occurrence of any query term
        for term in query_terms:
            pos = content_lower.find(term)
            if pos >= 0:
                best_pos = max(0, pos - 50)
                break

        snippet = content[best_pos : best_pos + length].strip()
        if len(content) > best_pos + length:
            snippet += '...'

        return snippet
