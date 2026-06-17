# Database Schema

## Tables

### `pages`

- `id` SERIAL PRIMARY KEY
- `url` TEXT UNIQUE NOT NULL
- `normalized_url` TEXT NOT NULL
- `title` TEXT
- `content` TEXT NOT NULL
- `crawl_time` TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
- `status` TEXT NOT NULL DEFAULT 'crawled'
- `http_status` INTEGER
- `error_message` TEXT

### `inverted_index`

- `id` SERIAL PRIMARY KEY
- `term` TEXT NOT NULL
- `page_id` INTEGER NOT NULL REFERENCES pages(id) ON DELETE CASCADE
- `term_frequency` INTEGER NOT NULL
- `document_frequency` INTEGER NOT NULL DEFAULT 0
- `updated_at` TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()

- Unique constraint: `(term, page_id)`

### `crawled_urls`

- `id` SERIAL PRIMARY KEY
- `url` TEXT UNIQUE NOT NULL
- `normalized_url` TEXT NOT NULL
- `hash` TEXT NOT NULL
- `first_seen` TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
- `last_crawled` TIMESTAMP WITH TIME ZONE
- `status` TEXT NOT NULL DEFAULT 'pending'
- `retry_count` INTEGER NOT NULL DEFAULT 0

### `analytics`

- `id` SERIAL PRIMARY KEY
- `metric` TEXT NOT NULL
- `value` BIGINT NOT NULL DEFAULT 0
- `updated_at` TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()

## Indexes

- `pages(url)` unique index
- `pages(normalized_url)` index
- `inverted_index(term)` index
- `inverted_index(page_id)` index
- `crawled_urls(hash)` unique index
- `analytics(metric)` unique index

## Notes

- `normalized_url` is used for deduplication of URL forms like `google.com` and `google.com/`.
- `inverted_index` stores `term_frequency` for TF scoring and `document_frequency` for IDF.
- `analytics` is a lightweight counter store that can support dashboard metrics.
