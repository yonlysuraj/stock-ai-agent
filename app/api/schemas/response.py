"""
Response schemas
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any


class StockAnalysisResponse(BaseModel):
    """Stock analysis response"""
    ticker: str
    recommendation: str
    confidence: float
    signal: Optional[str] = None
    analysis_date: Optional[str] = None
    technical_indicators: Optional[Dict[str, Any]] = None


class PortfolioResponse(BaseModel):
    """Portfolio response"""
    id: str
    name: str
    total_value: float
    stocks_count: int


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    code: Optional[int] = None
