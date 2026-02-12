"""
Script to seed database with initial data
"""

from app.data.database import SessionLocal
from app.data.models import Stock


def seed_stocks():
    """Seed stocks table"""
    db = SessionLocal()
    
    stocks = [
        Stock(id="1", ticker="AAPL", name="Apple Inc.", price=150.0),
        Stock(id="2", ticker="MSFT", name="Microsoft Corp.", price=300.0),
        Stock(id="3", ticker="GOOGL", name="Alphabet Inc.", price=2800.0),
    ]
    
    for stock in stocks:
        db.add(stock)
    
    db.commit()
    print("Database seeded successfully!")


if __name__ == "__main__":
    seed_stocks()
