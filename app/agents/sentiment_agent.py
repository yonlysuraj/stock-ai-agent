"""
Sentiment Agent - Analyzes news sentiment using Groq LLM

Responsibilities:
- Analyze sentiment of financial news and texts
- Use Groq API for LLM-powered sentiment analysis
- Return sentiment scores and interpretations
- Handle multiple texts and aggregate results
"""

import os
from typing import Dict, List, Optional
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SentimentAgent:
    """Agent responsible for sentiment analysis using Groq LLM"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize sentiment agent with Groq API.
        
        Args:
            api_key: Groq API key. If not provided, uses GROQ_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("Groq API key not provided and GROQ_API_KEY environment variable not set")
        
        self.client = Groq(api_key=self.api_key)
        self.model = "mixtral-8x7b-32768"  # Fast and effective model
    
    def analyze_sentiment(self, texts: List[str]) -> Dict:
        """
        Analyze sentiment of provided texts using Groq LLM.
        
        Args:
            texts: List of text strings to analyze for sentiment
        
        Returns:
            Dictionary containing:
            - texts_analyzed: Number of texts analyzed
            - overall_sentiment: Aggregate sentiment (POSITIVE, NEGATIVE, NEUTRAL)
            - overall_score: Average sentiment score (-1 to 1)
            - individual_scores: List of sentiment scores for each text
            - interpretations: List of interpretations for each text
            - confidence: Overall confidence level
            - summary: Brief summary of sentiment analysis
        """
        if not texts or len(texts) == 0:
            return {
                "texts_analyzed": 0,
                "overall_sentiment": "NEUTRAL",
                "overall_score": 0,
                "error": "No texts provided for sentiment analysis"
            }
        
        scores = []
        interpretations = []
        
        # Analyze each text
        for text in texts:
            score, interpretation = self._analyze_single_text(text)
            scores.append(score)
            interpretations.append(interpretation)
        
        # Calculate aggregated sentiment
        avg_score = sum(scores) / len(scores)
        overall_sentiment = self._determine_overall_sentiment(avg_score)
        confidence = self._calculate_confidence(scores)
        
        # Generate summary
        summary = self._generate_summary(avg_score, len(texts), overall_sentiment)
        
        return {
            "texts_analyzed": len(texts),
            "overall_sentiment": overall_sentiment,
            "overall_score": round(avg_score, 3),
            "individual_scores": [round(s, 3) for s in scores],
            "interpretations": interpretations,
            "confidence": round(confidence, 2),
            "summary": summary
        }
    
    def _analyze_single_text(self, text: str) -> tuple:
        """
        Analyze sentiment of a single text using Groq LLM.
        
        Args:
            text: Text to analyze
        
        Returns:
            Tuple of (sentiment_score, interpretation)
            - sentiment_score: Float between -1 (negative) and 1 (positive)
            - interpretation: String explanation of sentiment
        """
        try:
            prompt = f"""Analyze the sentiment of the following financial news text. 
Respond in JSON format with sentiment_score (float from -1 to 1, where -1 is very negative, 0 is neutral, 1 is very positive) and interpretation (brief explanation).

Text: {text}

Respond only with valid JSON in this format:
{{
    "sentiment_score": <float>,
    "interpretation": "<brief explanation>"
}}"""
            
            # Use Groq's chat completions API
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=150
            )
            
            response_text = completion.choices[0].message.content
            
            # Parse JSON response
            import json
            try:
                response_json = json.loads(response_text)
                score = float(response_json.get("sentiment_score", 0))
                interpretation = response_json.get("interpretation", "Unable to interpret")
                
                # Ensure score is within bounds
                score = max(-1, min(1, score))
                
                return score, interpretation
            except (json.JSONDecodeError, ValueError):
                # Fallback: simple keyword-based analysis
                return self._fallback_sentiment_analysis(text)
        
        except Exception as e:
            # Fallback analysis on error
            return self._fallback_sentiment_analysis(text)
    
    def _fallback_sentiment_analysis(self, text: str) -> tuple:
        """
        Fallback simple sentiment analysis using keyword matching.
        
        Args:
            text: Text to analyze
        
        Returns:
            Tuple of (sentiment_score, interpretation)
        """
        text_lower = text.lower()
        
        positive_words = ["gain", "rise", "rally", "surge", "bull", "positive", "growth", "strong", "beat", "outperform"]
        negative_words = ["loss", "fall", "crash", "bear", "negative", "decline", "weak", "miss", "underperform"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        net_score = positive_count - negative_count
        score = 0.3 if net_score > 0 else (-0.3 if net_score < 0 else 0)
        
        if score > 0:
            interpretation = "Positive sentiment detected"
        elif score < 0:
            interpretation = "Negative sentiment detected"
        else:
            interpretation = "Neutral sentiment"
        
        return score, interpretation
    
    def _determine_overall_sentiment(self, avg_score: float) -> str:
        """
        Determine overall sentiment category based on average score.
        
        Args:
            avg_score: Average sentiment score
        
        Returns:
            Sentiment category string
        """
        if avg_score > 0.2:
            return "POSITIVE"
        elif avg_score < -0.2:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def _calculate_confidence(self, scores: List[float]) -> float:
        """
        Calculate confidence in the sentiment analysis.
        
        Confidence is higher when scores agree with each other.
        
        Args:
            scores: List of sentiment scores
        
        Returns:
            Confidence score between 0 and 1
        """
        if len(scores) == 0:
            return 0.0
        
        if len(scores) == 1:
            return 0.7
        
        # Calculate standard deviation to measure agreement
        avg = sum(scores) / len(scores)
        variance = sum((s - avg) ** 2 for s in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # Convert std deviation to confidence (lower std = higher confidence)
        confidence = 1 - min(std_dev, 1)
        
        return confidence
    
    def _generate_summary(self, avg_score: float, count: int, sentiment: str) -> str:
        """
        Generate a text summary of sentiment analysis.
        
        Args:
            avg_score: Average sentiment score
            count: Number of texts analyzed
            sentiment: Overall sentiment category
        
        Returns:
            Summary string
        """
        score_str = f"{avg_score:.2f}"
        return f"Analyzed {count} text(s) with average sentiment score of {score_str}, overall sentiment is {sentiment}"
