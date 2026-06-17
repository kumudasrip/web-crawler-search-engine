from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Text, func
from .base import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    url = Column(Text, nullable=False)
    normalized_url = Column(Text, nullable=False, unique=True, index=True)
    url_hash = Column(String(64), nullable=False, unique=True, index=True)
    status = Column(String(32), nullable=False, default='pending')
    retry_count = Column(Integer, nullable=False, default=0)
    next_attempt_at = Column(DateTime(timezone=True), nullable=True)
    last_attempt_at = Column(DateTime(timezone=True), nullable=True)
    last_crawled_at = Column(DateTime(timezone=True), nullable=True)
    first_seen_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
