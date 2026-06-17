-- Distributed Web Crawler and Search Engine PostgreSQL schema

-- Enums for status tracking
CREATE TYPE crawl_job_status AS ENUM ('pending', 'running', 'completed', 'failed', 'cancelled');
CREATE TYPE url_status AS ENUM ('pending', 'queued', 'in_progress', 'crawled', 'failed', 'skipped');
CREATE TYPE page_status AS ENUM ('crawled', 'failed', 'stale');
CREATE TYPE search_metric AS ENUM ('search_query', 'result_click', 'crawl_error', 'url_discovery');

-- Core page storage table
CREATE TABLE pages (
    id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    url_id BIGINT NOT NULL,
    title TEXT,
    content TEXT NOT NULL,
    content_hash TEXT,
    http_status SMALLINT,
    status page_status NOT NULL DEFAULT 'crawled',
    crawl_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pages_url_id_fkey FOREIGN KEY (url_id) REFERENCES urls (id) ON DELETE RESTRICT,
    CONSTRAINT pages_url_unique UNIQUE (url_id)
);

-- URL deduplication and crawl queue support
CREATE TABLE urls (
    id BIGSERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    normalized_url TEXT NOT NULL,
    url_hash TEXT NOT NULL,
    canonical_url TEXT NOT NULL,
    status url_status NOT NULL DEFAULT 'pending',
    retry_count INTEGER NOT NULL DEFAULT 0,
    next_attempt_at TIMESTAMPTZ,
    last_attempt_at TIMESTAMPTZ,
    last_crawled_at TIMESTAMPTZ,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT urls_normalized_url_unique UNIQUE (normalized_url),
    CONSTRAINT urls_url_hash_unique UNIQUE (url_hash)
);

-- Crawl jobs and metadata
CREATE TABLE crawl_jobs (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    seed_urls TEXT[] NOT NULL,
    max_depth INTEGER NOT NULL DEFAULT 2,
    max_pages INTEGER NOT NULL DEFAULT 100,
    status crawl_job_status NOT NULL DEFAULT 'pending',
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    metrics JSONB DEFAULT '{}'::JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE crawl_job_urls (
    id BIGSERIAL PRIMARY KEY,
    job_id BIGINT NOT NULL,
    url_id BIGINT NOT NULL,
    depth INTEGER NOT NULL DEFAULT 0,
    status url_status NOT NULL DEFAULT 'pending',
    retries INTEGER NOT NULL DEFAULT 0,
    last_attempt_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    error_message TEXT,
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT crawl_job_urls_job_fkey FOREIGN KEY (job_id) REFERENCES crawl_jobs (id) ON DELETE CASCADE,
    CONSTRAINT crawl_job_urls_url_fkey FOREIGN KEY (url_id) REFERENCES urls (id) ON DELETE CASCADE,
    CONSTRAINT crawl_job_urls_unique_job_url UNIQUE (job_id, url_id)
);

-- Inverted index for search
CREATE TABLE page_terms (
    id BIGSERIAL PRIMARY KEY,
    page_id BIGINT NOT NULL,
    term TEXT NOT NULL,
    term_frequency INTEGER NOT NULL DEFAULT 0,
    document_frequency INTEGER NOT NULL DEFAULT 0,
    last_updated TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT page_terms_page_fkey FOREIGN KEY (page_id) REFERENCES pages (id) ON DELETE CASCADE,
    CONSTRAINT page_terms_unique UNIQUE (page_id, term)
);

-- Aggregated search analytics counters
CREATE TABLE analytics_counters (
    metric TEXT PRIMARY KEY,
    value BIGINT NOT NULL DEFAULT 0,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Detailed search analytics events
CREATE TABLE search_analytics (
    id BIGSERIAL PRIMARY KEY,
    event_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metric_type search_metric NOT NULL,
    query TEXT,
    page_id BIGINT,
    result_count INTEGER,
    metadata JSONB DEFAULT '{}'::JSONB,
    CONSTRAINT search_analytics_page_fkey FOREIGN KEY (page_id) REFERENCES pages (id) ON DELETE SET NULL
);

-- Indexes for performance
CREATE INDEX idx_urls_normalized_url ON urls (normalized_url);
CREATE INDEX idx_urls_url_hash ON urls (url_hash);
CREATE INDEX idx_urls_status_next_attempt ON urls (status, next_attempt_at);
CREATE INDEX idx_pages_url_id ON pages (url_id);
CREATE INDEX idx_pages_crawl_time ON pages (crawl_time DESC);
CREATE INDEX idx_crawl_job_urls_job_id ON crawl_job_urls (job_id);
CREATE INDEX idx_crawl_job_urls_status ON crawl_job_urls (status);
CREATE INDEX idx_page_terms_term ON page_terms (term);
CREATE INDEX idx_page_terms_page_id ON page_terms (page_id);
CREATE INDEX idx_search_analytics_event_time ON search_analytics (event_time);
CREATE INDEX idx_search_analytics_metric_type ON search_analytics (metric_type);

-- Optional full-text support for page content
ALTER TABLE pages ADD COLUMN IF NOT EXISTS content_vector tsvector;
CREATE INDEX IF NOT EXISTS idx_pages_content_vector ON pages USING GIN (content_vector);
