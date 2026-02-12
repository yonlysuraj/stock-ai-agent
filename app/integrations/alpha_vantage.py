"""
Alpha Vantage integration
"""

from typing import Dict, List
from app.config import settings


class AlphaVantage:
    """Alpha Vantage API wrapper"""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self):
        """Initialize Alpha Vantage client"""
        self.api_key = settings.ALPHA_VANTAGE_API_KEY
    
    def get_times_series(self, ticker: str, function: str = "TIME_SERIES_DAILY") -> Dict:
        """Get time series data"""
        return {
            "ticker": ticker,
            "function": function,
            "data": []
        }
    
    def get_technical_indicator(self, ticker: str, indicator: str) -> Dict:
        """Get technical indicator"""
        return {}
