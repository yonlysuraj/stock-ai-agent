"""
Indicator Agent - Computes technical indicators for stock analysis.

Responsibilities:
- Calculate RSI (Relative Strength Index)
- Calculate Moving Average (20-day)
- Calculate MACD (Moving Average Convergence Divergence)
- Return clean dict with latest indicator values
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional


def compute_rsi(df: pd.DataFrame, period: int = 14) -> float:
    """
    Calculate Relative Strength Index (RSI).
    
    RSI is a momentum oscillator that measures the speed and magnitude of price changes.
    Range: 0-100
    - RSI < 30: Oversold (potential BUY)
    - RSI > 70: Overbought (potential SELL)
    
    Args:
        df: DataFrame with Close prices
        period: RSI period (default: 14 days)
    
    Returns:
        Latest RSI value (float)
    """
    if len(df) < period:
        return 50.0  # Return neutral value if not enough data
    
    # Calculate price changes
    delta = df["Close"].diff()
    
    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = -delta.where(delta < 0, 0)
    
    # Calculate average gains and losses
    avg_gains = gains.rolling(window=period).mean()
    avg_losses = losses.rolling(window=period).mean()
    
    # Calculate Relative Strength
    rs = avg_gains / avg_losses.replace(0, np.nan)
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    # Return latest RSI value
    return float(rsi.iloc[-1]) if not rsi.isna().all() else 50.0


def compute_moving_average(df: pd.DataFrame, period: int = 20) -> float:
    """
    Calculate Simple Moving Average (SMA).
    
    SMA is the average of closing prices over a specified period.
    Used to identify trends and support/resistance levels.
    
    Args:
        df: DataFrame with Close prices
        period: MA period (default: 20 days)
    
    Returns:
        Latest Moving Average value (float)
    """
    if len(df) < period:
        return float(df["Close"].mean())  # Return simple average if not enough data
    
    # Calculate Simple Moving Average
    sma = df["Close"].rolling(window=period).mean()
    
    # Return latest MA value
    return float(sma.iloc[-1]) if not sma.isna().all() else float(df["Close"].iloc[-1])


def compute_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> float:
    """
    Calculate MACD (Moving Average Convergence Divergence).
    
    MACD is a trend-following momentum indicator that shows the relationship between two moving averages.
    - Positive MACD: Bullish (upward momentum)
    - Negative MACD: Bearish (downward momentum)
    
    Args:
        df: DataFrame with Close prices
        fast: Fast EMA period (default: 12)
        slow: Slow EMA period (default: 26)
        signal: Signal line period (default: 9)
    
    Returns:
        MACD value (float) - difference between fast and slow EMAs.
        Returns None if not enough data.
    """
    if len(df) < slow:
        return None  # Not enough data — caller should handle this
    
    # Calculate Exponential Moving Averages
    ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()
    
    # Calculate MACD
    macd = ema_fast - ema_slow
    
    # Return latest MACD value
    return float(macd.iloc[-1]) if not macd.isna().all() else None


def compute_indicators(df: pd.DataFrame) -> Dict[str, Optional[float]]:
    """
    Compute all technical indicators for the given price data.
    
    This is the main function that orchestrates indicator calculations.
    
    Args:
        df: DataFrame with OHLCV data (must have 'Close' column)
    
    Returns:
        Dictionary with indicator values:
        {
            "rsi": float (0-100),
            "ma20": float (price level),
            "macd": float (momentum value) or None if insufficient data
        }
    
    Raises:
        ValueError: If DataFrame is empty or missing Close column
    """
    if df.empty or "Close" not in df.columns:
        raise ValueError("DataFrame must have 'Close' column and be non-empty")
    
    # Calculate all indicators
    rsi = compute_rsi(df, period=14)
    ma20 = compute_moving_average(df, period=20)
    macd = compute_macd(df, fast=12, slow=26, signal=9)
    
    return {
        "rsi": round(rsi, 2),
        "ma20": round(ma20, 2),
        "macd": round(macd, 4) if macd is not None else None
    }
