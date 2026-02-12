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
        interval = "1d"
        range_param = period
        
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

def fetch_stock_news_manual(symbol, limit=5):
    """
    Fetch news from Yahoo Finance Search API.
    """
    try:
        # Search API often returns news
        url = f"https://query1.finance.yahoo.com/v1/finance/search"
        params = {
            "q": symbol,
            "quotesCount": 0,
            "newsCount": limit
        }
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        
        texts = []
        if "news" in data:
            for item in data["news"]:
                title = item.get("title", "")
                link = item.get("link", "")
                texts.append(f"{title}. {link}")
                
        return texts
    except Exception:
        return []
