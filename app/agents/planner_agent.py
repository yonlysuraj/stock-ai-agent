"""
Planner Agent - Orchestrates the stock analysis workflow.

Responsibilities:
- Coordinate all sub-agents (data, indicator, decision)
- Fetch prices → Calculate indicators → Make decision
- Aggregate results and handle errors gracefully
"""

from typing import Dict
from app.agents.data_agent import fetch_prices
from app.agents.indicator_agent import compute_indicators
from app.agents.decision_agent import decide


def analyze_stock(symbol: str, period: str = "1y") -> Dict:
    """
    Perform complete stock analysis workflow.
    
    This function orchestrates the analysis pipeline:
    1. Fetch historical prices (Data Agent)
    2. Compute technical indicators (Indicator Agent)
    3. Make trading decision (Decision Agent)
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
        period: Historical data period (default: "1y")
               Options: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    
    Returns:
        Dictionary containing complete analysis:
        {
            "symbol": str,
            "status": "success" | "error",
            "data": {
                "current_price": float,
                "indicators": {
                    "rsi": float,
                    "ma20": float,
                    "macd": float
                },
                "decision": {
                    "action": "BUY" | "SELL" | "HOLD",
                    "confidence": float,
                    "reason": str
                },
                "price_history_length": int
            },
            "error": str (optional, if status is "error")
        }
    
    Raises:
        None - Errors are caught and returned in response dict
    """
    try:
        # Step 1: Fetch historical prices
        df = fetch_prices(symbol, period=period)
        
        # Step 2: Compute technical indicators
        indicators = compute_indicators(df)
        
        # Step 3: Make trading decision
        decision = decide(indicators)
        
        # Get current price (latest close)
        current_price = float(df["Close"].iloc[-1])
        
        # Aggregate and return results
        return {
            "symbol": symbol.upper(),
            "status": "success",
            "data": {
                "current_price": round(current_price, 2),
                "indicators": indicators,
                "decision": decision,
                "price_history_length": len(df)
            }
        }
    
    except ValueError as e:
        # Handle validation errors
        return {
            "symbol": symbol.upper(),
            "status": "error",
            "error": str(e)
        }
    
    except Exception as e:
        # Handle unexpected errors
        return {
            "symbol": symbol.upper(),
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }
