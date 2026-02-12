"""
Repository pattern for database operations
"""

from sqlalchemy.orm import Session
from app.data.models import Stock, Portfolio, AnalysisResult


class StockRepository:
    """Repository for stock operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_stock(self, ticker: str):
        """Get stock by ticker"""
        return self.db.query(Stock).filter(Stock.ticker == ticker).first()
    
    def create_stock(self, ticker: str, name: str, price: float):
        """Create new stock"""
        stock = Stock(ticker=ticker, name=name, price=price)
        self.db.add(stock)
        self.db.commit()
        return stock


class PortfolioRepository:
    """Repository for portfolio operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_portfolio(self, portfolio_id: str):
        """Get portfolio by ID"""
        return self.db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()


class AnalysisRepository:
    """Repository for analysis operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_analysis(self, ticker: str, recommendation: str, confidence: float):
        """Save analysis result"""
        result = AnalysisResult(ticker=ticker, recommendation=recommendation, confidence=confidence)
        self.db.add(result)
        self.db.commit()
        return result
