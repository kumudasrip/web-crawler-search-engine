from unittest.mock import Mock

import requests

from backend.app.crawler.robots import RobotsTxtManager


def test_robots_txt_blocks_disallowed_paths(monkeypatch):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = 'User-agent: *\nDisallow: /private\n'

    monkeypatch.setattr(requests, 'get', lambda *args, **kwargs: mock_response)
    manager = RobotsTxtManager()

    assert manager.can_fetch('http://example.com/public') is True
    assert manager.can_fetch('http://example.com/private') is False
