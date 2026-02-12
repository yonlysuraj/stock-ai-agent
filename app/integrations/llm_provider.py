"""
LLM Provider integration - Supports Groq and OpenAI
"""

from typing import Optional, Dict, Any
from app.config import settings


class LLMProvider:
    """LLM provider wrapper for Groq, OpenAI, etc."""
    
    def __init__(self, provider: str = "groq"):
        """
        Initialize LLM provider.
        
        Args:
            provider: Provider name ("groq" or "openai")
        """
        self.provider = provider.lower()
        
        if self.provider == "groq":
            from groq import Groq
            self.api_key = settings.GROQ_API_KEY
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not found in settings")
            self.client = Groq(api_key=self.api_key)
            self.model = "mixtral-8x7b-32768"
        elif self.provider == "openai":
            try:
                from openai import OpenAI
                self.api_key = settings.OPENAI_API_KEY
                if not self.api_key:
                    raise ValueError("OPENAI_API_KEY not found in settings")
                self.client = OpenAI(api_key=self.api_key)
                self.model = "gpt-3.5-turbo"
            except ImportError:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'groq' or 'openai'")
    
    def generate_analysis(self, context: dict) -> str:
        """
        Generate analysis using LLM.
        
        Args:
            context: Dictionary with analysis context (indicators, price, etc.)
            
        Returns:
            AI-generated analysis text
        """
        prompt = f"""Analyze the following stock data and provide insights:
        
Stock: {context.get('symbol', 'Unknown')}
Current Price: ${context.get('price', 0)}
RSI: {context.get('rsi', 0)}
MACD: {context.get('macd', 0)}
Moving Average (20): ${context.get('ma20', 0)}

Provide a brief technical analysis and trading recommendation."""

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial analyst providing stock analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def generate_summary(self, text: str) -> str:
        """
        Generate summary using LLM.
        
        Args:
            text: Text to summarize
            
        Returns:
            Summarized text
        """
        prompt = f"Summarize the following text concisely:\n\n{text}"
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes text."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=150
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error generating summary: {str(e)}"
