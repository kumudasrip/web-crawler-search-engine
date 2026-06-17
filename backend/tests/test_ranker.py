import pytest
import math

from backend.app.indexer.inverted_index import InvertedIndex
from backend.app.indexer.ranker import TfIdfRanker


def test_tf_idf_ranking():
    index = InvertedIndex()
    index.index_document(1, ['python', 'programming', 'tutorial'])
    index.index_document(2, ['python', 'python', 'machine', 'learning'])
    index.index_document(3, ['machine', 'learning', 'deep', 'learning'])

    ranker = TfIdfRanker(index)

    # Compute TF for 'python' in doc 1
    tf_python_doc1 = ranker.compute_tf('python', 1)
    assert tf_python_doc1 == 1.0

    # Compute IDF for 'python' (in 2 of 3 docs)
    idf_python = ranker.compute_idf('python')
    expected_idf = math.log(3 / 2)
    assert abs(idf_python - expected_idf) < 0.01

    # Rank results for query 'python'
    ranked = ranker.rank_results(['python'], [1, 2, 3])
    # Doc 2 has 'python' twice, so should rank higher
    assert ranked[0][0] == 2  # doc 2
    assert ranked[0][1] > ranked[1][1]  # doc 2 score > doc 1 score


def test_tf_idf_rare_term():
    index = InvertedIndex()
    index.index_document(1, ['common', 'word'])
    index.index_document(2, ['common', 'word'])
    index.index_document(3, ['common', 'rare'])

    ranker = TfIdfRanker(index)

    # 'rare' appears in 1 of 3 docs, so higher IDF
    idf_rare = ranker.compute_idf('rare')
    idf_common = ranker.compute_idf('common')
    assert idf_rare > idf_common
