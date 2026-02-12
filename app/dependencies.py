"""
Dependency injection setup

This module provides FastAPI dependency functions for:
- Database sessions (optional, for future features)
- LLM provider instances (Groq by default)
"""

from app.integrations.llm_provider import LLMProvider

# Database session management (optional - for future portfolio/auth features)
try:
    from app.data.database import SessionLocal
    DB_AVAILABLE = True
except Exception:
    DB_AVAILABLE = False


def get_db():
    """
    Get database session (optional dependency).
    
    Yields:
        Database session if available
        
    Raises:
        RuntimeError: If database is not configured
    """
    if not DB_AVAILABLE:
        raise RuntimeError(
            "Database not configured. This feature requires database setup."
        )
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_llm_provider(provider: str = "groq") -> LLMProvider:
    """
    Get LLM provider instance.
    
    Args:
        provider: Provider name ("groq" or "openai"), defaults to "groq"
        
    Returns:
        LLM provider instance configured with the specified provider
        
    Example:
        provider = get_llm_provider()  # Uses Groq
        provider = get_llm_provider("openai")  # Uses OpenAI
    """
    return LLMProvider(provider=provider)
