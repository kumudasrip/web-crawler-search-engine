# Phase 4: Inverted Index Implementation

Complete production-ready inverted index and TF-IDF ranking system.

## Modules

### 1. `tokenizer.py`
- `Tokenizer` class: converts text to normalized tokens
- Splits on whitespace and punctuation
- Preserves apostrophes
- Lowercases everything

```python
tokenizer = Tokenizer()
tokens = tokenizer.tokenize("Hello, World!")
# Output: ['hello', 'world']
```

### 2. `stop_words.py`
- `StopWordManager` class: filters common low-value terms
- 155 default English stop words ("the", "and", "is", etc.)
- Can use custom stop word sets

```python
manager = StopWordManager()
filtered = manager.filter_stop_words(['the', 'quick', 'brown', 'fox'])
# Output: ['quick', 'brown', 'fox']
```

### 3. `inverted_index.py`
- `InvertedIndex` class: core data structure
- Maps terms → {page_id: frequency}
- Supports AND/OR searches
- Efficient O(1) lookups

```python
index = InvertedIndex()
index.index_document(1, ['python', 'programming'])
index.index_document(2, ['python', 'machine', 'learning'])

# AND search (pages with ALL terms)
results = index.search(['python', 'machine'])
# Output: set() - no page has both

# OR search (pages with ANY term)
results = index.search_or(['python', 'machine'])
# Output: {1, 2}
```

### 4. `ranker.py`
- `TfIdfRanker` class: TF-IDF scoring and result ranking
- TF = term frequency in document
- IDF = log(total_docs / docs_with_term)
- TF-IDF = TF × IDF

```python
ranker = TfIdfRanker(index)
ranked = ranker.rank_results(['python'], [1, 2, 3])
# Output: [(doc_id, score), ...] sorted by score desc
```

### 5. `indexer_service.py`
- `IndexerService` class: orchestrates indexing workflow
- Integrates with SQLAlchemy and the database
- Persists terms to `page_terms` table
- Can rebuild index from DB

```python
service = IndexerService(db)
service.index_page(1, "Python Guide", "python is great...")
service.rebuild_index_from_db()
```

## Workflow Example

```python
from backend.app.indexer import Tokenizer, StopWordManager, InvertedIndex, TfIdfRanker

# Initialize components
tokenizer = Tokenizer()
stop_words = StopWordManager()
index = InvertedIndex()
ranker = TfIdfRanker(index)

# Index documents
docs = {
    1: "Python is a programming language",
    2: "Python machine learning tutorial",
    3: "Java programming fundamentals"
}

for page_id, content in docs.items():
    tokens = tokenizer.tokenize(content)
    filtered = stop_words.filter_stop_words(tokens)
    index.index_document(page_id, filtered)

# Search and rank
query = "python programming"
query_tokens = stop_words.filter_stop_words(tokenizer.tokenize(query))
results = index.search(query_tokens)
ranked = ranker.rank_results(query_tokens, list(results))
# Output: [(1, 0.81), (2, 0.45)] - highest scoring first
```

## Complexity Summary

| Operation | Time Complexity | Space |
|-----------|-----------------|-------|
| Tokenize N chars | O(N) | O(m) |
| Filter stop words | O(m) | O(m) |
| Index document | O(m) | O(m) |
| Search (AND/OR) | O(q × df) | O(df) |
| Rank results | O(k × q) | O(k) |
| Rebuild from DB | O(n × m) | O(total terms) |

- N = text length
- m = tokens in text
- q = query terms
- df = avg docs per term
- k = result docs
- n = total documents

## Data Persistence

Terms are stored in the `page_terms` table:

```sql
CREATE TABLE page_terms (
    id SERIAL PRIMARY KEY,
    page_id INTEGER NOT NULL,
    term TEXT NOT NULL,
    frequency INTEGER NOT NULL,
    last_updated TIMESTAMP DEFAULT NOW(),
    UNIQUE(page_id, term)
);
```

This enables:
- Recovery of index from database
- Analytics on term popularity
- Transition to external search engines

## Testing

Comprehensive unit tests in `backend/tests/`:
- `test_tokenizer.py`
- `test_stop_words.py`
- `test_inverted_index.py`
- `test_ranker.py`
- `test_indexer_integration.py`

Run with: `pytest backend/tests/`

## Next Steps

Phase 5: FastAPI endpoints for search and crawl control.
