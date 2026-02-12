"""
Core application settings

This module re-exports the settings instance from config
for convenient access throughout the application.
"""

from app.config import settings

# Re-export settings instance
__all__ = ['settings']
