# Phase 4 — Inverted Index & TF-IDF Ranking

## Overview

The inverted index is the core data structure for the search engine.
It maps terms (words) to the pages (documents) that contain them.

## Data Structures

### InvertedIndex
- `index: Dict[str, Dict[int, int]]`
- Structure: `term -> {page_id: frequency}`
- `doc_count: int` — total indexed documents

### Example
```
Page 1: "python programming language"
Page 2: "python machine learning"
Page 3: "java programming"

Inverted Index:
{
    'python': {1: 1, 2: 1},
    'programming': {1: 1, 3: 1},
    'language': {1: 1},
    'machine': {2: 1},
    'learning': {2: 1},
    'java': {3: 1}
}
```

## Components

### 1. Tokenizer
- Splits text on whitespace and punctuation
- Lowercases all tokens
- Uses regex pattern: `[\w']+` to preserve apostrophes
- Removes empty strings

**Complexity**: O(n) where n = text length

### 2. StopWordManager
- Maintains set of ~155 common English words
- Filters out low-value terms like "the", "and", "is"
- Reduces index size and improves ranking signal

**Complexity**: O(1) per word check, O(m) for batch filtering where m = word count

### 3. InvertedIndex
Core operations:

#### index_document(page_id, terms)
- Creates a term frequency map
- Inserts into `index[term][page_id]`
- **Complexity**: O(m) where m = unique terms in document

#### search(terms) — AND search
- Finds docs containing ALL query terms
- Uses set intersection: `set.intersection(*result_sets)`
- **Complexity**: O(q * avg_df) where q = query terms, avg_df = avg docs per term

#### search_or(terms) — OR search
- Finds docs containing ANY query term
- Union of all result sets
- **Complexity**: O(q * avg_df)

#### get_term_frequency(term, page_id)
- Direct dict lookup
- **Complexity**: O(1)

#### get_document_frequency(term)
- Returns `len(index[term])`
- **Complexity**: O(1)

### 4. TfIdfRanker

#### TF (Term Frequency)
```
TF(term, doc) = frequency of term in doc
```
- Raw frequency stored during indexing
- **Complexity**: O(1) lookup

#### IDF (Inverse Document Frequency)
```
IDF(term) = log(total_docs / docs_with_term)
```
- Weights rare terms higher
- Common words have low IDF, rare words have high IDF
- **Complexity**: O(1)

#### TF-IDF Score
```
TF-IDF(term, doc) = TF(term, doc) × IDF(term)
```

#### Ranking
- For multi-term queries, sum TF-IDF scores across all terms
- Sort results descending by score
- **Complexity**: O(k * q) where k = result docs, q = query terms

## Complexity Analysis Summary

| Operation | Time | Space |
|-----------|------|-------|
| Index document | O(m) | O(m) |
| Search (AND) | O(q * df) | O(df) |
| Search (OR) | O(q * df) | O(df) |
| Lookup TF | O(1) | — |
| Lookup DF | O(1) | — |
| Rank results | O(k * q) | O(k) |
| Rebuild index | O(n * m) | O(total terms) |

Where:
- n = total documents
- m = avg terms per document
- q = query terms
- df = avg documents per term
- k = result documents

## Phrase Search Preparation

While full phrase search is not implemented yet, the current structure supports it:

1. Store term positions during tokenization
2. Expand PageTerm model to include position data
3. After AND search, verify query terms are adjacent/ordered

**Example**:
```python
query = "machine learning"
pages = index.search(['machine', 'learning'])  # Finds candidates
# Then verify 'machine' and 'learning' are adjacent in found pages
```

## Example Outputs

### Scenario 1: Simple AND Search

**Indexed Pages**:
- Page 1: "Python is a programming language"
- Page 2: "Java is a programming language"
- Page 3: "Python machine learning tutorial"

**Query**: "python programming"

**Steps**:
1. Tokenize: ['python', 'programming']
2. Remove stop words: ['python', 'programming'] (no change)
3. Find pages with 'python': {1, 3}
4. Find pages with 'programming': {1, 2}
5. AND: {1, 3} ∩ {1, 2} = {1}

**Result**: [Page 1]

### Scenario 2: TF-IDF Ranking

**Indexed Pages**:
- Page 1: "python python learning" (TF(python)=2)
- Page 2: "python machine learning" (TF(python)=1)
- Page 3: "machine learning tutorial" (TF(python)=0)

**Index**:
```
'python': {1: 2, 2: 1}  (DF=2)
```

**Query**: "python"

**Calculation**:
- IDF(python) = log(3/2) ≈ 0.405
- TF-IDF(python, Page 1) = 2 × 0.405 = 0.81
- TF-IDF(python, Page 2) = 1 × 0.405 = 0.405

**Ranked Results**:
1. Page 1 (score: 0.81)
2. Page 2 (score: 0.405)

### Scenario 3: Multi-term Query

**Query**: "python machine learning"

**Found Pages**: {1, 2, 3}

**Scores**:
- Page 1: TF-IDF(python) + 0 + TF-IDF(learning)
- Page 2: TF-IDF(python) + TF-IDF(machine) + TF-IDF(learning)
- Page 3: 0 + TF-IDF(machine) + TF-IDF(learning)

**Result**: Ranked by aggregate score

## Integration

The `IndexerService` ties everything together:

```python
service = IndexerService(db)
service.index_page(1, "Python Basics", "python is a programming language")
service.rebuild_index_from_db()
```

This:
1. Tokenizes title and content
2. Filters stop words
3. Updates in-memory `InvertedIndex`
4. Persists terms to `page_terms` table

## Space Complexity

For N documents with average M unique terms:
- **In-memory index**: O(N * M) in worst case
- **Database storage**: O(N * M) for page_terms table

For a typical corpus (1M pages, 50 unique terms avg):
- ~50M index entries
- With each entry ~50 bytes: ~2.5 GB memory
- Production systems use specialized engines (Elasticsearch) for scale

## Optimization Opportunities

1. **Stemming**: Reduce 'running', 'runs', 'run' to single stem 'run'
2. **N-grams**: Support partial matching and typo tolerance
3. **Field boosting**: Weight title matches higher than body text
4. **Caching**: Cache computed IDF scores
5. **Compression**: Use bit vectors for large inverted indexes
