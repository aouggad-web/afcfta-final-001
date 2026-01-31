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
from services.real_trade_data_service import AFRICAN_COUNTRIES, get_country_name, get_product_name

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/substitution", tags=["Trade Substitution Analysis"])


@router.get("/countries")
async def get_available_countries(
    lang: str = Query(default="fr", description="Language for country names (fr/en)")
):
    """
    Get list of available African countries for analysis
    """
    countries = []
    for iso3, info in AFRICAN_COUNTRIES.items():
        countries.append({
            "iso3": iso3,
            "name": info.get(f"name_{lang}", info.get("name_en", iso3)),
            "oec_id": info.get("oec", "")
        })
    
    countries.sort(key=lambda x: x["name"])
    
    return {
        "total": len(countries),
        "countries": countries
    }


@router.get("/opportunities/import/{country_iso3}")
async def get_import_substitution_opportunities(
    country_iso3: str,
    year: int = Query(default=2022, description="Year for trade data"),
    min_value: int = Query(default=1000000, description="Minimum import value to consider (USD)"),
    lang: str = Query(default="fr", description="Language for names (fr/en)")
):
    """
    Find import substitution opportunities for a specific African country
    
    This endpoint identifies products that the country currently imports 
    from outside Africa that could be sourced from other AfCFTA countries.
    
    Uses REAL data from OEC (Observatory of Economic Complexity) API.
    
    Args:
        country_iso3: ISO3 code of the importing country
        year: Year for trade data (2018-2022 available)
        min_value: Minimum import value in USD to consider
        lang: Language for country/product names
    
    Returns:
        List of substitution opportunities with potential African suppliers
    """
    try:
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
    min_market_size: int = Query(default=5000000, description="Minimum market size to consider (USD)"),
    lang: str = Query(default="fr", description="Language for names (fr/en)")
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
    
    Returns:
        List of export opportunities with potential markets
    """
    try:
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


@router.get("/summary")
async def get_opportunities_summary(
    lang: str = Query(default="fr", description="Language for names (fr/en)")
):
    """
    Get aggregate summary of trade opportunities across Africa
    
    Returns overview statistics for the OpportunitySummary component
    """
    try:
        # Get data for a few major economies for summary stats
        major_economies = ["ZAF", "EGY", "NGA", "MAR", "KEN"]
        
        total_import_potential = 0
        total_export_potential = 0
        all_import_opps = []
        all_export_opps = []
        sectors = {}
        
        for iso3 in major_economies:
            try:
                # Get import opportunities
                import_data = await real_substitution_service.find_import_substitution_opportunities(
                    iso3, year=2022, min_value=1000000, lang=lang
                )
                if import_data.get("opportunities"):
                    total_import_potential += import_data.get("summary", {}).get("total_substitutable_value", 0)
                    for opp in import_data["opportunities"][:5]:
                        opp["country"] = get_country_name(iso3, lang)
                        opp["country_iso3"] = iso3
                        all_import_opps.append(opp)
                        
                        # Track sectors
                        hs_chapter = opp["imported_product"]["hs_code"][:2]
                        if hs_chapter not in sectors:
                            sectors[hs_chapter] = {"value": 0, "count": 0}
                        sectors[hs_chapter]["value"] += opp["substitution_potential"]
                        sectors[hs_chapter]["count"] += 1
                
                # Get export opportunities
                export_data = await real_substitution_service.find_export_opportunities(
                    iso3, year=2022, min_market_size=5000000, lang=lang
                )
                if export_data.get("opportunities"):
                    total_export_potential += export_data.get("summary", {}).get("total_potential_value", 0)
                    for opp in export_data["opportunities"][:5]:
                        opp["country"] = get_country_name(iso3, lang)
                        opp["country_iso3"] = iso3
                        all_export_opps.append(opp)
            except Exception as e:
                logger.warning(f"Error getting data for {iso3}: {e}")
                continue
        
        # Sort and format sectors
        sector_names = {
            "01": "Animaux", "02": "Viandes", "03": "Poissons", "04": "Produits laitiers",
            "07": "Légumes", "08": "Fruits", "09": "Café/Thé", "10": "Céréales",
            "15": "Huiles", "17": "Sucres", "18": "Cacao", "27": "Combustibles",
            "31": "Engrais", "39": "Plastiques", "72": "Fer/Acier", "84": "Machines",
            "85": "Électronique", "87": "Véhicules"
        }
        
        top_sectors = []
        for hs, data in sorted(sectors.items(), key=lambda x: x[1]["value"], reverse=True)[:8]:
            top_sectors.append({
                "hs_chapter": hs,
                "name": sector_names.get(hs, f"HS {hs}"),
                "value": data["value"],
                "count": data["count"]
            })
        
        # Sort opportunities
        all_import_opps.sort(key=lambda x: x["substitution_potential"], reverse=True)
        all_export_opps.sort(key=lambda x: x.get("estimated_capture", 0), reverse=True)
        
        return {
            "summary": {
                "total_import_substitution_potential": total_import_potential,
                "total_export_potential": total_export_potential,
                "total_combined": total_import_potential + total_export_potential,
                "countries_analyzed": len(major_economies),
                "currency": "USD"
            },
            "top_import_opportunities": all_import_opps[:10],
            "top_export_opportunities": all_export_opps[:10],
            "top_sectors": top_sectors,
            "data_source": "OEC (Observatory of Economic Complexity)"
        }
    
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
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
        Product-level trade analysis with African exporters and importers
    """
    from services.real_trade_data_service import real_trade_service
    
    try:
        # Get African exporters for this product
        exporters = await real_trade_service.get_african_exporters_for_product(hs_code, year)
        
        # Get African importers for this product
        importers = await real_trade_service.get_african_importers_for_product(hs_code, year)
        
        product_name = get_product_name(hs_code, lang)
        
        # Calculate totals
        total_exports = sum(e["export_value"] for e in exporters)
        total_imports = sum(i["import_value"] for i in importers)
        
        # Find substitution opportunities
        opportunities = []
        for imp in importers[:10]:
            for exp in exporters[:5]:
                if imp["country_iso3"] != exp["country_iso3"]:
                    potential = min(imp["import_value"] * 0.3, exp["export_value"])
                    if potential > 100000:
                        opportunities.append({
                            "importer": imp["country_name"],
                            "importer_iso3": imp["country_iso3"],
                            "exporter": exp["country_name"],
                            "exporter_iso3": exp["country_iso3"],
                            "potential_value": potential
                        })
        
        opportunities.sort(key=lambda x: x["potential_value"], reverse=True)
        
        return {
            "product": {
                "hs_code": hs_code,
                "name": product_name,
                "chapter": hs_code[:2]
            },
            "african_trade": {
                "total_exports": total_exports,
                "total_imports": total_imports,
                "intra_african_potential": min(total_exports, total_imports) * 0.3
            },
            "top_exporters": [
                {
                    "country": get_country_name(e["country_iso3"], lang),
                    "iso3": e["country_iso3"],
                    "value": e["export_value"]
                }
                for e in exporters[:10]
            ],
            "top_importers": [
                {
                    "country": get_country_name(i["country_iso3"], lang),
                    "iso3": i["country_iso3"],
                    "value": i["import_value"]
                }
                for i in importers[:10]
            ],
            "substitution_opportunities": opportunities[:15],
            "year": year,
            "data_source": "OEC"
        }
    
    except Exception as e:
        logger.error(f"Error analyzing product {hs_code}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def register_routes(app_router):
    """Register substitution routes with the main API router"""
    app_router.include_router(router)
