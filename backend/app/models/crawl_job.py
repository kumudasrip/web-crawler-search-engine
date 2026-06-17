from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from .base import Base


class CrawlJob(Base):
    __tablename__ = 'crawl_jobs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    seed_urls = Column(ARRAY(Text), nullable=False)
    max_depth = Column(Integer, nullable=False, default=2)
    max_pages = Column(Integer, nullable=False, default=100)
    status = Column(String(32), nullable=False, default='pending')
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
