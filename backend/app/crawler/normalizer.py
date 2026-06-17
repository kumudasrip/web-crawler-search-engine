from urllib.parse import parse_qsl, quote, unquote, urlencode, urlparse, urlunparse
import posixpath


class UrlNormalizer:
    @staticmethod
    def normalize(url: str) -> str:
        if not url or not url.strip():
            raise ValueError('URL must be a non-empty string')

        parsed = urlparse(url.strip())

        scheme = parsed.scheme.lower() if parsed.scheme else 'http'
        netloc = parsed.netloc.lower()

        if not netloc and parsed.path:
            parsed = parsed._replace(path='', scheme=scheme, netloc=parsed.path)
            netloc = parsed.netloc.lower()

        if scheme == 'http' and netloc.endswith(':80'):
            netloc = netloc[:-3]
        if scheme == 'https' and netloc.endswith(':443'):
            netloc = netloc[:-4]

        raw_path = unquote(parsed.path or '/')
        normalized_path = posixpath.normpath(raw_path)
        if normalized_path == '.':
            normalized_path = '/'
        if not normalized_path.startswith('/'):
            normalized_path = '/' + normalized_path
        if raw_path.endswith('/') and not normalized_path.endswith('/'):
            normalized_path += '/'

        query_items = parse_qsl(parsed.query, keep_blank_values=True)
        sorted_query = sorted(query_items)
        normalized_query = urlencode(sorted_query, doseq=True)

        normalized = urlunparse(
            (
                scheme,
                netloc,
                quote(normalized_path, safe='/%'),
                '',
                normalized_query,
                '',
            )
        )
        return normalized