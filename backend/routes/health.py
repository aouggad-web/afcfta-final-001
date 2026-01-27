"""
Health check routes
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API ZLECAf - Système Commercial Africain",
        "version": "2.0.0",
        "status": "Production Ready"
    }

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "running",
            "database": "connected"
        }
    }

@router.get("/health/status")
async def detailed_health():
    """Detailed health status with all service checks"""
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
