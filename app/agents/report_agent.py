"""
Report Agent - Generates analysis reports

Responsibilities:
- Format analysis results into readable reports
- Include summary, indicators, decision, and recommendations
- Add timestamp and metadata
"""

from datetime import datetime
from typing import Dict, Optional


class ReportAgent:
    """Agent responsible for generating comprehensive analysis reports"""
    
    def __init__(self):
        """Initialize report agent"""
        self.report_version = "1.0"
    
    def generate_report(self, ticker: str, analysis_data: dict) -> Dict:
        """
        Generate a comprehensive analysis report from stock analysis data.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            analysis_data: Dictionary containing:
                          - current_price: float
                          - indicators: dict with rsi, ma20, macd
                          - decision: dict with action, confidence, reason
                          - price_history_length: int
        
        Returns:
            Dictionary containing formatted report with:
            - summary
            - technical_indicators
            - trading_decision
            - recommendation
            - timestamp
            - risk_assessment
        """
        if not analysis_data or "error" in analysis_data:
            return {
                "ticker": ticker.upper(),
                "status": "error",
                "message": analysis_data.get("error", "Unknown error") if analysis_data else "No data provided",
                "timestamp": datetime.now().isoformat()
            }
        
        data = analysis_data.get("data", {})
        indicators = data.get("indicators", {})
        decision = data.get("decision", {})
        current_price = data.get("current_price", 0)
        
        # Generate summary
        summary = self._generate_summary(ticker, current_price, decision)
        
        # Generate technical analysis section
        tech_analysis = self._analyze_indicators(indicators)
        
        # Generate risk assessment
        risk_assessment = self._assess_risk(indicators, decision)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(decision, tech_analysis, risk_assessment)
        
        return {
            "ticker": ticker.upper(),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "report": {
                "summary": summary,
                "current_price": current_price,
                "technical_indicators": {
                    "rsi": {
                        "value": indicators.get("rsi", 0),
                        "interpretation": self._interpret_rsi(indicators.get("rsi", 50))
                    },
                    "moving_average_20": {
                        "value": indicators.get("ma20", 0),
                        "signal": self._interpret_ma(current_price, indicators.get("ma20", 0))
                    },
                    "macd": {
                        "value": indicators.get("macd", 0),
                        "interpretation": self._interpret_macd(indicators.get("macd", 0))
                    }
                },
                "trading_decision": {
                    "action": decision.get("action", "HOLD"),
                    "confidence": decision.get("confidence", 0),
                    "reasoning": decision.get("reason", "No reason provided")
                },
                "risk_assessment": risk_assessment,
                "recommendation": recommendation,
                "data_points": data.get("price_history_length", 0)
            }
        }
    
    def _generate_summary(self, ticker: str, price: float, decision: dict) -> str:
        """Generate a text summary of the analysis"""
        action = decision.get("action", "HOLD")
        confidence = decision.get("confidence", 0)
        
        if action == "BUY":
            sentiment = "bullish"
        elif action == "SELL":
            sentiment = "bearish"
        else:
            sentiment = "neutral"
        
        return f"{ticker} is trading at ${price:.2f} with a {sentiment} outlook. {action} signal with {confidence:.0%} confidence."
    
    def _interpret_rsi(self, rsi: float) -> str:
        """Interpret RSI value"""
        if rsi < 30:
            return "Oversold - Strong BUY signal"
        elif rsi < 40:
            return "Approaching oversold"
        elif rsi > 70:
            return "Overbought - Strong SELL signal"
        elif rsi > 60:
            return "Approaching overbought"
        else:
            return "Neutral - In equilibrium"
    
    def _interpret_ma(self, price: float, ma20: float) -> str:
        """Interpret Moving Average signal"""
        if price > ma20:
            diff_pct = ((price - ma20) / ma20) * 100
            return f"Price above MA20 ({diff_pct:.2f}%) - Bullish"
        else:
            diff_pct = ((ma20 - price) / ma20) * 100
            return f"Price below MA20 ({diff_pct:.2f}%) - Bearish"
    
    def _interpret_macd(self, macd: float) -> str:
        """Interpret MACD value"""
        if macd > 0.005:
            return "Positive momentum - Bullish"
        elif macd < -0.005:
            return "Negative momentum - Bearish"
        else:
            return "Neutral momentum"
    
    def _analyze_indicators(self, indicators: dict) -> Dict:
        """Analyze technical indicators and provide insights"""
        return {
            "count": len(indicators),
            "bullish_signals": self._count_bullish_signals(indicators),
            "bearish_signals": self._count_bearish_signals(indicators),
            "overall_strength": self._calculate_signal_strength(indicators)
        }
    
    def _count_bullish_signals(self, indicators: dict) -> int:
        """Count bullish signals from indicators"""
        count = 0
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)
        
        if rsi < 30:
            count += 1
        if macd > 0:
            count += 1
        
        return count
    
    def _count_bearish_signals(self, indicators: dict) -> int:
        """Count bearish signals from indicators"""
        count = 0
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)
        
        if rsi > 70:
            count += 1
        if macd < 0:
            count += 1
        
        return count
    
    def _calculate_signal_strength(self, indicators: dict) -> str:
        """Calculate overall signal strength"""
        bullish = self._count_bullish_signals(indicators)
        bearish = self._count_bearish_signals(indicators)
        
        if bullish > bearish:
            return "Strong Bullish"
        elif bearish > bullish:
            return "Strong Bearish"
        else:
            return "Mixed"
    
    def _assess_risk(self, indicators: dict, decision: dict) -> Dict:
        """Assess risk level based on indicators and decision"""
        rsi = indicators.get("rsi", 50)
        action = decision.get("action", "HOLD")
        confidence = decision.get("confidence", 0)
        
        # Determine risk level
        if rsi < 20 or rsi > 80:
            risk_level = "HIGH"
        elif rsi < 30 or rsi > 70:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"
        
        # Adjust for low confidence
        if confidence < 0.6:
            if risk_level == "LOW":
                risk_level = "MODERATE"
            elif risk_level == "MODERATE":
                risk_level = "HIGH"
        
        return {
            "level": risk_level,
            "confidence_score": confidence,
            "recommendation": f"Use {'wider' if risk_level == 'HIGH' else 'tight'} stop-loss and {'reduced' if risk_level == 'HIGH' else 'normal'} position size"
        }
    
    def _generate_recommendation(self, decision: dict, tech_analysis: dict, risk_assessment: dict) -> str:
        """Generate final recommendation based on all analysis"""
        action = decision.get("action", "HOLD")
        confidence = decision.get("confidence", 0)
        risk = risk_assessment.get("level", "MODERATE")
        
        strength = tech_analysis.get("overall_strength", "Mixed")
        
        if action == "BUY" and confidence > 0.7:
            return f"STRONG BUY - {strength} signals with {risk} risk. Consider entering a position with {risk_assessment['recommendation'].lower()}"
        elif action == "BUY":
            return f"BUY - Mixed signals, enter cautiously with {risk_assessment['recommendation'].lower()}"
        elif action == "SELL" and confidence > 0.7:
            return f"STRONG SELL - {strength} signals with {risk} risk. Consider exiting positions with {risk_assessment['recommendation'].lower()}"
        elif action == "SELL":
            return f"SELL - Mixed signals, exit cautiously with {risk_assessment['recommendation'].lower()}"
        else:
            return f"HOLD - {strength} signals. Monitor price action and wait for clearer signals before making moves."
