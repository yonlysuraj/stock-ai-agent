"""
Data Agent - Fetches historical stock prices using yfinance.

Responsibilities:
- Fetch OHLCV data from Yahoo Finance
- Handle errors gracefully
- Return clean DataFrame with price history
"""

from typing import List, Dict, Any
from app.services.yahoo_finance import fetch_stock_data, fetch_stock_news_manual

def fetch_prices(symbol: str, period: str = "1y") -> List[Dict[str, Any]]:
    """
    Fetch historical stock prices from Yahoo Finance (Lightweight).
    Returns list of dicts: {date, open, high, low, close, volume}
    """
    try:
        data = fetch_stock_data(symbol, period)
        if not data:
            raise ValueError(f"No data available for symbol: {symbol}")
        return data
    except Exception as e:
        raise ValueError(f"Failed to fetch prices for {symbol}: {str(e)}")


def fetch_news(symbol: str, limit: int = 5) -> List[str]:
    """
    Fetch recent news headlines using lightweight service.
    """
    try:
        return fetch_stock_news_manual(symbol, limit)
    except Exception:
        return []
