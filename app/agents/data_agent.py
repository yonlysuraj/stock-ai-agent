"""
Data Agent - Fetches historical stock prices using yfinance.

Responsibilities:
- Fetch OHLCV data from Yahoo Finance
- Handle errors gracefully
- Return clean DataFrame with price history
"""

import pandas as pd
import yfinance as yf
from typing import Optional, List, Dict

def fetch_prices(symbol: str, period: str = "1y") -> pd.DataFrame:
    """
    Fetch historical stock prices from Yahoo Finance.
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")
        period: Time period for historical data (default: "1y")
                Options: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    
    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume, Adj Close
        Index: DatetimeIndex with trading dates
    
    Raises:
        ValueError: If symbol is invalid or data cannot be fetched
    """
    try:
        # Fetch data from Yahoo Finance
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        
        # Validate data
        if df.empty:
            raise ValueError(f"No data available for symbol: {symbol}")
        
        # Sort by date ascending (oldest first)
        df = df.sort_index()
        
        return df
    
    except Exception as e:
        raise ValueError(f"Failed to fetch prices for {symbol}: {str(e)}")


def fetch_news(symbol: str, limit: int = 5) -> List[str]:
    """
    Fetch recent news headlines and summaries for a stock.
    
    Args:
        symbol: Stock ticker symbol
        limit: Maximum number of news items to fetch
    
    Returns:
        List of strings, where each string combines title and description
    """
    try:
        ticker = yf.Ticker(symbol)
        news_items = ticker.news or []
        
        texts = []
        for item in news_items[:limit]:
            content = item.get("content", {})
            title = content.get("title", "")
            description = content.get("description", "")
            
            if title:
                text = f"{title}. {description}"
                texts.append(text)
                
        return texts
        
    except Exception:
        # Return empty list on error to allow analysis to proceed without news
        return []
