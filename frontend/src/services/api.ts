import { SearchResponse, PageContent, Analytics, CrawlStatus, CrawlRequest, CrawlResponse, CrawlerMetrics } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

class ApiService {
  async search(query: string, limit: number = 10, offset: number = 0): Promise<SearchResponse> {
    const params = new URLSearchParams({
      q: query,
      limit: limit.toString(),
      offset: offset.toString(),
    });

    const response = await fetch(`${API_BASE_URL}/search?${params}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Search failed: ${response.statusText}`);
    }

    return response.json();
  }

  async getPage(pageId: number): Promise<PageContent> {
    const response = await fetch(`${API_BASE_URL}/page/${pageId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch page: ${response.statusText}`);
    }

    return response.json();
  }

  async getAnalytics(): Promise<Analytics> {
    const response = await fetch(`${API_BASE_URL}/analytics`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch analytics: ${response.statusText}`);
    }

    return response.json();
  }

  async getCrawlStatus(jobId: number): Promise<CrawlStatus> {
    const response = await fetch(`${API_BASE_URL}/crawl/status/${jobId}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch crawl status: ${response.statusText}`);
    }

    return response.json();
  }

  async getCrawlerMetrics(): Promise<CrawlerMetrics> {
    const response = await fetch(`${API_BASE_URL}/crawler/metrics`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch crawler metrics: ${response.statusText}`);
    }

    return response.json();
  }

  async startCrawl(request: CrawlRequest): Promise<CrawlResponse> {
    const response = await fetch(`${API_BASE_URL}/crawl`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Crawl failed: ${response.statusText}`);
    }

    return response.json();
  }
}

export default new ApiService();
