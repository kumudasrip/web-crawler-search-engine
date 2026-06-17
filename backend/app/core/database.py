from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Iterator
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://crawler:crawlerpass@localhost:5432/crawler_db')

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Iterator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
