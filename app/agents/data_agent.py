"""
Data Agent - Fetches historical stock prices using yfinance.

Responsibilities:
- Fetch OHLCV data from Yahoo Finance
- Handle errors gracefully
- Return clean DataFrame with price history
"""

import pandas as pd
import yfinance as yf
from typing import Optional


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
