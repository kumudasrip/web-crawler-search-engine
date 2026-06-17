import pytest

from backend.app.indexer.tokenizer import Tokenizer


def test_tokenizer_splits_and_lowercases():
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("Hello, World! This is a TEST.")
    assert tokens == ['hello', 'world', 'this', 'is', 'a', 'test']


def test_tokenizer_handles_apostrophes():
    tokenizer = Tokenizer()
    tokens = tokenizer.tokenize("It's don't can't")
    assert 'it' in tokens or 'it\'s' in tokens
    assert 'don' in tokens or 'don\'t' in tokens


def test_tokenizer_returns_empty_for_empty_text():
    tokenizer = Tokenizer()
    assert tokenizer.tokenize('') == []
    assert tokenizer.tokenize('   ') == []


def test_normalizer_lowercases_and_strips():
    tokenizer = Tokenizer()
    assert tokenizer.normalize("HELLO") == 'hello'
    assert tokenizer.normalize("'quoted'") == 'quoted'
