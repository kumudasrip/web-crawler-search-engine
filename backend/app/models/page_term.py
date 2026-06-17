from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, func
from sqlalchemy.orm import relationship
from .base import Base


class PageTerm(Base):
    __tablename__ = 'page_terms'

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey('pages.id', ondelete='CASCADE'), nullable=False, index=True)
    term = Column(Text, nullable=False, index=True)
    frequency = Column(Integer, nullable=False, default=0)
    last_updated = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    page = relationship('Page', backref='terms')
