from backend.app.crawler.parser import PageParser


def test_extract_title_and_text():
    html = '<html><head><title>Test Title</title></head><body><p>Hello <strong>World</strong></p><script>ignored()</script></body></html>'
    parser = PageParser()
    assert parser.extract_title(html) == 'Test Title'
    assert 'Hello World' in parser.extract_text(html)


def test_extract_links_resolves_relative_urls_and_normalizes():
    html = '<a href="/about">About</a><a href="http://example.com/contact">Contact</a><a href="mailto:info@example.com">Email</a>'
    parser = PageParser()
    links = parser.extract_links('http://example.com', html)
    assert 'http://example.com/about' in links
    assert 'http://example.com/contact' in links
    assert all(link.startswith('http://') for link in links)
