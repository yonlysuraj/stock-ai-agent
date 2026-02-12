"""
Indicator Agent - Computes technical indicators for stock analysis.

Responsibilities:
- Calculate RSI (Relative Strength Index)
- Calculate Moving Average (20-day)
- Calculate MACD (Moving Average Convergence Divergence)
- Return clean dict with latest indicator values
"""

from typing import List, Dict, Optional

def compute_rsi(prices: List[float], period: int = 14) -> float:
    if len(prices) < period + 1:
        return 50.0

    gains = []
    losses = []
    
    # Calculate initial changes
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
            
    # Calculate initial average
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    # Smooth (Wilder's Smoothing)
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
    if avg_loss == 0:
        return 100.0
        
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return float(rsi)

def compute_moving_average(prices: List[float], period: int = 20) -> float:
    if len(prices) < period:
        return sum(prices) / len(prices) if prices else 0.0
    
    # Simple Moving Average of the last 'period' items
    return sum(prices[-period:]) / period

def compute_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Optional[float]:
    if len(prices) < slow:
        return None
        
    # Calculate EMA manually
    def calculate_ema(data, span):
        alpha = 2 / (span + 1)
        ema = [data[0]]
        for price in data[1:]:
            ema.append(alpha * price + (1 - alpha) * ema[-1])
        return ema

    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    
    # MACD Line = Fast EMA - Slow EMA
    macd_line = []
    min_len = min(len(ema_fast), len(ema_slow))
    
    # Align lists (though they should be same length)
    for i in range(min_len):
        macd_line.append(ema_fast[i] - ema_slow[i])
        
    # We only need the latest value of the Histogram/Signal? 
    # Usually MACD returned is the MACD line value or Histogram. 
    # The previous code returned "macd", which was diff between fast and slow.
    
    return float(macd_line[-1])

def compute_indicators(history: List[Dict]) -> Dict[str, Optional[float]]:
    """
    Compute indicators using list of historical data.
    Args:
        history: List of dicts with 'close' key.
    """
    if not history:
        raise ValueError("No data to compute indicators")

    # Extract closing prices
    closes = [day["close"] for day in history]
    
    rsi = compute_rsi(closes)
    ma20 = compute_moving_average(closes)
    macd = compute_macd(closes)
    
    return {
        "rsi": round(rsi, 2),
        "ma20": round(ma20, 2),
        "macd": round(macd, 4) if macd is not None else None
    }
