"""
Production routes - FAOSTAT, UNIDO, USGS, World Bank data
Covers all 4 dimensions: Macro, Agriculture, Manufacturing, Mining
"""
from fastapi import APIRouter, Query
from typing import Optional

from production_data import (
    get_value_added,
    get_value_added_by_country,
    get_agriculture_production,
    get_agriculture_by_country,
    get_manufacturing_production,
    get_manufacturing_by_country,
    get_mining_production,
    get_mining_by_country as get_mining_by_country_data,
    get_production_statistics,
    get_country_production_overview
)

router = APIRouter(prefix="/production")

@router.get("/statistics")
async def get_production_stats():
    """
    Get global production statistics for all African countries
    Returns overview of data coverage across 4 dimensions
    """
    return get_production_statistics()

@router.get("/macro")
async def get_macro_value_added(
    country_iso3: Optional[str] = None,
    year: Optional[int] = None,
    sector: Optional[str] = None
):
    """
    Get macro-level value added data (World Bank/IMF)
    
    Query parameters:
    - country_iso3: ISO3 country code (e.g., 'ZAF')
    - year: Year (2021-2024)
    - sector: ISIC section ('A', 'B-F', 'C')
    """
    return get_value_added(country_iso3=country_iso3, year=year, sector=sector)

@router.get("/macro/{country_iso3}")
async def get_macro_by_country(country_iso3: str):
    """
    Get all macro value added series for a specific country
    Organized by sector with time series
    """
    return get_value_added_by_country(country_iso3)

@router.get("/agriculture")
async def get_agri_production(
    country_iso3: Optional[str] = None,
    year: Optional[int] = None,
    commodity: Optional[str] = None
):
    """
    Get agricultural production data (FAOSTAT)
    
    Query parameters:
    - country_iso3: ISO3 country code
    - year: Year (2021-2024)
    - commodity: Commodity name or code (e.g., 'Maize', '0015')
    """
    return get_agriculture_production(country_iso3=country_iso3, year=year, commodity=commodity)

@router.get("/agriculture/{country_iso3}")
async def get_agri_by_country(country_iso3: str):
    """
    Get all agricultural production for a specific country
    Organized by commodity with time series
    """
    return get_agriculture_by_country(country_iso3)

@router.get("/manufacturing")
async def get_manuf_production(
    country_iso3: Optional[str] = None,
    year: Optional[int] = None,
    isic_code: Optional[str] = None
):
    """
    Get manufacturing production data (UNIDO)
    
    Query parameters:
    - country_iso3: ISO3 country code
    - year: Year (2021-2024)
    - isic_code: ISIC Rev.4 code (e.g., '10', '11')
    """
    return get_manufacturing_production(country_iso3=country_iso3, year=year, isic_code=isic_code)

@router.get("/manufacturing/{country_iso3}")
async def get_manuf_by_country(country_iso3: str):
    """
    Get all manufacturing production for a specific country
    Organized by ISIC sector with time series
    """
    return get_manufacturing_by_country(country_iso3)

@router.get("/mining")
async def get_mining_prod(
    country_iso3: Optional[str] = None,
    year: Optional[int] = None,
    commodity: Optional[str] = None
):
    """
    Get mining production data (USGS)
    
    Query parameters:
    - country_iso3: ISO3 country code
    - year: Year (2021-2024)
    - commodity: Mineral name or code (e.g., 'Gold', 'AU')
    """
    return get_mining_production(country_iso3=country_iso3, year=year, commodity=commodity)

@router.get("/mining/{country_iso3}")
async def get_mining_by_country(country_iso3: str):
    """
    Get all mining production for a specific country
    Organized by commodity with time series
    """
    return get_mining_by_country_data(country_iso3)

@router.get("/overview/{country_iso3}")
async def get_country_production_full_overview(country_iso3: str):
    """
    Get complete production overview for a country
    Includes all 4 dimensions: macro, agriculture, manufacturing, mining
    """
    return get_country_production_overview(country_iso3)
