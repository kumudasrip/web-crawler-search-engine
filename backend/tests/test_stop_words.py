import pytest

from backend.app.indexer.stop_words import StopWordManager


def test_stop_word_filtering():
    manager = StopWordManager()
    tokens = ['the', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog']
    filtered = manager.filter_stop_words(tokens)
    assert 'the' not in filtered
    assert 'quick' in filtered
    assert 'brown' in filtered
    assert 'fox' in filtered
    assert 'lazy' in filtered
    assert 'dog' in filtered


def test_is_stop_word():
    manager = StopWordManager()
    assert manager.is_stop_word('the') is True
    assert manager.is_stop_word('and') is True
    assert manager.is_stop_word('python') is False


def test_custom_stop_words():
    custom_stops = {'foo', 'bar'}
    manager = StopWordManager(stop_words=custom_stops)
    assert manager.is_stop_word('foo') is True
    assert manager.is_stop_word('bar') is True
    assert manager.is_stop_word('the') is False
