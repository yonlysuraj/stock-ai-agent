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
    """
    try:
        # Step 1: Fetch historical prices (List of Dicts)
        history = fetch_prices(symbol, period=period)
        
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
                    print(f"Warning: GROQ_API_KEY not found. Skipping sentiment analysis for {symbol}.")
            else:
                 print(f"No news found for {symbol}.")
                 
        except Exception as e:
            print(f"Sentiment analysis failed for {symbol}: {str(e)}")
            sentiment_result = {"error": str(e), "overall_sentiment": "NEUTRAL", "overall_score": 0}

        # Step 3: Compute technical indicators
        indicators = compute_indicators(history)

        # Step 4: Make trading decision
        decision = decide(indicators, sentiment=sentiment_result)

        # Get latest data point
        latest = history[-1]
        current_price = latest["close"]
        
        # Prepare compact price history for frontend charts (most recent 180 points)
        # Data is already dicts, just need to slice
        slice_start = max(0, len(history) - 180)
        price_history = history[slice_start:]
        
        # Ensure 'adj_close' exists (using 'close' as fallback if not present)
        for point in price_history:
            if "adj_close" not in point:
                point["adj_close"] = point["close"]

        # Aggregate and return results
        return {
            "symbol": symbol.upper(),
            "status": "success",
            "data": {
                "current_price": round(current_price, 2),
                "indicators": indicators,
                "sentiment": sentiment_result,
                "decision": decision,
                "price_history_length": len(history),
                "price_history": price_history,
            }
        }
    
    except ValueError as e:
        return {
            "symbol": symbol.upper(),
            "status": "error",
            "error": str(e)
        }
    
    except Exception as e:
        return {
            "symbol": symbol.upper(),
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }
