from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Page:
    url: str
    normalized_url: str
    title: str
    text: str
    links: List[str]
    status_code: Optional[int]
    fetch_success: bool
    error_message: Optional[str] = None
