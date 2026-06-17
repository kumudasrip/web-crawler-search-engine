from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship
from .base import Base


class Page(Base):
    __tablename__ = 'pages'

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey('urls.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    title = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    content_hash = Column(String(64), nullable=True)
    http_status = Column(Integer, nullable=True)
    status = Column(String(32), nullable=False, default='crawled')
    crawl_time = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    url = relationship('Url', backref='page')
