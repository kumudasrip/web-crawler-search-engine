from unittest.mock import Mock

import requests

from backend.app.crawler.fetcher import PageFetcher, FetchResult


def test_fetcher_success(monkeypatch):
    mock_response = Mock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.text = '<html></html>'

    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    fetcher = PageFetcher(max_retries=1)
    result = fetcher.fetch('http://example.com')

    assert isinstance(result, FetchResult)
    assert result.success is True
    assert result.status_code == 200
    assert result.content == '<html></html>'


def test_fetcher_retries_on_server_error(monkeypatch):
    responses = []
    first = Mock(ok=False, status_code=500, text='Server Error')
    second = Mock(ok=True, status_code=200, text='<html></html>')
    responses.extend([first, second])

    def fake_get(*args, **kwargs):
        return responses.pop(0)

    monkeypatch.setattr(requests, 'get', fake_get)
    fetcher = PageFetcher(max_retries=1, backoff_factor=0)
    result = fetcher.fetch('http://example.com')

    assert result.success is True
    assert result.status_code == 200


def test_fetcher_returns_error_after_max_retries(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException('timeout')

    monkeypatch.setattr(requests, 'get', fake_get)
    fetcher = PageFetcher(max_retries=1, backoff_factor=0)
    result = fetcher.fetch('http://example.com')

    assert result.success is False
    assert 'timeout' in result.error_message
