"""
Custom exceptions
"""


class StockAIException(Exception):
    """Base exception for Stock AI Agent"""
    pass


class StockNotFoundError(StockAIException):
    """Raised when stock is not found"""
    pass


class PortfolioNotFoundError(StockAIException):
    """Raised when portfolio is not found"""
    pass


class DataFetchError(StockAIException):
    """Raised when data fetch fails"""
    pass


class AnalysisError(StockAIException):
    """Raised when analysis fails"""
    pass
