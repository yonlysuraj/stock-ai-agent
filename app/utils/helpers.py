"""
Helper functions
"""

from datetime import datetime, timedelta
from typing import List


def format_date(date: datetime) -> str:
    """Format date to string"""
    return date.strftime("%Y-%m-%d")


def get_date_range(days: int) -> tuple:
    """Get date range for last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    return start_date, end_date


def round_to_decimals(value: float, decimals: int = 2) -> float:
    """Round value to specified decimals"""
    return round(value, decimals)
