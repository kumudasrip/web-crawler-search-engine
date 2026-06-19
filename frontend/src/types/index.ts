// Search and page types
export interface SearchResult {
  page_id: number;
  title: string;
  url: string;
  snippet: string;
  score: number;
}

export interface SearchResponse {
  query: string;
  total: number;
  limit: number;
  offset: number;
  results: SearchResult[];
}

export interface PageContent {
  page_id: number;
  title: string;
  url: string;
  content: string;
  http_status: number | null;
  crawl_time: string;
}

// Analytics types
export interface Analytics {
  pages_crawled: number;
  unique_urls: number;
  pending_urls: number;
  failed_urls: number;
  search_queries: number;
  index_size: number;
}

export interface PopularQuery {
  query: string;
  count: number;
}

export interface CrawlerMetrics {
  queue_size: number;
  failed_count: number;
  pages_crawled: number;
  popular_queries: PopularQuery[];
}

// Crawl job types
export interface CrawlStatus {
  job_id: number;
  status: string;
  seed_urls: string[];
  pages_crawled: number;
  max_pages: number;
  started_at: string | null;
  completed_at: string | null;
}

export interface CrawlRequest {
  seed_urls: string[];
  max_depth: number;
  max_pages: number;
}

export interface CrawlResponse {
  job_id: number;
  status: string;
  message: string;
}
