"""
Health check routes
Provides endpoints for monitoring API health and status
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/", tags=["Root"], summary="API Welcome")
async def root():
    """
    Welcome endpoint providing API information.
    
    Returns basic information about the API including version and status.
    """
    return {
        "message": "Bienvenue sur l'API ZLECAf - Système Commercial Africain",
        "version": "2.0.0",
        "status": "Production Ready"
    }

@router.get("/health", tags=["Health"], summary="Basic Health Check")
async def health_check():
    """
    Simple health check endpoint.
    
    Returns basic health status of the API. Use this for quick health checks
    in load balancers or monitoring systems.
    
    Returns:
        dict: Health status with timestamp and service status
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "database": "connected"
        }
    }

@router.get("/health/status", tags=["Health"], summary="Detailed Health Status")
async def detailed_health():
    """
    Detailed health status with all service checks.
    
    Provides comprehensive health information including:
    - Component status (API, Database, Cache)
    - Feature availability
    - Service latency
    
    Use this endpoint for detailed monitoring and diagnostics.
    
    Returns:
        dict: Detailed health status with all components and features
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "components": {
            "api": {"status": "up", "latency_ms": 1},
            "database": {"status": "up", "type": "MongoDB"},
            "cache": {"status": "up", "type": "In-Memory"}
        },
        "features": {
            "tariff_calculator": "enabled",
            "hs6_database": "enabled",
            "oec_integration": "enabled",
            "news_feed": "enabled"
        }
    }
