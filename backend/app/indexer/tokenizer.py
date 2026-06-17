import re
from typing import List


class Tokenizer:
    """Tokenizes text into normalized words suitable for indexing."""

    def __init__(self) -> None:
        # Pattern: split on whitespace and punctuation, keep only alphanumeric + apostrophes
        self.pattern = re.compile(r"[\w']+", re.UNICODE)

    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words.

        Args:
            text: Raw text to tokenize.

        Returns:
            List of lowercase words.
        """
        if not text:
            return []

        tokens = self.pattern.findall(text.lower())
        return [token for token in tokens if token]

    def normalize(self, token: str) -> str:
        """Normalize a single token (lowercase, strip punctuation)."""
        normalized = token.lower().strip("'\"")
        return normalized if normalized else ""
