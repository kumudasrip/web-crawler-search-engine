import logging
from typing import Dict
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests

from .normalizer import UrlNormalizer


class RobotsTxtManager:
    def __init__(self, user_agent: str = 'web-crawler-search-engine', timeout: int = 5):
        self.user_agent = user_agent
        self.timeout = timeout
        self.parsers: Dict[str, RobotFileParser] = {}
        self.logger = logging.getLogger(__name__)

    def can_fetch(self, url: str) -> bool:
        normalized_url = UrlNormalizer.normalize(url)
        parsed = urlparse(normalized_url)
        origin = f'{parsed.scheme}://{parsed.netloc}'

        if origin not in self.parsers:
            self.parsers[origin] = self._load_robots_parser(origin)

        parser = self.parsers[origin]
        try:
            return parser.can_fetch(self.user_agent, normalized_url)
        except Exception as exc:
            self.logger.warning('Robots parser error for %s: %s', origin, exc)
            return True

    def _load_robots_parser(self, origin: str) -> RobotFileParser:
        robots_url = urljoin(origin, '/robots.txt')
        parser = RobotFileParser()
        parser.set_url(robots_url)

        try:
            response = requests.get(robots_url, timeout=self.timeout, headers={'User-Agent': self.user_agent})
            if response.status_code == 200:
                parser.parse(response.text.splitlines())
            else:
                self.logger.debug('Robots.txt not found or unavailable for %s: status %s', origin, response.status_code)
                parser.parse(['User-agent: *', 'Allow: /'])
        except requests.RequestException as exc:
            self.logger.warning('Failed to fetch robots.txt for %s: %s', origin, exc)
            parser.parse(['User-agent: *', 'Allow: /'])

        return parser