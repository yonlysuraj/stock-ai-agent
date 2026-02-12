"""
Stock Analysis Routes - FastAPI endpoints for stock analysis.

Responsibilities:
- Define REST API endpoints
- Handle HTTP requests
- Call planner agent, report agent, and sentiment agent
- Return JSON responses

"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List
import yfinance as yf
from app.agents.planner_agent import analyze_stock
from app.agents.report_agent import ReportAgent
from app.agents.sentiment_agent import SentimentAgent
from app.api.schemas.request import StockAnalysisRequest
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create router instance
router = APIRouter()

# Initialize agents
report_agent = ReportAgent()


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    texts: List[str]


@router.get("/analyze/{symbol}")
async def analyze_stock_endpoint(
    symbol: str,
    period: str = Query("1y", description="Historical data period")
) -> Dict[str, Any]:
    """
    Analyze a stock and return trading recommendation.
    
    Endpoint: GET /api/stocks/analyze/{symbol}
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
        period: Historical data period (default: "1y")
               Options: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    
    Returns:
        JSON response with stock analysis results including:
        - symbol, status, current_price
        - indicators (RSI, MA20, MACD)
        - decision (action, confidence, reason)
        - price history length
    
    Example:
        GET /api/stocks/analyze/AAPL
        GET /api/stocks/analyze/MSFT?period=6mo
    """
    # Validate symbol (basic check)
    if not symbol or len(symbol) > 5:
        raise HTTPException(status_code=400, detail="Invalid stock symbol")
    
    # Perform analysis
    result = analyze_stock(symbol, period=period)
    
    # Handle errors
    if result.get("status") == "error":
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Analysis failed")
        )
    
    return result


@router.get("/report/{symbol}")
async def generate_report_endpoint(
    symbol: str,
    period: str = Query("1y", description="Historical data period")
) -> Dict[str, Any]:
    """
    Generate comprehensive analysis report for a stock.
    
    Endpoint: GET /api/stocks/report/{symbol}
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")
        period: Historical data period (default: "1y")
    
    Returns:
        Comprehensive report containing:
        - Symbol and timestamp
        - Summary and current price
        - Technical indicators with interpretations
        - Trading decision with confidence
        - Risk assessment
        - Final recommendation
    
    Example:
        GET /api/stocks/report/AAPL
    """
    if not symbol or len(symbol) > 5:
        raise HTTPException(status_code=400, detail="Invalid stock symbol")
    
    try:
        # First perform analysis
        analysis_result = analyze_stock(symbol, period=period)
        
        if analysis_result.get("status") == "error":
            raise HTTPException(
                status_code=400,
                detail=analysis_result.get("error", "Analysis failed")
            )
        
        # Generate report using ReportAgent
        report = report_agent.generate_report(symbol, analysis_result)
        
        return report
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")


@router.post("/sentiment/analyze")
async def analyze_sentiment_endpoint(request: SentimentRequest) -> Dict[str, Any]:
    """
    Analyze sentiment of financial news texts using Groq LLM.
    
    Endpoint: POST /api/stocks/sentiment/analyze
    
    Args:
        texts: List of text strings to analyze
    
    Returns:
        Sentiment analysis results:
        - texts_analyzed: Number of texts
        - overall_sentiment: POSITIVE, NEGATIVE, or NEUTRAL
        - overall_score: Average score (-1 to 1)
        - individual_scores: Score for each text
        - interpretations: Explanation for each text
        - confidence: Overall confidence score
        - summary: Text summary
    
    Example:
        POST /api/stocks/sentiment/analyze
        {
            "texts": [
                "Apple reported strong Q4 earnings",
                "Markets decline on recession fears"
            ]
        }
    """
    if not request.texts or len(request.texts) == 0:
        raise HTTPException(status_code=400, detail="At least one text is required")
    
    try:
        # Verify API key is available
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise HTTPException(
                status_code=503,
                detail="Sentiment analysis service not configured (missing GROQ_API_KEY)"
            )
        
        # Initialize sentiment agent with API key
        sentiment_agent = SentimentAgent(api_key=api_key)
        
        # Analyze sentiment
        result = sentiment_agent.analyze_sentiment(request.texts)
        
        return {
            "status": "success",
            "analysis": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sentiment analysis failed: {str(e)}")


@router.post("/analyze")
async def analyze_stock_from_request(request: StockAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze stock using request body (alternative to path parameter).
    
    Endpoint: POST /api/stocks/analyze
    
    Args:
        StockAnalysisRequest with:
        - ticker: Stock symbol
        - timeframe: Historical period (optional, default: "1y")
        - indicators: List of indicators to compute (optional)
    
    Returns:
        Stock analysis results
    
    Example:
        POST /api/stocks/analyze
        {
            "ticker": "AAPL",
            "timeframe": "6mo",
            "indicators": ["RSI", "MACD", "SMA"]
        }
    """
    if not request.ticker:
        raise HTTPException(status_code=400, detail="Ticker is required")
    
    result = analyze_stock(request.ticker, period=request.timeframe)
    
    if result.get("status") == "error":
        raise HTTPException(
            status_code=400,
            detail=result.get("error", "Analysis failed")
        )
    
    return result


@router.get("/news/{symbol}")
async def get_stock_news(
    symbol: str,
    limit: int = Query(10, description="Max number of news items", ge=1, le=20)
) -> Dict[str, Any]:
    """
    Fetch recent financial news for a stock ticker using Yahoo Finance (free).
    
    Endpoint: GET /api/stocks/news/{symbol}
    
    Args:
        symbol: Stock ticker symbol (e.g., "AAPL")
        limit: Max number of news items to return (default: 10, max: 20)
    
    Returns:
        List of news articles with title, description, source, date, url, thumbnail
    """
    if not symbol or len(symbol) > 12:
        raise HTTPException(status_code=400, detail="Invalid stock symbol")
    
    try:
        ticker = yf.Ticker(symbol)
        raw_news = ticker.news or []
        
        articles = []
        for item in raw_news[:limit]:
            content = item.get("content", {})
            if not content:
                continue
            
            # Extract thumbnail URL
            thumbnail = None
            thumb_data = content.get("thumbnail")
            if thumb_data:
                resolutions = thumb_data.get("resolutions", [])
                if resolutions:
                    thumbnail = resolutions[-1].get("url")  # highest resolution
            
            # Extract article URL
            url = None
            click_url = content.get("clickThroughUrl")
            if click_url:
                url = click_url.get("url")
            if not url:
                canonical = content.get("canonicalUrl")
                if canonical:
                    url = canonical.get("url")
            
            # Extract provider name
            provider = content.get("provider", {})
            source = provider.get("displayName", "Unknown")
            
            articles.append({
                "id": content.get("id", ""),
                "title": content.get("title", ""),
                "description": content.get("description", ""),
                "source": source,
                "date": content.get("pubDate", ""),
                "url": url,
                "thumbnail": thumbnail,
            })
        
        return {
            "status": "success",
            "symbol": symbol.upper(),
            "count": len(articles),
            "articles": articles
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")
