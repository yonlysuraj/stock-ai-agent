"""
Decision Agent - Makes simple rule-based trading decisions.

Responsibilities:
- Analyze technical indicators
- Apply rule-based trading logic
- Return trading action (BUY/SELL/HOLD) with confidence and reasoning
"""

from typing import Dict, Literal, Optional


def decide(indicators: Dict[str, Optional[float]]) -> Dict:
    """
    Make trading decision based on technical indicators using simple rules.
    
    Trading Rules:
    - RSI < 30: OVERSOLD → BUY signal (confidence: 0.8)
    - RSI > 70: OVERBOUGHT → SELL signal (confidence: 0.8)
    - RSI 30-70: NEUTRAL → HOLD signal (confidence: 0.5)
    
    Additional signals from MACD and MA20 are used to adjust confidence.
    
    Args:
        indicators: Dictionary with keys:
                   - "rsi" (float, 0-100): Relative Strength Index
                   - "ma20" (float): 20-period Moving Average
                   - "macd" (float or None): MACD momentum value
    
    Returns:
        Dictionary with:
        {
            "action": "BUY" | "SELL" | "HOLD",
            "confidence": float (0.0-1.0),
            "reason": str (human-readable explanation)
        }
    
    Raises:
        ValueError: If required indicators are missing
    """
    # Validate input
    required_keys = {"rsi", "ma20", "macd"}
    if not required_keys.issubset(indicators.keys()):
        raise ValueError(f"Missing required indicators. Need: {required_keys}")
    
    rsi = indicators["rsi"]
    ma20 = indicators["ma20"]
    macd = indicators["macd"]  # Can be None if insufficient data
    
    # Base decision logic using RSI
    if rsi < 30:
        action = "BUY"
        confidence = 0.8
        reason = f"RSI {rsi:.1f} indicates oversold condition"
        
        # Boost confidence if MACD is positive (upward momentum)
        if macd is not None and macd > 0:
            confidence = 0.9
            reason += " and MACD shows positive momentum"
        elif macd is None:
            reason += " (MACD unavailable — insufficient data)"
        
    elif rsi > 70:
        action = "SELL"
        confidence = 0.8
        reason = f"RSI {rsi:.1f} indicates overbought condition"
        
        # Boost confidence if MACD is negative (downward momentum)
        if macd is not None and macd < 0:
            confidence = 0.9
            reason += " and MACD shows negative momentum"
        elif macd is None:
            reason += " (MACD unavailable — insufficient data)"
    
    else:
        # Neutral zone (30 <= RSI <= 70)
        action = "HOLD"
        confidence = 0.5
        reason = f"RSI {rsi:.1f} is in neutral zone"
        
        # Try to determine slight bias from MACD
        if macd is not None:
            if macd > 0.01:
                confidence = 0.6
                reason += " with slight bullish bias (positive MACD)"
            elif macd < -0.01:
                confidence = 0.6
                reason += " with slight bearish bias (negative MACD)"
        else:
            reason += " (MACD unavailable — need 26+ data points)"
    
    return {
        "action": action,
        "confidence": round(confidence, 2),
        "reason": reason
    }
