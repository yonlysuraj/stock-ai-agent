"""
Technical indicators calculation
"""

from typing import List, Tuple


class Indicators:
    """Technical indicators helper class"""
    
    @staticmethod
    def calculate_rsi(prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        return 0.0
    
    @staticmethod
    def calculate_macd(prices: List[float]) -> Tuple[List[float], List[float]]:
        """Calculate MACD"""
        return [], []
    
    @staticmethod
    def calculate_sma(prices: List[float], period: int = 20) -> List[float]:
        """Calculate Simple Moving Average"""
        return []
    
    @staticmethod
    def calculate_ema(prices: List[float], period: int = 20) -> List[float]:
        """Calculate Exponential Moving Average"""
        return []
