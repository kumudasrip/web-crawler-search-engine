import pytest

from backend.app.indexer import Tokenizer, StopWordManager, InvertedIndex, TfIdfRanker


def test_end_to_end_indexing_and_ranking():
    """Full workflow: tokenize, filter, index, and rank."""
    
    tokenizer = Tokenizer()
    stop_words = StopWordManager()
    index = InvertedIndex()
    ranker = TfIdfRanker(index)
    
    # Document 1: "python is a great programming language"
    page_1_text = "python is a great programming language"
    tokens_1 = tokenizer.tokenize(page_1_text)
    filtered_1 = stop_words.filter_stop_words(tokens_1)
    index.index_document(1, filtered_1)
    
    # Document 2: "python machine learning deep learning"
    page_2_text = "python machine learning deep learning"
    tokens_2 = tokenizer.tokenize(page_2_text)
    filtered_2 = stop_words.filter_stop_words(tokens_2)
    index.index_document(2, filtered_2)
    
    # Document 3: "java is a great programming language"
    page_3_text = "java is a great programming language"
    tokens_3 = tokenizer.tokenize(page_3_text)
    filtered_3 = stop_words.filter_stop_words(tokens_3)
    index.index_document(3, filtered_3)
    
    # Query 1: "python"
    query_1 = stop_words.filter_stop_words(tokenizer.tokenize("python"))
    results_1 = index.search(query_1)
    assert results_1 == {1, 2}
    
    # Rank results
    ranked_1 = ranker.rank_results(query_1, list(results_1))
    assert ranked_1[0][0] == 2  # doc 2 has 'python' once + 'learning' twice
    
    # Query 2: "python programming"
    query_2 = stop_words.filter_stop_words(tokenizer.tokenize("python programming"))
    results_2 = index.search(query_2)
    assert results_2 == {1}
    
    # Query 3: "learning" (OR search)
    query_3 = stop_words.filter_stop_words(tokenizer.tokenize("learning language"))
    results_3 = index.search_or(query_3)
    assert 1 in results_3
    assert 2 in results_3
    assert 3 in results_3
