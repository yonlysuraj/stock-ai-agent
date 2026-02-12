"""
Planner Agent - Orchestrates the stock analysis workflow.

Responsibilities:
- Coordinate all sub-agents (data, indicator, decision, sentiment)
- Fetch prices → Fetch News → Calculate indicators → Analyze Sentiment → Make decision
- Aggregate results and handle errors gracefully
"""

from typing import Dict, Optional, List
import os
from app.agents.data_agent import fetch_prices, fetch_news
from app.agents.indicator_agent import compute_indicators
from app.agents.decision_agent import decide
from app.agents.sentiment_agent import SentimentAgent


def analyze_stock(symbol: str, period: str = "1y") -> Dict:
    """
    Perform complete stock analysis workflow, including Technical and Sentiment analysis.
    
    This function orchestrates the analysis pipeline:
    1. Fetch historical prices (Data Agent)
    2. Fetch recent news (Data Agent)
    3. Compute technical indicators (Indicator Agent)
    4. Analyze news sentiment (Sentiment Agent)
    5. Make trading decision based on ALL signals (Decision Agent)
    
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
                "indicators": { ... },
                "sentiment": { ... } | None,
                "decision": { ... },
                "price_history_length": int
            },
            "error": str (optional)
        }
    """
    try:
        # Step 1: Fetch historical prices
        df = fetch_prices(symbol, period=period)
        
        # Step 2: Fetch News & Analyze Sentiment
        sentiment_result = None
        try:
            news = fetch_news(symbol, limit=5)
            if news:
                # Check for API Key
                api_key = os.getenv("GROQ_API_KEY")
                if api_key:
                    sentiment_agent = SentimentAgent(api_key=api_key)
                    sentiment_result = sentiment_agent.analyze_sentiment(news)
                else:
                    # Log warning or handle silently
                    print(f"Warning: GROQ_API_KEY not found. Skipping sentiment analysis for {symbol}.")
            else:
                 print(f"No news found for {symbol}.")
                 
        except Exception as e:
            print(f"Sentiment analysis failed for {symbol}: {str(e)}")
            # Continue without sentiment
            sentiment_result = {"error": str(e), "overall_sentiment": "NEUTRAL", "overall_score": 0}

        # Step 3: Compute technical indicators
        indicators = compute_indicators(df)

        # Step 4: Make trading decision (combining Technicals + Sentiment)
        decision = decide(indicators, sentiment=sentiment_result)

        # Get current price (latest close)
        current_price = float(df["Close"].iloc[-1])

        # Prepare compact price history for frontend charts (most recent 180 points)
        history_window = df.tail(180).reset_index()
        price_history: List[Dict] = []
        for _, row in history_window.iterrows():
            try:
                ts = row[history_window.columns[0]]
                # Convert Timestamp/Datetime to ISO string
                date_str = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
                price_history.append(
                    {
                        "date": date_str,
                        "open": float(row.get("Open", float("nan"))),
                        "high": float(row.get("High", float("nan"))),
                        "low": float(row.get("Low", float("nan"))),
                        "close": float(row.get("Close", float("nan"))),
                        "adj_close": float(row.get("Adj Close", row.get("Adj_Close", row.get("AdjClose", row.get("Close", float("nan")))))),
                        "volume": float(row.get("Volume", 0.0)),
                    }
                )
            except Exception:
                # Skip any rows that can't be serialized cleanly
                continue

        # Aggregate and return results
        return {
            "symbol": symbol.upper(),
            "status": "success",
            "data": {
                "current_price": round(current_price, 2),
                "indicators": indicators,
                "sentiment": sentiment_result,
                "decision": decision,
                "price_history_length": len(df),
                "price_history": price_history,
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
