"""
Report Agent - Generates analysis reports

Responsibilities:
- Format analysis results into readable reports
- Include summary, indicators, sentiment, decision, and recommendations
- Add timestamp and metadata
"""

from datetime import datetime
from typing import Dict, Optional
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ReportAgent:
    """Agent responsible for generating comprehensive analysis reports"""
    
    def __init__(self):
        """Initialize report agent"""
        self.report_version = "1.2" # Bump version
        
        # Initialize Groq client for AI advice
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = Groq(api_key=self.api_key)
                # Updated to a currently supported model
                self.model = "llama-3.3-70b-versatile"
            except Exception as e:
                print(f"Failed to initialize Groq client in ReportAgent: {e}")
    
    def generate_report(self, ticker: str, analysis_data: dict) -> Dict:
        """
        Generate a comprehensive analysis report from stock analysis data.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL")
            analysis_data: Dictionary containing:
                          - current_price: float
                          - indicators: dict with rsi, ma20, macd
                          - sentiment: dict with overall_score, summary, etc.
                          - decision: dict with action, confidence, reason
                          - price_history_length: int
        
        Returns:
            Dictionary containing formatted report with:
            - summary
            - sentiment_analysis
            - technical_indicators
            - trading_decision
            - recommendation
            - timestamp
            - risk_assessment
            - investment_advice (AI generated)
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
        sentiment = data.get("sentiment", {})
        decision = data.get("decision", {})
        current_price = data.get("current_price", 0)
        
        # Generate summary
        summary = self._generate_summary(ticker, current_price, decision, sentiment)
        
        # Generate technical analysis section
        tech_analysis = self._analyze_indicators(indicators)
        
        # Generate risk assessment
        risk_assessment = self._assess_risk(indicators, decision, sentiment)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(decision, tech_analysis, risk_assessment)

        # Generate AI Advice
        ai_advice = self._generate_ai_advice(ticker, current_price, decision, sentiment, indicators)
        
        return {
            "ticker": ticker.upper(),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "report": {
                "summary": summary,
                "current_price": current_price,
                "sentiment_analysis": {
                    "overall_sentiment": sentiment.get("overall_sentiment", "N/A"),
                    "score": sentiment.get("overall_score", 0),
                    "summary": sentiment.get("summary", "No sentiment data available"),
                    "confidence": sentiment.get("confidence", 0)
                },
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
                "investment_advice": ai_advice,
                "data_points": data.get("price_history_length", 0)
            }
        }
    
    def _generate_ai_advice(self, ticker: str, price: float, decision: dict, sentiment: dict, indicators: dict) -> str:
        """Generate smart investment advice using LLM"""
        if not self.client:
            return "AI Advice unavailable (API Key missing)."

        try:
            prompt = f"""You are an expert senior financial strategist. 
Based on the following data for {ticker}, provide a detailed, insightful playing strategy analysis.

Data:
- Price: ${price}
- Decision: {decision.get('action')} (Confidence: {decision.get('confidence')})
- Tech Indicators: RSI={indicators.get('rsi')}, MACD={indicators.get('macd')}
- News Sentiment: {sentiment.get('overall_sentiment')} (Score: {sentiment.get('overall_score')})
- Risk Analysis: {self._assess_risk(indicators, decision, sentiment).get('level')}

Write a comprehensive paragraph (approx 80-100 words) that:
1. Synthesizes the technical and sentiment data.
2. Explains the *why* behind the current market setup.
3. Provides a clear, actionable strategy for the next 1-2 weeks.

Tone: Professional, analytical, and direct. Avoid generic disclaimers. Do not use markdown formatting.
"""
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating AI advice: {e}")
            return "AI Advice currently unavailable."

    def _generate_summary(self, ticker: str, price: float, decision: dict, sentiment: dict) -> str:
        """Generate a text summary of the analysis"""
        action = decision.get("action", "HOLD")
        confidence = decision.get("confidence", 0)
        
        sentiment_label = sentiment.get("overall_sentiment", "neutral").lower() if sentiment else "unknown"
        
        if action == "BUY":
            bias = "bullish"
        elif action == "SELL":
            bias = "bearish"
        else:
            bias = "neutral"
        
        return f"{ticker} is trading at ${price:.2f} with a {bias} outlook. Sentiment is {sentiment_label}. {action} signal with {confidence:.0%} confidence."
    
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
        if macd is not None and macd > 0:
            count += 1
        
        return count
    
    def _count_bearish_signals(self, indicators: dict) -> int:
        """Count bearish signals from indicators"""
        count = 0
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)
        
        if rsi > 70:
            count += 1
        if macd is not None and macd < 0:
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
    
    def _assess_risk(self, indicators: dict, decision: dict, sentiment: dict) -> Dict:
        """Assess risk level based on indicators, decision, and sentiment"""
        rsi = indicators.get("rsi", 50)
        action = decision.get("action", "HOLD")
        confidence = decision.get("confidence", 0)
        
        # Determine risk level from indicators
        if rsi < 20 or rsi > 80:
            risk_level = "HIGH"
        elif rsi < 30 or rsi > 70:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"
            
        # Adjust based on Sentiment (if available)
        if sentiment:
            sentiment_score = sentiment.get("overall_score", 0)
            # High risk if sentiment contradicts action strongly
            if action == "BUY" and sentiment_score < -0.5:
                 risk_level = "HIGH"
            elif action == "SELL" and sentiment_score > 0.5:
                 risk_level = "HIGH"
        
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
