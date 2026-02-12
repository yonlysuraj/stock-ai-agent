"""
Main Application Entry Point - Stock AI Research Agent Backend.

Minimal FastAPI application for stock analysis.
No authentication, no database, pure analysis logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.api.routes.stock_routes import router as stock_router
from app.config import settings

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    description="AI-powered stock analysis using technical indicators",
    version=settings.API_VERSION
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),  # Use settings instead of hardcoded
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stock_router, prefix="/api/stocks", tags=["stocks"])


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON response indicating API status
    """
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }


@app.get("/")
async def root():
    """
    Root endpoint - API information.
    
    Returns:
        API documentation and usage info
    """
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "description": "AI-powered stock analysis using technical indicators and LLM",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "analyze": "/api/stocks/analyze/{symbol}",
            "report": "/api/stocks/report/{symbol}",
            "sentiment": "/api/stocks/sentiment/analyze (POST)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    # Run server with hot reload
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
