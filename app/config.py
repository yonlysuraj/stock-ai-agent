"""
Configuration management
"""

from pydantic_settings import BaseSettings
from typing import Optional, List, Union
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Settings
    API_TITLE: str = "Stock AI Agent API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "sqlite:///./stock_ai.db"
    
    # API Keys
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ALPHA_VANTAGE_API_KEY: Optional[str] = None
    YAHOO_FINANCE_API_KEY: Optional[str] = None
    
    # CORS - can be a list or JSON string from env
    CORS_ORIGINS: Union[List[str], str] = '["http://localhost:3000", "http://localhost:5173", "http://localhost:8080"]'
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Redis (optional)
    REDIS_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as a list, handling both string and list inputs"""
        if isinstance(self.CORS_ORIGINS, str):
            try:
                return json.loads(self.CORS_ORIGINS)
            except json.JSONDecodeError:
                # If not JSON, split by comma
                return [origin.strip() for origin in self.CORS_ORIGINS.split(',')]
        return self.CORS_ORIGINS


settings = Settings()
