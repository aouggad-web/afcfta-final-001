"""
COMTRADE API Routes
Provides access to UN COMTRADE trade data
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import logging

from services.comtrade_service import comtrade_service
from services.data_source_selector import data_source_selector

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/comtrade", tags=["COMTRADE"])


@router.get("/bilateral/{reporter}")
async def get_bilateral_trade(
    reporter: str,
    partner: str = Query("0", description="Partner country code (0 for World)"),
    period: str = Query(None, description="Year (YYYY)"),
    hs_code: str = Query(None, description="HS product code")
):
    """
    Get bilateral trade data from UN COMTRADE
    
    - **reporter**: ISO3 country code (e.g., MAR, DZA, NGA)
    - **partner**: Partner country code (0 for World aggregate)
    - **period**: Year in YYYY format (defaults to previous year)
    - **hs_code**: Optional HS code filter
    """
    try:
        result = await comtrade_service.get_bilateral_trade(
            reporter_code=reporter.upper(),
            partner_code=partner,
            period=period,
            hs_code=hs_code
        )
        
        if not result:
            return {
                "status": "no_data",
                "message": f"Aucune donnée COMTRADE disponible pour {reporter}",
                "reporter": reporter,
                "source": "UN_COMTRADE"
            }
        
        return result
        
    except Exception as e:
        logger.error(f"COMTRADE bilateral error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve bilateral trade data")


@router.get("/summary/{country}")
async def get_trade_summary(
    country: str,
    period: str = Query(None, description="Year (YYYY)")
):
    """
    Get trade summary (total exports/imports) for a country
    
    - **country**: ISO3 country code
    - **period**: Year (defaults to previous year)
    """
    try:
        result = await comtrade_service.get_trade_summary(
            reporter_code=country.upper(),
            period=period
        )
        
        if not result:
            return {
                "status": "no_data",
                "message": f"Aucun résumé commercial disponible pour {country}",
                "country": country
            }
        
        return result
        
    except Exception as e:
        logger.error(f"COMTRADE summary error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve trade summary")


@router.get("/product/{hs_code}")
async def get_product_trade(
    hs_code: str,
    period: str = Query(None, description="Year (YYYY)"),
    flow: str = Query("X", description="X for exports, M for imports")
):
    """
    Get trade data for a specific product across African countries
    
    - **hs_code**: HS code (2, 4, or 6 digits)
    - **period**: Year (defaults to previous year)
    - **flow**: Trade flow (X=exports, M=imports)
    """
    try:
        result = await comtrade_service.get_product_trade(
            hs_code=hs_code,
            period=period,
            flow=flow.upper()
        )
        
        return {
            "hs_code": hs_code,
            "flow": "exports" if flow.upper() == "X" else "imports",
            "period": period,
            "countries": result,
            "count": len(result),
            "source": "UN_COMTRADE"
        }
        
    except Exception as e:
        logger.error(f"COMTRADE product error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve product trade data")


@router.get("/latest-period/{country}")
async def get_latest_period(country: str):
    """
    Check the latest available data period for a country
    
    - **country**: ISO3 country code
    """
    try:
        period = await comtrade_service.get_latest_available_period(country.upper())
        
        return {
            "country": country.upper(),
            "latest_period": period,
            "has_data": period is not None,
            "source": "UN_COMTRADE"
        }
        
    except Exception as e:
        logger.error(f"COMTRADE latest period error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve latest data period")


@router.get("/smart/{reporter}")
async def get_smart_trade_data(
    reporter: str,
    partner: str = Query(None, description="Partner country code"),
    hs_code: str = Query(None, description="HS product code")
):
    """
    Smart endpoint: automatically selects the best data source
    
    Tries sources in order: COMTRADE → OEC → WTO
    Returns data with source information for transparency
    
    - **reporter**: ISO3 country code
    - **partner**: Optional partner country
    - **hs_code**: Optional HS code filter
    """
    try:
        result = await data_source_selector.get_trade_with_source_info(
            reporter=reporter.upper(),
            partner=partner.upper() if partner else None,
            hs_code=hs_code
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Smart trade data error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve trade data")


@router.get("/sources/compare")
async def compare_data_sources(
    countries: str = Query("ZAF,EGY,NGA,MAR,KEN", description="Comma-separated ISO3 codes")
):
    """
    Compare data freshness across all sources
    
    - **countries**: Comma-separated list of ISO3 country codes
    """
    try:
        country_list = [c.strip().upper() for c in countries.split(",")]
        
        comparison = await data_source_selector.compare_data_sources(country_list)
        
        return comparison
        
    except Exception as e:
        logger.error(f"Source comparison error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to compare data sources")


@router.get("/sources/status")
async def get_sources_status():
    """
    Get current status of all trade data sources
    
    Shows availability, error counts, and recommended source
    """
    return data_source_selector.get_source_status()
