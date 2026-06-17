import pytest

from backend.app.crawler.normalizer import UrlNormalizer


def test_normalize_strips_default_ports_and_lowercases_scheme():
    normalized = UrlNormalizer.normalize('HTTP://Example.com:80/path/../INDEX.html?b=2&a=1')
    assert normalized == 'http://example.com/INDEX.html?a=1&b=2'


def test_normalize_adds_http_scheme_when_missing():
    normalized = UrlNormalizer.normalize('example.com/path')
    assert normalized.startswith('http://example.com')


def test_normalize_raises_for_empty_url():
    with pytest.raises(ValueError):
        UrlNormalizer.normalize('')
