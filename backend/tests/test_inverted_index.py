import pytest

from backend.app.indexer.inverted_index import InvertedIndex


def test_index_document_and_search():
    index = InvertedIndex()
    index.index_document(1, ['python', 'programming', 'language'])
    index.index_document(2, ['python', 'tutorial', 'beginners'])
    index.index_document(3, ['java', 'programming', 'language'])

    # Search for pages with 'python'
    results = index.search(['python'])
    assert results == {1, 2}

    # Search for pages with both 'python' and 'programming'
    results = index.search(['python', 'programming'])
    assert results == {1}

    # OR search
    results = index.search_or(['python', 'java'])
    assert results == {1, 2, 3}


def test_term_and_document_frequency():
    index = InvertedIndex()
    index.index_document(1, ['python', 'python', 'programming'])
    index.index_document(2, ['python', 'tutorial'])

    # Term frequency in doc 1
    assert index.get_term_frequency('python', 1) == 2
    assert index.get_term_frequency('programming', 1) == 1
    assert index.get_term_frequency('python', 2) == 1

    # Document frequency for term
    assert index.get_document_frequency('python') == 2
    assert index.get_document_frequency('programming') == 1
    assert index.get_document_frequency('nonexistent') == 0


def test_remove_document():
    index = InvertedIndex()
    index.index_document(1, ['python', 'programming'])
    index.index_document(2, ['python', 'tutorial'])

    assert index.document_count() == 2
    assert index.get_document_frequency('python') == 2

    index.remove_document(1)

    assert index.document_count() == 1
    assert index.get_document_frequency('python') == 1
    assert index.search(['python']) == {2}


def test_get_terms_for_document():
    index = InvertedIndex()
    index.index_document(1, ['python', 'programming', 'python', 'language'])

    terms = index.get_terms_for_document(1)
    assert terms['python'] == 2
    assert terms['programming'] == 1
    assert terms['language'] == 1
