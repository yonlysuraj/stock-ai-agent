"""
Script to run backtesting
"""

from app.services.backtest_service import BacktestService


def run_backtest(ticker: str, start_date: str, end_date: str):
    """Run backtest for a ticker"""
    service = BacktestService()
    result = service.backtest_strategy(ticker, start_date, end_date)
    
    print(f"Backtest Results for {ticker}:")
    print(f"Initial Capital: ${result['initial_capital']:.2f}")
    print(f"Final Value: ${result['final_value']:.2f}")
    print(f"Returns: {result['returns']:.2%}")


if __name__ == "__main__":
    run_backtest("AAPL", "2022-01-01", "2023-01-01")
