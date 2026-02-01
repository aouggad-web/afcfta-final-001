"""
Gemini AI Trade Analysis Routes
API endpoints for AI-powered trade analysis using Google Gemini
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import logging

from services.gemini_trade_service import gemini_trade_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI Trade Analysis"])


@router.get("/opportunities/{country_name}")
async def get_ai_trade_opportunities(
    country_name: str,
    mode: str = Query(default="export", description="Analysis mode: export, import, or industrial"),
    lang: str = Query(default="fr", description="Language for response (fr/en)")
):
    """
    Get AI-analyzed trade opportunities for a country
    
    Uses Google Gemini to analyze trade opportunities based on official data sources.
    
    Args:
        country_name: Name of the African country (e.g., "Algeria", "Nigeria", "Kenya")
        mode: Analysis mode
            - export: Find export opportunities
            - import: Find import substitution opportunities  
            - industrial: Analyze value chain transformation opportunities
        lang: Language for the response
    
    Returns:
        AI-generated trade opportunities with sources and reliability indicators
    """
    valid_modes = ["export", "import", "industrial"]
    if mode not in valid_modes:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid mode. Must be one of: {valid_modes}"
        )
    
    try:
        result = await gemini_trade_service.analyze_trade_opportunities(
            country_name=country_name,
            mode=mode,
            lang=lang
        )
        
        if "error" in result and not result.get("opportunities"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in AI trade analysis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/{country_name}")
async def get_ai_country_profile(
    country_name: str,
    lang: str = Query(default="fr", description="Language for response (fr/en)")
):
    """
    Get AI-generated comprehensive economic profile for a country
    
    Includes:
    - Economic indicators (GDP, inflation, unemployment, debt)
    - Development indices (HDI, GAI)
    - Trade summary with top partners and products
    - AfCFTA potential and opportunities
    
    Args:
        country_name: Name of the African country
        lang: Language for the response
    
    Returns:
        Comprehensive country profile with economic and trade data
    """
    try:
        result = await gemini_trade_service.get_country_economic_profile(
            country_name=country_name,
            lang=lang
        )
        
        if "error" in result and len(result) <= 2:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating country profile: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/product/{hs_code}")
async def get_ai_product_analysis(
    hs_code: str,
    lang: str = Query(default="fr", description="Language for response (fr/en)")
):
    """
    Get AI-analyzed trade flows for a specific product (HS code)
    
    Provides:
    - Product information and classification
    - African trade flows summary
    - Top African exporters and importers
    - Production capacities
    - Substitution opportunities
    
    Args:
        hs_code: HS code (4 or 6 digits)
        lang: Language for the response
    
    Returns:
        Comprehensive product trade analysis for Africa
    """
    # Validate HS code format
    if not hs_code.isdigit() or len(hs_code) not in [2, 4, 6]:
        raise HTTPException(
            status_code=400,
            detail="HS code must be 2, 4, or 6 digits"
        )
    
    try:
        result = await gemini_trade_service.analyze_product_by_hs_code(
            hs_code=hs_code,
            lang=lang
        )
        
        if "error" in result and len(result) <= 2:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/balance/{country_name}")
async def get_ai_trade_balance(
    country_name: str,
    lang: str = Query(default="fr", description="Language for response (fr/en)")
):
    """
    Get AI-analyzed trade balance history for a country
    
    Returns trade balance data (exports, imports, balance) for 2020-2024
    with trend analysis and outlook.
    
    Args:
        country_name: Name of the African country
        lang: Language for the response
    
    Returns:
        Trade balance history with analysis
    """
    try:
        result = await gemini_trade_service.get_trade_balance_analysis(
            country_name=country_name,
            lang=lang
        )
        
        if "error" in result and len(result) <= 2:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trade balance: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def check_ai_service_health():
    """
    Check if the AI service is properly configured and operational
    """
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    has_key = bool(os.environ.get("EMERGENT_LLM_KEY"))
    
    return {
        "status": "operational" if has_key else "not_configured",
        "api_key_configured": has_key,
        "model": "gemini-3-flash-preview",
        "provider": "Google Gemini via Emergent LLM"
    }


def register_routes(app_router):
    """Register AI analysis routes with the main API router"""
    app_router.include_router(router)
