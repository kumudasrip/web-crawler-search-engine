import logging
from typing import List, Dict

from sqlalchemy.orm import Session

from backend.app.indexer.inverted_index import InvertedIndex
from backend.app.indexer.stop_words import StopWordManager
from backend.app.indexer.tokenizer import Tokenizer
from backend.app.models.page import Page as PageModel
from backend.app.models.page_term import PageTerm


class IndexerService:
    """Service to build and maintain the inverted index."""

    def __init__(self, db: Session) -> None:
        self.db = db
        self.tokenizer = Tokenizer()
        self.stop_word_manager = StopWordManager()
        self.index = InvertedIndex()
        self.logger = logging.getLogger(__name__)

    def index_page(self, page_id: int, title: str, content: str) -> None:
        """
        Index a page: tokenize, filter stop words, and update the index.

        Args:
            page_id: ID of the page to index.
            title: Page title.
            content: Page content.
        """
        # Combine title and content with title weighted
        full_text = f"{title} {title} {content}"

        # Tokenize
        tokens = self.tokenizer.tokenize(full_text)

        # Remove stop words
        filtered_tokens = self.stop_word_manager.filter_stop_words(tokens)

        if not filtered_tokens:
            self.logger.debug('No indexable terms for page %d', page_id)
            return

        # Add to in-memory index
        self.index.index_document(page_id, filtered_tokens)

        # Persist term frequencies to database
        self._persist_terms(page_id, filtered_tokens)

    def _persist_terms(self, page_id: int, terms: List[str]) -> None:
        """Store term frequencies in the database."""
        # Count term frequencies
        term_freq: Dict[str, int] = {}
        for term in terms:
            term_freq[term] = term_freq.get(term, 0) + 1

        # Delete existing terms for this page
        self.db.query(PageTerm).filter_by(page_id=page_id).delete()

        # Insert new terms
        for term, frequency in term_freq.items():
            page_term = PageTerm(
                page_id=page_id,
                term=term,
                frequency=frequency,
            )
            self.db.add(page_term)

        self.db.flush()

    def rebuild_index_from_db(self) -> None:
        """Rebuild the entire in-memory index from the database without mutating stored term data."""
        self.index = InvertedIndex()
        pages = self.db.query(PageModel).all()

        for page in pages:
            if not page.content:
                continue

            if getattr(page, 'terms', None):
                tokens = []
                for page_term in page.terms:
                    tokens.extend([page_term.term] * page_term.frequency)
                self.index.index_document(page.id, tokens)
            else:
                # Fallback if term records are unavailable
                full_text = f"{page.title or ''} {page.title or ''} {page.content}"
                tokens = self.tokenizer.tokenize(full_text)
                filtered_tokens = self.stop_word_manager.filter_stop_words(tokens)
                if filtered_tokens:
                    self.index.index_document(page.id, filtered_tokens)

        self.logger.info('Rebuilt index with %d documents and %d unique terms', self.index.document_count(), self.index.size())

    def get_index(self) -> InvertedIndex:
        """Return the current in-memory inverted index."""
        return self.index

    def search(self, query_terms: List[str]) -> List[int]:
        """Search for pages containing all query terms."""
        filtered = self.stop_word_manager.filter_stop_words(query_terms)
        return list(self.index.search(filtered))
