import logging
import time
from dataclasses import dataclass
from typing import Optional

import requests

from .normalizer import UrlNormalizer


@dataclass
class FetchResult:
    url: str
    normalized_url: str
    success: bool
    content: Optional[str]
    status_code: Optional[int]
    error_message: Optional[str] = None


class PageFetcher:
    def __init__(self, timeout: int = 10, max_retries: int = 2, backoff_factor: float = 0.5, user_agent: str = 'web-crawler-search-engine'):
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.user_agent = user_agent
        self.logger = logging.getLogger(__name__)

    def fetch(self, url: str) -> FetchResult:
        normalized_url = UrlNormalizer.normalize(url)
        last_error = None

        for attempt in range(1, self.max_retries + 2):
            try:
                response = requests.get(
                    normalized_url,
                    timeout=self.timeout,
                    headers={'User-Agent': self.user_agent},
                )
                status_code = response.status_code

                if response.ok:
                    return FetchResult(
                        url=url,
                        normalized_url=normalized_url,
                        success=True,
                        content=response.text,
                        status_code=status_code,
                    )

                error_message = f'HTTP {status_code}'
                self.logger.warning('Fetch failed %s (%s): %s', normalized_url, status_code, error_message)

                if attempt <= self.max_retries and status_code >= 500:
                    self._sleep_backoff(attempt)
                    continue

                return FetchResult(
                    url=url,
                    normalized_url=normalized_url,
                    success=False,
                    content=None,
                    status_code=status_code,
                    error_message=error_message,
                )

            except requests.RequestException as exc:
                last_error = str(exc)
                self.logger.warning('Fetch exception for %s: %s', normalized_url, exc)
                if attempt <= self.max_retries:
                    self._sleep_backoff(attempt)
                    continue

        return FetchResult(
            url=url,
            normalized_url=normalized_url,
            success=False,
            content=None,
            status_code=None,
            error_message=last_error,
        )

    def _sleep_backoff(self, attempt: int) -> None:
        delay = self.backoff_factor * (2 ** (attempt - 1))
        self.logger.debug('Retrying after %.1f seconds', delay)
        time.sleep(delay)