"""
SQLAlchemy models for database
"""

from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Stock(Base):
    """Stock model"""
    __tablename__ = "stocks"
    
    id = Column(String, primary_key=True)
    ticker = Column(String, unique=True, index=True)
    name = Column(String)
    price = Column(Float)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Portfolio(Base):
    """Portfolio model"""
    __tablename__ = "portfolios"
    
    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalysisResult(Base):
    """Analysis result model"""
    __tablename__ = "analysis_results"
    
    id = Column(String, primary_key=True)
    ticker = Column(String, index=True)
    recommendation = Column(String)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
