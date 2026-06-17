import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router
from backend.app.core import engine
from backend.app.models import Base

# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title='Web Crawler & Search Engine',
    description='Distributed web crawler and search engine with TF-IDF ranking.',
    version='1.0.0',
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Include routes
app.include_router(router)


@app.get('/health')
def health_check() -> dict:
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'Web Crawler & Search Engine is running'}


@app.get('/')
def root() -> dict:
    """Root endpoint with API info."""
    return {
        'app': 'Web Crawler & Search Engine',
        'version': '1.0.0',
        'docs': '/docs',
        'endpoints': [
            'GET /search',
            'GET /page/{id}',
            'GET /analytics',
            'GET /crawl/status/{job_id}',
            'POST /crawl',
        ],
    }
