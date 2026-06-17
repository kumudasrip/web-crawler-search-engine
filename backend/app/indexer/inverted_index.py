from collections import defaultdict
from typing import Dict, List, Set


class InvertedIndex:
    """
    In-memory inverted index mapping terms to document IDs and frequencies.

    Structure: term -> {page_id: frequency}

    Supports O(1) lookup and efficient ranking.
    """

    def __init__(self) -> None:
        self.index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.doc_count = 0

    def index_document(self, page_id: int, terms: List[str]) -> None:
        """
        Add a document (page) to the index with its terms.

        Args:
            page_id: ID of the page.
            terms: List of terms to index.
        """
        term_freq: Dict[str, int] = defaultdict(int)
        for term in terms:
            term_freq[term] += 1

        for term, freq in term_freq.items():
            self.index[term][page_id] = freq

        self.doc_count += 1

    def remove_document(self, page_id: int) -> None:
        """Remove a document from the index."""
        for term in list(self.index.keys()):
            if page_id in self.index[term]:
                del self.index[term][page_id]
            if not self.index[term]:
                del self.index[term]

        self.doc_count = max(0, self.doc_count - 1)

    def search(self, terms: List[str]) -> Set[int]:
        """
        Find documents containing all query terms (AND search).

        Args:
            terms: Query terms.

        Returns:
            Set of page IDs that contain all terms.

        Time complexity: O(n * m) where n = unique terms, m = avg docs per term
        """
        if not terms:
            return set()

        result_sets = [set(self.index.get(term, {}).keys()) for term in terms]
        return set.intersection(*result_sets) if result_sets else set()

    def search_or(self, terms: List[str]) -> Set[int]:
        """
        Find documents containing any query term (OR search).

        Args:
            terms: Query terms.

        Returns:
            Set of page IDs that contain any term.
        """
        result = set()
        for term in terms:
            result.update(self.index.get(term, {}).keys())
        return result

    def get_term_frequency(self, term: str, page_id: int) -> int:
        """Get the frequency of a term in a document."""
        return self.index.get(term, {}).get(page_id, 0)

    def get_document_frequency(self, term: str) -> int:
        """Get the number of documents containing a term."""
        return len(self.index.get(term, {}))

    def get_terms_for_document(self, page_id: int) -> Dict[str, int]:
        """Get all terms and their frequencies for a document."""
        result = {}
        for term, docs in self.index.items():
            if page_id in docs:
                result[term] = docs[page_id]
        return result

    def get_all_terms(self) -> Set[str]:
        """Get all unique terms in the index."""
        return set(self.index.keys())

    def size(self) -> int:
        """Return the number of unique terms in the index."""
        return len(self.index)

    def document_count(self) -> int:
        """Return the total number of indexed documents."""
        return self.doc_count
