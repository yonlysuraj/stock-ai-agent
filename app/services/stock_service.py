"""
Stock Service - Business logic for stock operations
"""

from app.agents.planner_agent import PlannerAgent
from app.agents.data_agent import DataAgent
from app.agents.indicator_agent import IndicatorAgent
from app.agents.sentiment_agent import SentimentAgent
from app.agents.decision_agent import DecisionAgent


class StockService:
    """Service for stock analysis operations"""
    
    def __init__(self):
        """Initialize stock service"""
        self.planner = PlannerAgent()
        self.data_agent = DataAgent()
        self.indicator_agent = IndicatorAgent()
        self.sentiment_agent = SentimentAgent()
        self.decision_agent = DecisionAgent()
    
    def analyze_stock(self, ticker: str, timeframe: str = "1y"):
        """Analyze a stock"""
        plan = self.planner.plan(ticker)
        data = self.data_agent.fetch_stock_data(ticker, timeframe)
        indicators = self.indicator_agent.calculate_indicators(data["data"])
        decision = self.decision_agent.decide(ticker, indicators, {})
        return decision
