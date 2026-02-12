"""
Request schemas
"""

from pydantic import BaseModel
from typing import Optional, List


class StockAnalysisRequest(BaseModel):
    """Stock analysis request"""
    ticker: str
    timeframe: Optional[str] = "1y"
    indicators: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticker": "AAPL",
                "timeframe": "1y",
                "indicators": ["RSI", "MACD", "SMA"]
            }
        }


class PortfolioRequest(BaseModel):
    """Portfolio creation request"""
    name: str
    description: Optional[str] = None
    stocks: Optional[List[dict]] = None


class BacktestRequest(BaseModel):
    """Backtest request"""
    ticker: str
    start_date: str
    end_date: str
    initial_capital: float = 10000.0
