import math
from collections import Counter
from typing import Dict, List, Optional, Tuple

from backend.app.indexer.inverted_index import InvertedIndex


class TfIdfRanker:
    """TF-IDF ranker for documents stored in an in-memory inverted index."""

    def __init__(self, index: InvertedIndex) -> None:
        self.index = index

    def compute_tf(self, term: str, page_id: int) -> float:
        """Compute term frequency using logarithmic normalization."""
        freq = self.index.get_term_frequency(term, page_id)
        if freq <= 0:
            return 0.0
        return 1.0 + math.log(freq)

    def compute_idf(self, term: str) -> float:
        """Compute inverse document frequency for a term."""
        document_count = self.index.document_count()
        df = self.index.get_document_frequency(term)
        if df <= 0 or document_count <= 0:
            return 0.0
        return math.log(document_count / df)

    def _query_vector(self, query_terms: List[str]) -> Tuple[Dict[str, float], float]:
        query_freq = Counter(query_terms)
        weights: Dict[str, float] = {}

        for term, freq in query_freq.items():
            idf = self.compute_idf(term)
            if idf <= 0.0:
                continue
            qtf = 1.0 + math.log(freq)
            weights[term] = qtf * idf

        norm = math.sqrt(sum(weight * weight for weight in weights.values()))
        return weights, norm

    def _document_norm(self, page_id: int) -> float:
        term_freqs = self.index.get_terms_for_document(page_id)
        if not term_freqs:
            return 0.0

        total = 0.0
        for term in term_freqs.keys():
            tf = self.compute_tf(term, page_id)
            idf = self.compute_idf(term)
            total += (tf * idf) ** 2

        return math.sqrt(total)

    def score_document(self, query_terms: List[str], page_id: int) -> float:
        """Compute a normalized TF-IDF score for a single document."""
        if not query_terms:
            return 0.0

        query_weights, query_norm = self._query_vector(query_terms)
        if query_norm <= 0.0:
            return 0.0

        numerator = 0.0
        for term, query_weight in query_weights.items():
            tf = self.compute_tf(term, page_id)
            if tf <= 0.0:
                continue
            doc_weight = tf * self.compute_idf(term)
            numerator += doc_weight * query_weight

        doc_norm = self._document_norm(page_id)
        if doc_norm <= 0.0:
            return 0.0

        return numerator / (doc_norm * query_norm)

    def rank_results(self, query_terms: List[str], page_ids: List[int], top_k: Optional[int] = None) -> List[tuple[int, float]]:
        """Rank documents for a query and return ordered (page_id, score) pairs."""
        if not query_terms or not page_ids:
            return []

        scores = []
        for page_id in page_ids:
            score = self.score_document(query_terms, page_id)
            if score > 0.0:
                scores.append((page_id, score))

        scores.sort(key=lambda item: (-item[1], item[0]))

        if top_k is not None and top_k >= 0:
            return scores[:top_k]
        return scores
