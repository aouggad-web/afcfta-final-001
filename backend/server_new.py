"""
ZLECAf Commercial Analysis System - Main Server
================================================
FastAPI backend with modular route architecture

Routes are organized in /routes/ directory:
- health.py: Health checks
- news.py: Economic news
- oec.py: OEC Trade Statistics
- hs_codes.py: HS Code browser
- production.py: Production data (FAOSTAT, UNIDO)
- logistics.py: Logistics (ports, corridors)
- countries.py: Country profiles
- tariffs.py: Tariff calculations
- statistics.py: Trade statistics
- etl.py: ETL administration

MongoDB routes (require database):
- /statistics: Comprehensive ZLECAf statistics
- /calculate-tariff: Tariff calculator
- /save-calculation: Save calculation to DB
"""

from fastapi import FastAPI, APIRouter, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from typing import Optional, Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv
import os
import logging
import json

# Import models
from models import TariffCalculationRequest, TariffCalculationResponse

# Import constants
from constants import AFRICAN_COUNTRIES

# Import data modules
from country_data import (
    get_all_countries_trade_performance,
    get_enhanced_statistics
)
from etl.country_hs6_detailed import COUNTRY_HS6_DETAILED
from etl.hs6_database import (
    get_all_categories,
    get_codes_by_category,
    get_database_stats
)
from etl.afcfta_rules_of_origin import (
    get_rule_of_origin,
    get_rules_statistics,
    ORIGIN_TYPES,
    CHAPTER_RULES
)
from etl.country_hs6_tariffs import (
    get_tariff_for_hs6,
    get_all_sub_positions,
    has_varying_rates,
    get_best_tariff_match
)

# Import routes module for modular endpoint registration
from routes import register_routes

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(
    title="Système Commercial ZLECAf - API",
    version="3.0.0",
    description="API complète pour l'analyse commerciale de la ZLECAf"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# =============================================================================
# ROOT ENDPOINT
# =============================================================================

@api_router.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Système Commercial ZLECAf API",
        "version": "3.0.0",
        "documentation": "/docs"
    }


# =============================================================================
# STATISTICS ENDPOINT (requires MongoDB)
# =============================================================================

@api_router.get("/statistics")
async def get_comprehensive_statistics():
    """
    Récupérer les statistiques complètes ZLECAf avec données enrichies 2024
    
    Includes:
    - Overview (calculations, savings, members)
    - Trade evolution (intra-African, projections)
    - Top exporters/importers 2024
    - GDP rankings
    - Sector performance
    - ZLECAf impact metrics
    """
    # Load enhanced statistics from JSON
    enhanced_stats = get_enhanced_statistics()
    
    # Database statistics
    total_calculations = await db.comprehensive_calculations.count_documents({})
    
    # Total savings
    pipeline_savings = [
        {"$group": {"_id": None, "total_savings": {"$sum": "$savings"}}}
    ]
    savings_result = await db.comprehensive_calculations.aggregate(pipeline_savings).to_list(1)
    total_savings = savings_result[0]["total_savings"] if savings_result else 0
    
    # Most active countries
    pipeline_countries = [
        {"$group": {"_id": "$origin_country", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    countries_result = await db.comprehensive_calculations.aggregate(pipeline_countries).to_list(10)
    
    # Most used HS codes
    pipeline_hs = [
        {"$group": {"_id": "$hs_code", "count": {"$sum": 1}, "avg_savings": {"$avg": "$savings"}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    hs_result = await db.comprehensive_calculations.aggregate(pipeline_hs).to_list(10)
    
    # Top beneficiary sectors
    pipeline_sectors = [
        {"$addFields": {"sector": {"$substr": ["$hs_code", 0, 2]}}},
        {"$group": {"_id": "$sector", "count": {"$sum": 1}, "total_savings": {"$sum": "$savings"}}},
        {"$sort": {"total_savings": -1}},
        {"$limit": 10}
    ]
    sectors_result = await db.comprehensive_calculations.aggregate(pipeline_sectors).to_list(10)
    
    # Calculate totals
    african_population = sum([country['population'] for country in AFRICAN_COUNTRIES])
    overview_enhanced = enhanced_stats.get('overview', {})
    
    # Generate Top 10 exporters and importers
    trade_data_all = get_all_countries_trade_performance()
    
    # Top 10 exporters
    top_10_exporters = sorted(trade_data_all, key=lambda x: x['exports_2024'], reverse=True)[:10]
    total_exports = sum([c['exports_2024'] for c in trade_data_all])
    top_exporters_formatted = [
        {
            "rank": idx + 1,
            "country": country['code'],
            "name": country['country'],
            "exports_2024": country['exports_2024'] * 1e9,
            "share_pct": round((country['exports_2024'] / total_exports) * 100, 1) if total_exports > 0 else 0
        }
        for idx, country in enumerate(top_10_exporters)
    ]
    
    # Top 10 importers
    top_10_importers = sorted(trade_data_all, key=lambda x: x['imports_2024'], reverse=True)[:10]
    total_imports = sum([c['imports_2024'] for c in trade_data_all])
    top_importers_formatted = [
        {
            "rank": idx + 1,
            "country": country['code'],
            "name": country['country'],
            "imports_2024": country['imports_2024'] * 1e9,
            "share_pct": round((country['imports_2024'] / total_imports) * 100, 1) if total_imports > 0 else 0
        }
        for idx, country in enumerate(top_10_importers)
    ]
    
    # Top 10 GDP 2024
    top_10_gdp = sorted(trade_data_all, key=lambda x: x['gdp_2024'], reverse=True)[:10]
    top_10_gdp_formatted = [
        {
            "rank": idx + 1,
            "country": country['country'],
            "code": country['code'],
            "gdp_2024_billion": round(country['gdp_2024'], 2),
            "growth_2024": country.get('growth_rate_2024', 'N/A')
        }
        for idx, country in enumerate(top_10_gdp)
    ]
    
    # Trade evolution data
    trade_evolution_data = enhanced_stats.get('trade_evolution', {})
    trade_evolution_data.update({
        "total_exports_2024": round(total_exports, 1),
        "total_imports_2024": round(total_imports, 1),
        "intra_african_trade_2024": trade_evolution_data.get("intra_african_trade_2024", 218.7),
        "growth_rate_2023_2024": trade_evolution_data.get("growth_rate_2023_2024", 13.7)
    })
    
    return {
        "overview": {
            "total_calculations": overview_enhanced.get('total_calculations', total_calculations),
            "total_savings": overview_enhanced.get('total_savings', total_savings),
            "african_countries_members": len(AFRICAN_COUNTRIES),
            "combined_population": african_population,
            "estimated_combined_gdp": overview_enhanced.get('estimated_combined_gdp', 2706000000000)
        },
        "trade_evolution": trade_evolution_data,
        "top_exporters_2024": top_exporters_formatted,
        "top_importers_2024": top_importers_formatted,
        "top_10_gdp_2024": top_10_gdp_formatted,
        "product_analysis": enhanced_stats.get('product_analysis', {}),
        "regional_integration": enhanced_stats.get('regional_integration', {}),
        "sector_performance": enhanced_stats.get('sector_performance', {}),
        "zlecaf_impact_metrics": enhanced_stats.get('zlecaf_impact_metrics', {}),
        "trade_statistics": {
            "most_active_countries": countries_result,
            "popular_hs_codes": hs_result,
            "top_beneficiary_sectors": sectors_result
        },
        "zlecaf_impact": {
            "average_tariff_reduction": "90%",
            "estimated_trade_creation": "52 milliards USD",
            "job_creation_potential": "18 millions d'emplois",
            "intra_african_trade_target": "25% d'ici 2030"
        },
        "data_sources": [
            {"source": "Union Africaine - AfCFTA Secretariat", "url": "https://au.int/en/cfta"},
            {"source": "Banque Mondiale", "url": "https://www.worldbank.org/"},
            {"source": "UNECA", "url": "https://www.uneca.org/"},
            {"source": "UNCTAD", "url": "https://unctad.org/"}
        ],
        "last_updated": datetime.now().isoformat()
    }


# =============================================================================
# RULES OF ORIGIN ENDPOINTS
# =============================================================================

@api_router.get("/rules-of-origin/stats")
async def get_rules_of_origin_statistics():
    """Get statistics about the AfCFTA Rules of Origin database"""
    return get_rules_statistics()


@api_router.get("/rules-of-origin/{hs_code}")
async def get_rules_of_origin_endpoint(hs_code: str, lang: str = "fr"):
    """
    Get AfCFTA Rules of Origin for an HS code
    
    Based on Annex II, Appendix IV of the AfCFTA Agreement
    Source: AfCFTA Protocol on Trade in Goods - Rules of Origin Manual
    """
    rule = get_rule_of_origin(hs_code, lang)
    
    if not rule:
        raise HTTPException(status_code=404, detail="Règles d'origine non trouvées pour ce code SH")
    
    # Get chapter info
    chapter = hs_code[:2].zfill(2)
    chapter_info = CHAPTER_RULES.get(chapter, {})
    
    # Determine status label
    status = rule.get("status", "UNKNOWN")
    status_labels = {
        "AGREED": {"fr": "Convenu", "en": "Agreed"},
        "PARTIAL": {"fr": "Partiellement convenu", "en": "Partially agreed"},
        "YTB": {"fr": "En cours de négociation", "en": "Under negotiation"},
        "UNKNOWN": {"fr": "Non défini", "en": "Not defined"}
    }
    status_label = status_labels.get(status, status_labels["UNKNOWN"]).get(lang, status)
    
    # Regional content calculation
    regional_content = rule.get("regional_content", 40)
    
    # Build explanation
    primary_rule = rule.get("primary_rule", {})
    alt_rule = rule.get("alternative_rule")
    
    explanation_parts = []
    if primary_rule:
        explanation_parts.append(primary_rule.get("description", primary_rule.get("name", "")))
    if alt_rule and alt_rule.get("name"):
        explanation_parts.append(f"OU {alt_rule.get('name')}")
    
    requirement_summary = " ".join(explanation_parts) if explanation_parts else "Non défini"
    
    return {
        "hs_code": hs_code,
        "hs6_code": rule.get("hs6_code"),
        "chapter": chapter,
        "chapter_description": chapter_info.get(f"description_{lang}", ""),
        "status": status,
        "status_label": status_label,
        "rules": rule,
        "explanation": {
            "primary_rule": primary_rule.get("name") if primary_rule else None,
            "alternative_rule": alt_rule.get("name") if alt_rule else None,
            "regional_content_minimum": regional_content,
            "requirement_summary": requirement_summary
        },
        "notes": rule.get("notes", ""),
        "source": {
            "name": "AfCFTA Protocol on Trade in Goods - Annex II, Appendix IV",
            "reference": "COM-12, December 2023",
            "url": "https://au-afcfta.org/legal-texts/treaties/36437-ax-AfCFTA_RULES_OF_ORIGIN_MANUAL.pdf"
        }
    }


# =============================================================================
# TARIFF CALCULATOR (requires MongoDB for saving)
# =============================================================================

@api_router.post("/calculate-tariff", response_model=TariffCalculationResponse)
async def calculate_tariff(request: TariffCalculationRequest):
    """
    Calculate comprehensive tariff comparison between NPF and ZLECAf rates
    
    Features:
    - Uses national sub-headings (8-12 digits) when available
    - Detects varying rates across sub-headings
    - Includes Rules of Origin
    - Saves calculation to database
    """
    # Normalize country codes
    from translations import get_country_name
    
    origin_iso3 = request.origin_country.upper()
    dest_iso3 = request.destination_country.upper()
    hs6_code = request.hs_code[:6].zfill(6)
    
    # Get tariff rates with sub-position precision
    tariff_info = get_best_tariff_match(dest_iso3, request.hs_code)
    
    # Determine tariff precision level
    tariff_precision = "chapter"
    sub_position_used = None
    sub_position_description = None
    
    if tariff_info:
        if tariff_info.get("match_type") == "sub_position":
            tariff_precision = "sub_position"
            sub_position_used = tariff_info.get("code")
            sub_position_description = tariff_info.get("description_fr")
        elif tariff_info.get("match_type") == "hs6_country":
            tariff_precision = "hs6_country"
    
    # Get rates
    normal_rate = tariff_info.get("dd_rate", 0.20) if tariff_info else 0.20
    vat_rate = tariff_info.get("vat_rate", 0.18) if tariff_info else 0.18
    other_taxes_rate = tariff_info.get("other_taxes_rate", 0.05) if tariff_info else 0.05
    
    # ZLECAf preferential rate
    zlecaf_rate = max(0, normal_rate - 0.10)
    
    # Check for varying rates across sub-positions
    sub_positions_available = get_all_sub_positions(dest_iso3, hs6_code)
    has_varying, min_rate, max_rate = has_varying_rates(dest_iso3, hs6_code)
    
    # Build rate warning
    rate_warning = None
    sub_positions_details = None
    
    if has_varying and len(sub_positions_available) > 0:
        rate_warning = {
            "has_variation": True,
            "message_fr": f"⚠️ Attention: Ce code SH6 ({hs6_code}) a des taux de droits de douane variables selon les sous-positions nationales. Le taux peut varier de {min_rate*100:.1f}% à {max_rate*100:.1f}%.",
            "message_en": f"⚠️ Warning: This HS6 code ({hs6_code}) has varying duty rates depending on national sub-headings. Rates range from {min_rate*100:.1f}% to {max_rate*100:.1f}%.",
            "min_rate": min_rate,
            "max_rate": max_rate,
            "min_rate_pct": f"{min_rate*100:.1f}%",
            "max_rate_pct": f"{max_rate*100:.1f}%",
            "rate_used": normal_rate,
            "rate_used_pct": f"{normal_rate*100:.1f}%",
            "recommendation_fr": "Pour un calcul plus précis, veuillez spécifier la sous-position nationale complète (8-12 chiffres).",
            "recommendation_en": "For a more accurate calculation, please specify the complete national sub-heading (8-12 digits)."
        }
        sub_positions_details = sub_positions_available
    
    # Calculate amounts
    # Normal (NPF)
    normal_dd = request.value * normal_rate
    normal_vat_base = request.value + normal_dd
    normal_vat = normal_vat_base * vat_rate
    normal_other = request.value * other_taxes_rate
    normal_total = request.value + normal_dd + normal_vat + normal_other
    
    # ZLECAf
    zlecaf_dd = request.value * zlecaf_rate
    zlecaf_vat_base = request.value + zlecaf_dd
    zlecaf_vat = zlecaf_vat_base * vat_rate
    zlecaf_other = request.value * other_taxes_rate
    zlecaf_total = request.value + zlecaf_dd + zlecaf_vat + zlecaf_other
    
    # Savings
    savings = normal_total - zlecaf_total
    savings_pct = (savings / normal_total * 100) if normal_total > 0 else 0
    
    # Get Rules of Origin
    rule_of_origin = get_rule_of_origin(hs6_code, "fr")
    regional_content = rule_of_origin.get("regional_content", 40) if rule_of_origin else 40
    
    primary_rule = rule_of_origin.get("primary_rule", {}) if rule_of_origin else {}
    alt_rule = rule_of_origin.get("alternative_rule") if rule_of_origin else None
    
    rule_code = primary_rule.get("code", "VA40")
    rule_name = primary_rule.get("name", "Valeur Ajoutée 40%")
    
    if alt_rule and alt_rule.get("name"):
        rule_name = f"{rule_name} OU {alt_rule.get('name')}"
    
    requirement = f"{regional_content}% valeur ajoutée africaine" if rule_code.startswith("VA") else rule_name
    
    # Build calculation journal
    normal_journal = [
        {"component": "Valeur CIF", "base": f"{request.value:,.0f}", "rate": "-", "amount": f"{request.value:,.0f}"},
        {"component": "Droits de douane", "base": f"{request.value:,.0f}", "rate": f"{normal_rate*100:.1f}%", "amount": f"{normal_dd:,.0f}"},
        {"component": "TVA", "base": f"{normal_vat_base:,.0f}", "rate": f"{vat_rate*100:.1f}%", "amount": f"{normal_vat:,.0f}"},
        {"component": "Autres taxes", "base": f"{request.value:,.0f}", "rate": f"{other_taxes_rate*100:.1f}%", "amount": f"{normal_other:,.0f}"},
        {"component": "TOTAL", "base": "-", "rate": "-", "amount": f"{normal_total:,.0f}"}
    ]
    
    zlecaf_journal = [
        {"component": "Valeur CIF", "base": f"{request.value:,.0f}", "rate": "-", "amount": f"{request.value:,.0f}"},
        {"component": "Droits de douane ZLECAf", "base": f"{request.value:,.0f}", "rate": f"{zlecaf_rate*100:.1f}%", "amount": f"{zlecaf_dd:,.0f}"},
        {"component": "TVA", "base": f"{zlecaf_vat_base:,.0f}", "rate": f"{vat_rate*100:.1f}%", "amount": f"{zlecaf_vat:,.0f}"},
        {"component": "Autres taxes", "base": f"{request.value:,.0f}", "rate": f"{other_taxes_rate*100:.1f}%", "amount": f"{zlecaf_other:,.0f}"},
        {"component": "TOTAL", "base": "-", "rate": "-", "amount": f"{zlecaf_total:,.0f}"}
    ]
    
    # Prepare response
    response = TariffCalculationResponse(
        hs_code=request.hs_code,
        hs6_code=hs6_code,
        origin_country=origin_iso3,
        destination_country=dest_iso3,
        value=request.value,
        currency=request.currency,
        normal_tariff_rate=normal_rate,
        zlecaf_tariff_rate=zlecaf_rate,
        normal_duty=normal_dd,
        zlecaf_duty=zlecaf_dd,
        savings=normal_dd - zlecaf_dd,
        savings_percentage=((normal_dd - zlecaf_dd) / normal_dd * 100) if normal_dd > 0 else 0,
        vat_rate=vat_rate,
        normal_vat_amount=normal_vat,
        zlecaf_vat_amount=zlecaf_vat,
        other_taxes_rate=other_taxes_rate,
        normal_other_taxes=normal_other,
        zlecaf_other_taxes=zlecaf_other,
        normal_total_cost=normal_total,
        zlecaf_total_cost=zlecaf_total,
        total_savings_with_taxes=savings,
        total_savings_percentage=savings_pct,
        normal_calculation_journal=normal_journal,
        zlecaf_calculation_journal=zlecaf_journal,
        computation_order_ref=f"CALC-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        rules_of_origin={
            "rule": rule_name,
            "rule_code": rule_code,
            "requirement": requirement,
            "regional_content": regional_content,
            "status": rule_of_origin.get("status", "AGREED") if rule_of_origin else "AGREED",
            "status_label": "Convenu" if rule_of_origin and rule_of_origin.get("status") == "AGREED" else "En négociation",
            "notes": rule_of_origin.get("notes", "") if rule_of_origin else "",
            "source": "AfCFTA Protocol on Trade in Goods - Annex II, Appendix IV"
        },
        tariff_precision=tariff_precision,
        sub_position_used=sub_position_used,
        sub_position_description=sub_position_description,
        has_varying_sub_positions=has_varying,
        available_sub_positions_count=len(sub_positions_available),
        rate_warning=rate_warning,
        sub_positions_details=sub_positions_details
    )
    
    # Save to database
    try:
        await db.comprehensive_calculations.insert_one({
            "hs_code": request.hs_code,
            "origin_country": origin_iso3,
            "destination_country": dest_iso3,
            "value": request.value,
            "savings": savings,
            "timestamp": datetime.now()
        })
    except Exception as e:
        logging.warning(f"Could not save calculation: {e}")
    
    return response


# =============================================================================
# REGISTER MODULAR ROUTES
# =============================================================================

register_routes(api_router)

# Include the router in the main app
app.include_router(api_router)
