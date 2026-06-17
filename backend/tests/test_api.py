import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.main import app
from backend.app.core.database import get_db
from backend.app.models.base import Base


# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = 'sqlite:///:memory:'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_root():
    response = client.get('/')
    assert response.status_code == 200
    assert 'app' in response.json()
    assert 'version' in response.json()


def test_search_empty_query():
    response = client.get('/api/search?q=')
    assert response.status_code == 422  # Validation error


def test_search_no_results():
    response = client.get('/api/search?q=nonexistent&limit=10&offset=0')
    assert response.status_code == 200
    data = response.json()
    assert data['query'] == 'nonexistent'
    assert data['total'] == 0
    assert data['results'] == []


def test_search_pagination():
    response = client.get('/api/search?q=python&limit=5&offset=0')
    assert response.status_code == 200
    data = response.json()
    assert data['limit'] == 5
    assert data['offset'] == 0


def test_search_limit_validation():
    response = client.get('/api/search?q=python&limit=200')
    assert response.status_code == 422  # Max limit is 100


def test_get_page_not_found():
    response = client.get('/api/page/999')
    assert response.status_code == 404


def test_analytics():
    response = client.get('/api/analytics')
    assert response.status_code == 200
    data = response.json()
    assert 'pages_crawled' in data
    assert 'unique_urls' in data
    assert 'pending_urls' in data
    assert 'failed_urls' in data
    assert 'search_queries' in data
    assert 'index_size' in data


def test_get_crawl_status_not_found():
    response = client.get('/api/crawl/status/999')
    assert response.status_code == 404


def test_crawl_invalid_request():
    response = client.post('/api/crawl', json={'seed_urls': []})
    assert response.status_code == 422  # min_items validation


def test_crawl_invalid_seed_urls():
    response = client.post(
        '/api/crawl',
        json={'seed_urls': ['https://example.com'] * 20},
    )
    assert response.status_code == 422  # max_items is 10


def test_crawl_max_depth_validation():
    response = client.post(
        '/api/crawl',
        json={
            'seed_urls': ['https://example.com'],
            'max_depth': 10,
            'max_pages': 100,
        },
    )
    assert response.status_code == 422  # max_depth is 5


def test_search_response_schema():
    response = client.get('/api/search?q=test&limit=10&offset=0')
    assert response.status_code == 200
    data = response.json()

    assert 'query' in data
    assert 'total' in data
    assert 'limit' in data
    assert 'offset' in data
    assert 'results' in data
    assert isinstance(data['results'], list)


def test_analytics_response_schema():
    response = client.get('/api/analytics')
    assert response.status_code == 200
    data = response.json()

    required_fields = [
        'pages_crawled',
        'unique_urls',
        'pending_urls',
        'failed_urls',
        'search_queries',
        'index_size',
    ]
    for field in required_fields:
        assert field in data
        assert isinstance(data[field], int)
