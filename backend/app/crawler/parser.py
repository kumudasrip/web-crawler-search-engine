import logging
from typing import List
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .normalizer import UrlNormalizer


class PageParser:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def extract_title(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('title')
        return title_tag.get_text(strip=True) if title_tag else ''

    def extract_text(self, html: str) -> str:
        soup = BeautifulSoup(html, 'html.parser')
        for element in soup(['script', 'style', 'noscript']):
            element.extract()
        text = soup.get_text(separator=' ', strip=True)
        return ' '.join(text.split())

    def extract_links(self, base_url: str, html: str) -> List[str]:
        soup = BeautifulSoup(html, 'html.parser')
        parsed_base = urlparse(base_url)
        links: List[str] = []

        for anchor in soup.find_all('a', href=True):
            href = anchor.get('href').strip()
            if not href or href.startswith(('mailto:', 'javascript:', '#')):
                continue

            full_url = urljoin(base_url, href)
            try:
                normalized = UrlNormalizer.normalize(full_url)
            except ValueError:
                self.logger.debug('Skipping invalid extracted URL: %s', full_url)
                continue

            parsed = urlparse(normalized)
            if parsed.scheme not in ('http', 'https'):
                continue

            links.append(normalized)

        return list(dict.fromkeys(links))
