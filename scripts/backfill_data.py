"""
Script to backfill historical stock data
"""

from app.integrations.yahoo_finance import YahooFinance


def backfill_data(tickers: list, period: str = "5y"):
    """Backfill historical data for tickers"""
    yahoo = YahooFinance()
    
    for ticker in tickers:
        print(f"Backfilling data for {ticker}...")
        data = yahoo.get_historical_data(ticker, period)
        print(f"Fetched {len(data)} records for {ticker}")


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL"]
    backfill_data(tickers)
