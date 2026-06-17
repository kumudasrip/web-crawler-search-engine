import pytest
from unittest.mock import Mock

from backend.app.crawler.crawler import Crawler
from backend.app.crawler.fetcher import FetchResult
from backend.app.crawler.parser import PageParser
from backend.app.crawler.robots import RobotsTxtManager


class DummyFetcher:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    def fetch(self, url):
        self.calls.append(url)
        return self.responses.pop(0)


class DummyRobots(RobotsTxtManager):
    def __init__(self, allowed=True):
        super().__init__()
        self.allowed = allowed

    def can_fetch(self, url):
        return self.allowed


def test_crawler_extracts_page_data_and_links(monkeypatch):
    html = '<html><head><title>Example</title></head><body><p>Hello world</p><a href="/about">About</a></body></html>'
    fetch_result = FetchResult(
        url='http://example.com',
        normalized_url='http://example.com/',
        success=True,
        content=html,
        status_code=200,
    )

    fetcher = DummyFetcher([fetch_result])
    crawler = Crawler(fetcher=fetcher, robots_manager=DummyRobots(), max_depth=0)
    pages = crawler.crawl(['http://example.com'])

    assert len(pages) == 1
    page = pages[0]
    assert page.title == 'Example'
    assert 'Hello world' in page.text
    assert page.links == ['http://example.com/about']
    assert page.fetch_success is True


def test_crawler_respects_robots_txt(monkeypatch):
    fetch_result = FetchResult(
        url='http://example.com',
        normalized_url='http://example.com/',
        success=True,
        content='<html></html>',
        status_code=200,
    )

    fetcher = DummyFetcher([fetch_result])
    crawler = Crawler(fetcher=fetcher, robots_manager=DummyRobots(allowed=False))
    pages = crawler.crawl(['http://example.com'])

    assert len(pages) == 0


def test_crawler_handles_broken_urls(monkeypatch):
    fetch_result = FetchResult(
        url='http://invalid.example',
        normalized_url='http://invalid.example/',
        success=False,
        content=None,
        status_code=None,
        error_message='DNS failure',
    )

    fetcher = DummyFetcher([fetch_result])
    crawler = Crawler(fetcher=fetcher, robots_manager=DummyRobots())
    pages = crawler.crawl(['http://invalid.example'])

    assert len(pages) == 1
    assert pages[0].fetch_success is False
    assert pages[0].error_message == 'DNS failure'


def test_crawler_respects_max_depth(monkeypatch):
    html1 = '<html><body><a href="/page2">Page 2</a></body></html>'
    html2 = '<html><body><p>Deep</p></body></html>'

    fetcher = DummyFetcher([
        FetchResult(url='http://example.com', normalized_url='http://example.com/', success=True, content=html1, status_code=200),
        FetchResult(url='http://example.com/page2', normalized_url='http://example.com/page2', success=True, content=html2, status_code=200),
    ])

    crawler = Crawler(fetcher=fetcher, robots_manager=DummyRobots(), max_depth=0)
    pages = crawler.crawl(['http://example.com'])

    assert len(pages) == 1
    assert pages[0].links == ['http://example.com/page2']
