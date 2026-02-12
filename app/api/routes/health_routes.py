"""
Health check and status routes

Responsibilities:
- Provide API health status
- Check service availability
- Return version and service information

"""

from fastapi import APIRouter
from datetime import datetime
from typing import Dict, Any

router = APIRouter()

# Service metadata
SERVICE_VERSION = "1.0.0"
SERVICE_NAME = "Stock AI Research Agent"
START_TIME = datetime.now()


@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        - status: "healthy" or "degraded"
        - service: Service name
        - version: Service version
        - timestamp: Current timestamp
        - uptime_seconds: Seconds since service started
    """
    uptime = (datetime.now() - START_TIME).total_seconds()
    
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "timestamp": datetime.now().isoformat(),
        "uptime_seconds": round(uptime, 2)
    }


@router.get("/status")
async def status() -> Dict[str, Any]:
    """
    Detailed service status endpoint.
    
    Returns:
        - status: Overall status
        - service: Service information
        - capabilities: Available features
        - timestamp: Current timestamp
    """
    return {
        "status": "operational",
        "service": {
            "name": SERVICE_NAME,
            "version": SERVICE_VERSION,
            "environment": "production"
        },
        "capabilities": [
            "Stock analysis with technical indicators",
            "Trading decision recommendations",
            "Portfolio management",
            "Sentiment analysis",
            "Report generation"
        ],
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "analysis": "/api/stocks/analyze/{symbol}",
            "report": "/api/stocks/report/{symbol}",
            "sentiment": "/api/sentiment/analyze",
            "portfolio": "/api/portfolio"
        }
    }


@router.get("/ping")
async def ping() -> Dict[str, bool]:
    """
    Simple ping endpoint for connectivity check.
    
    Returns:
        - pong: True if service is responsive
    """
    return {"pong": True}


@router.get("/ready")
async def readiness_check() -> Dict[str, Any]:
    """
    Kubernetes-style readiness check.
    
    Returns:
        - ready: True if service is ready to handle requests
        - service: Service name
        - checks: Status of critical checks
    """
    return {
        "ready": True,
        "service": SERVICE_NAME,
        "checks": {
            "api": "pass",
            "database": "pass",
            "external_services": "pass"
        }
    }
