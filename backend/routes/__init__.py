"""
Routes module for ZLECAf API
Organized by domain for better maintainability

MIGRATION STATUS:
- health.py: COMPLETE
- news.py: COMPLETE  
- oec.py: COMPLETE
- hs_codes.py: COMPLETE
- production.py: COMPLETE
- logistics.py: COMPLETE
- countries.py: COMPLETE
- tariffs.py: COMPLETE
- statistics.py: COMPLETE
"""

from fastapi import APIRouter

# Import all route modules
from .health import router as health_router
from .news import router as news_router
from .oec import router as oec_router
from .hs_codes import router as hs_codes_router
from .production import router as production_router
from .logistics import router as logistics_router
from .countries import router as countries_router
from .tariffs import router as tariffs_router
from .statistics import router as statistics_router

def register_routes(api_router: APIRouter):
    """Register all route modules to the main API router"""
    api_router.include_router(health_router, tags=["Health"])
    api_router.include_router(news_router, tags=["News"])
    api_router.include_router(oec_router, tags=["OEC Trade"])
    api_router.include_router(hs_codes_router, tags=["HS Codes"])
    api_router.include_router(production_router, tags=["Production"])
    api_router.include_router(logistics_router, tags=["Logistics"])
    api_router.include_router(countries_router, tags=["Countries"])
    api_router.include_router(tariffs_router, tags=["Tariffs"])
    api_router.include_router(statistics_router, tags=["Statistics"])
