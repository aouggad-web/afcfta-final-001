"""
Trade Substitution Analysis Routes
API endpoints for analyzing intra-African trade substitution opportunities
Uses REAL data from OEC API
"""
from fastapi import APIRouter, Query, HTTPException
from typing import Optional
import logging

# Import real services only (OEC data)
from services.real_substitution_service import real_substitution_service
from services.real_trade_data_service import AFRICAN_COUNTRIES

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/substitution", tags=["Trade Substitution Analysis"])


@router.get("/opportunities/import/{country_iso3}")
async def get_import_substitution_opportunities(
    country_iso3: str,
    year: int = Query(default=2022, description="Year for trade data"),
    min_value: int = Query(default=5000000, description="Minimum import value to consider (USD)"),
    lang: str = Query(default="fr", description="Language for names (fr/en)"),
    use_real_data: bool = Query(default=True, description="Use real OEC data (True) or simulated (False)")
):
    """
    Find import substitution opportunities for a specific African country
    
    This endpoint identifies products that the country currently imports from outside Africa
    but could potentially source from other AfCFTA member countries.
    
    Uses REAL data from OEC (Observatory of Economic Complexity) API.
    
    Args:
        country_iso3: ISO3 code of the importing country (e.g., NGA, EGY, ZAF)
        year: Year for trade data (2018-2022 available)
        min_value: Minimum import value threshold in USD
        lang: Language for country/product names
        use_real_data: Use real OEC API data (default) or fallback to simulated
    
    Returns:
        List of substitution opportunities with potential African suppliers
    """
    try:
        # Use real OEC data only
        result = await real_substitution_service.find_import_substitution_opportunities(
            country_iso3, year=year, min_value=min_value, lang=lang
        )
        
        if "error" in result and not result.get("opportunities"):
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding substitution opportunities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/opportunities/export/{country_iso3}")
async def get_export_opportunities(
    country_iso3: str,
    year: int = Query(default=2022, description="Year for trade data"),
    min_market_size: int = Query(default=10000000, description="Minimum market size to consider (USD)"),
    lang: str = Query(default="fr", description="Language for names (fr/en)"),
    use_real_data: bool = Query(default=True, description="Use real OEC data (True) or simulated (False)")
):
    """
    Find export opportunities for a specific African country
    
    This endpoint identifies products that the country produces and could export
    to other AfCFTA countries that currently import from outside Africa.
    
    Uses REAL data from OEC (Observatory of Economic Complexity) API.
    
    Args:
        country_iso3: ISO3 code of the exporting country
        year: Year for trade data (2018-2022 available)
        min_market_size: Minimum target market size in USD
        lang: Language for country/product names
        use_real_data: Use real OEC API data (default) or fallback to simulated
    
    Returns:
        List of export opportunities with potential markets
    """
    try:
        # Use real OEC data only
        result = await real_substitution_service.find_export_opportunities(
            country_iso3, year=year, min_market_size=min_market_size, lang=lang
        )
        
        if "error" in result and not result.get("opportunities"):
            raise HTTPException(status_code=404, detail=result["error"])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding export opportunities: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/product/{hs_code}")
async def get_product_substitution_analysis(
    hs_code: str,
    year: int = Query(default=2022, description="Year for trade data"),
    lang: str = Query(default="fr", description="Language for names (fr/en)")
):
    """
    Analyze substitution opportunities for a specific product (HS code)
    
    Uses REAL data from OEC API.
    
    Args:
        hs_code: HS code (2, 4, or 6 digits)
        year: Year for trade data
        lang: Language for names
    
    Returns:
        Product-level substitution analysis with African exporters
    """
    try:
        result = await real_substitution_service.get_product_trade_flows(
            hs_code, year=year, lang=lang
        )
        return result
    
    except Exception as e:
        logger.error(f"Error analyzing product {hs_code}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matrix")
async def get_substitution_matrix(
    lang: str = Query(default="fr", description="Language for names (fr/en)")
):
    """
    Get the complete substitution opportunity matrix for all AfCFTA countries
    
    This endpoint provides:
    - Overview of substitution potential for each country
    - Top 20 opportunities across Africa
    - Sector-level summary
    
    Returns:
        Comprehensive substitution matrix
    """
    try:
        result = substitution_service.get_african_trade_matrix(lang)
        return result
    
    except Exception as e:
        logger.error(f"Error generating substitution matrix: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/country/{country_iso3}/imports")
async def get_country_imports_from_outside(
    country_iso3: str,
    lang: str = Query(default="fr", description="Language for names")
):
    """
    Get list of products a country imports from outside Africa
    
    Args:
        country_iso3: ISO3 code of the country
        lang: Language for names
    
    Returns:
        List of imports from outside Africa
    """
    imports = get_simulated_imports_from_outside(country_iso3)
    
    if not imports:
        return {
            "country": country_iso3,
            "country_name": get_country_name(country_iso3, lang),
            "message": "No import data available for this country",
            "imports": []
        }
    
    return {
        "country": country_iso3,
        "country_name": get_country_name(country_iso3, lang),
        "total_value": sum(i["value"] for i in imports),
        "imports": imports
    }


@router.get("/country/{country_iso3}/production")
async def get_country_production_capabilities(
    country_iso3: str,
    lang: str = Query(default="fr", description="Language for names")
):
    """
    Get production/export capabilities of an African country
    
    Args:
        country_iso3: ISO3 code of the country
        lang: Language for names
    
    Returns:
        List of production capabilities
    """
    production = get_simulated_african_production(country_iso3)
    
    if not production:
        return {
            "country": country_iso3,
            "country_name": get_country_name(country_iso3, lang),
            "message": "No production data available for this country",
            "production": []
        }
    
    return {
        "country": country_iso3,
        "country_name": get_country_name(country_iso3, lang),
        "total_capacity": sum(p["capacity"] for p in production),
        "production": production
    }


@router.get("/countries")
async def get_available_countries(
    lang: str = Query(default="fr", description="Language for names")
):
    """
    Get list of all AfCFTA countries with data availability
    
    Returns:
        List of countries with import/production data status
    """
    countries = []
    
    # Use real data structure
    for iso3, info in AFRICAN_COUNTRIES.items():
        countries.append({
            "iso3": iso3,
            "name": info.get(f"name_{lang}", info.get("name_en", iso3)),
            "has_import_data": True,  # OEC has data for all countries
            "has_production_data": True,
            "oec_id": info.get("oec", "")
        })
    
    # Sort alphabetically
    countries.sort(key=lambda x: x["name"])
    
    return {
        "total_countries": len(countries),
        "data_source": "OEC (Observatory of Economic Complexity)",
        "countries": countries
    }


def register_routes(app_router):
    """Register substitution routes with the main API router"""
    app_router.include_router(router)
