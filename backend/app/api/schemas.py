from typing import List, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    q: str = Field(..., min_length=1, max_length=500, description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")
    offset: int = Field(default=0, ge=0, description="Pagination offset")

    class Config:
        schema_extra = {
            "example": {
                "q": "machine learning",
                "limit": 10,
                "offset": 0,
            }
        }


class SearchResultItem(BaseModel):
    page_id: int
    title: Optional[str]
    url: Optional[str]
    snippet: str
    score: float

    class Config:
        schema_extra = {
            "example": {
                "page_id": 1,
                "title": "Python Machine Learning Guide",
                "url": "https://example.com/ml-guide",
                "snippet": "Machine learning is a subset of artificial intelligence...",
                "score": 0.85,
            }
        }


class SearchResponse(BaseModel):
    query: str
    total: int
    limit: int
    offset: int
    results: List[SearchResultItem]

    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning",
                "total": 5,
                "limit": 10,
                "offset": 0,
                "results": [
                    {
                        "page_id": 1,
                        "title": "Python ML",
                        "url": "https://example.com/ml",
                        "snippet": "Machine learning...",
                        "score": 0.85,
                    }
                ],
            }
        }


class PageResponse(BaseModel):
    page_id: int
    title: Optional[str]
    url: Optional[str]
    content: str
    http_status: Optional[int]
    crawl_time: str

    class Config:
        schema_extra = {
            "example": {
                "page_id": 1,
                "title": "Example Page",
                "url": "https://example.com",
                "content": "This is the page content...",
                "http_status": 200,
                "crawl_time": "2026-06-17T12:00:00Z",
            }
        }


class AnalyticsResponse(BaseModel):
    pages_crawled: int
    unique_urls: int
    pending_urls: int
    failed_urls: int
    search_queries: int
    index_size: int

    class Config:
        schema_extra = {
            "example": {
                "pages_crawled": 150,
                "unique_urls": 200,
                "pending_urls": 50,
                "failed_urls": 10,
                "search_queries": 500,
                "index_size": 12000,
            }
        }


class CrawlStatusResponse(BaseModel):
    job_id: int
    status: str
    seed_urls: List[str]
    pages_crawled: int
    max_pages: int
    started_at: Optional[str]
    completed_at: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "job_id": 1,
                "status": "running",
                "seed_urls": ["https://example.com"],
                "pages_crawled": 45,
                "max_pages": 100,
                "started_at": "2026-06-17T12:00:00Z",
                "completed_at": None,
            }
        }


class CrawlRequestBody(BaseModel):
    seed_urls: List[str] = Field(..., min_items=1, max_items=10, description="Starting URLs")
    max_depth: int = Field(default=2, ge=1, le=5, description="Crawl depth")
    max_pages: int = Field(default=100, ge=1, le=1000, description="Max pages to crawl")

    class Config:
        schema_extra = {
            "example": {
                "seed_urls": ["https://example.com"],
                "max_depth": 2,
                "max_pages": 100,
            }
        }


class CrawlResponseBody(BaseModel):
    job_id: int
    status: str
    message: str
