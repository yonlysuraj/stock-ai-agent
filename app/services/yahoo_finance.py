import requests
import json
from datetime import datetime
import time

def fetch_stock_data(symbol, period="1y"):
    """
    Fetch historical stock data manually from Yahoo Finance Chart API.
    Avoids using pandas/yfinance to keep bundle size small for Vercel.
    """
    try:
        # 1. Convert period to interval and range
        range_param = period
        interval = "1d"
        
        if period in ["1d", "5d"]:
            interval = "15m"
        elif period in ["1mo", "3mo"]:
            interval = "1d" # Explicitly 1d

        
        # Yahoo API endpoint
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {
            "interval": interval,
            "range": range_param
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # 2. Parse response
        result = data["chart"]["result"][0]
        meta = result["meta"]
        timestamps = result["timestamp"]
        indicators = result["indicators"]["quote"][0]
        
        closes = indicators["close"]
        opens = indicators["open"]
        highs = indicators["high"]
        lows = indicators["low"]
        volumes = indicators["volume"]
        
        # 3. Structure data as list of dicts (lightweight DataFrame replacement)
        # Filter out None values (market holidays/errors)
        history = []
        for i in range(len(timestamps)):
            if closes[i] is None:
                continue
            history.append({
                "date": datetime.fromtimestamp(timestamps[i]).strftime('%Y-%m-%d'),
                "open": opens[i],
                "high": highs[i],
                "low": lows[i],
                "close": closes[i],
                "volume": volumes[i]
            })
            
        return history
        
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return []

def fetch_stock_news_rich(symbol, limit=5):
    """
    Fetch rich news objects for the frontend.
    Returns list of dicts: {title, description, source, date, url, thumbnail}
    """
    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search"
        params = {
            "q": symbol,
            "quotesCount": 0,
            "newsCount": limit
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        articles = []
        if "news" in data:
            for item in data["news"]:
                # Extract image if available
                thumbnail = None
                if "thumbnail" in item and "resolutions" in item["thumbnail"]:
                    res = item["thumbnail"]["resolutions"]
                    if res:
                        thumbnail = res[-1]["url"]
                
                pub_date = ""
                if "providerPublishTime" in item:
                    pub_date = datetime.fromtimestamp(item["providerPublishTime"]).isoformat()

                articles.append({
                    "id": item.get("uuid", ""),
                    "title": item.get("title", ""),
                    "description": item.get("type", ""), # Search API doesn't give full desc
                    "source": item.get("publisher", "Yahoo Finance"),
                    "date": pub_date,
                    "url": item.get("link", ""),
                    "thumbnail": thumbnail
                })
        return articles
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []

def fetch_stock_news_manual(symbol, limit=5):
    """
    Fetch news strings for Sentiment Analysis agent.
    Returns list of strings: "Title. Link"
    """
    rich_news = fetch_stock_news_rich(symbol, limit)
    return [f"{a['title']}. {a['url']}" for a in rich_news]
