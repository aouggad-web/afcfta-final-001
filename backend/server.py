from fastapi import FastAPI, APIRouter, HTTPException, UploadFile, File, Form, Query
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
import uuid
from datetime import datetime
import requests
import pandas as pd
import asyncio
import json
from country_data import get_country_data, REAL_COUNTRY_DATA
from tax_rates import calculate_all_taxes, get_vat_rate
from data_loader import (
    load_corrections_data, 
    load_commerce_data, 
    get_country_commerce_profile,
    get_all_countries_trade_performance,
    get_enhanced_statistics,
    get_tariff_corrections,
    get_country_customs_info,
    get_country_infrastructure_ranking
)
from etl.news_aggregator import get_news, get_news_by_region, get_news_by_category
from logistics_data import (
    get_all_ports,
    get_port_by_id,
    get_ports_by_type,
    get_top_ports_by_teu,
    search_ports
)
from logistics_air_data import (
    get_all_airports,
    get_airport_by_id,
    get_top_airports_by_cargo,
    search_airports
)
from projects_data import get_country_ongoing_projects
from etl.country_tariffs import get_country_tariff_rate, get_available_rates, get_tariff_regime
from free_zones_data import load_free_zones, get_free_zones_by_country
from etl.hs_codes_data import (
    get_hs_chapters,
    get_hs6_codes,
    get_hs6_code,
    search_hs_codes,
    get_codes_by_chapter,
    get_all_hs_data
)
from etl.hs6_tariffs import (
    get_hs6_tariff,
    get_hs6_tariff_rates,
    search_hs6_tariffs,
    get_hs6_tariffs_by_chapter,
    get_hs6_statistics
)
from etl.country_tariffs_complete import (
    get_tariff_rate_for_country,
    get_zlecaf_tariff_rate,
    get_vat_rate_for_country,
    get_other_taxes_for_country,
    get_complete_taxes_for_country,
    get_all_country_rates,
    COUNTRY_VAT_RATES,
    COUNTRY_OTHER_TAXES
)
from etl.country_hs6_tariffs import (
    get_country_hs6_tariff,
    get_country_hs6_dd_rate,
    search_country_hs6_tariffs,
    get_available_country_tariffs,
    COUNTRY_HS6_TARIFFS
)
from etl.country_hs6_detailed import (
    get_detailed_tariff,
    get_sub_position_rate,
    get_all_sub_positions,
    has_varying_rates,
    get_tariff_summary,
    COUNTRY_HS6_DETAILED
)
from etl.hs6_database import (
    HS6_DATABASE,
    SUB_POSITION_TYPES,
    get_hs6_info,
    get_sub_position_suggestions,
    get_rule_of_origin,
    search_hs6_codes,
    get_all_categories,
    get_codes_by_category,
    get_database_stats
)
from services.oec_trade_service import (
    oec_service,
    get_african_countries_list,
    AFRICAN_COUNTRIES_OEC
)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Translations for country names and regions
COUNTRY_TRANSLATIONS = {
    "DZ": {"fr": "Algérie", "en": "Algeria"},
    "AO": {"fr": "Angola", "en": "Angola"},
    "BJ": {"fr": "Bénin", "en": "Benin"},
    "BW": {"fr": "Botswana", "en": "Botswana"},
    "BF": {"fr": "Burkina Faso", "en": "Burkina Faso"},
    "BI": {"fr": "Burundi", "en": "Burundi"},
    "CM": {"fr": "Cameroun", "en": "Cameroon"},
    "CV": {"fr": "Cap-Vert", "en": "Cape Verde"},
    "CF": {"fr": "République Centrafricaine", "en": "Central African Republic"},
    "TD": {"fr": "Tchad", "en": "Chad"},
    "KM": {"fr": "Comores", "en": "Comoros"},
    "CG": {"fr": "République du Congo", "en": "Republic of Congo"},
    "CD": {"fr": "République Démocratique du Congo", "en": "Democratic Republic of Congo"},
    "CI": {"fr": "Côte d'Ivoire", "en": "Ivory Coast"},
    "DJ": {"fr": "Djibouti", "en": "Djibouti"},
    "EG": {"fr": "Égypte", "en": "Egypt"},
    "GQ": {"fr": "Guinée Équatoriale", "en": "Equatorial Guinea"},
    "ER": {"fr": "Érythrée", "en": "Eritrea"},
    "SZ": {"fr": "Eswatini", "en": "Eswatini"},
    "ET": {"fr": "Éthiopie", "en": "Ethiopia"},
    "GA": {"fr": "Gabon", "en": "Gabon"},
    "GM": {"fr": "Gambie", "en": "Gambia"},
    "GH": {"fr": "Ghana", "en": "Ghana"},
    "GN": {"fr": "Guinée", "en": "Guinea"},
    "GW": {"fr": "Guinée-Bissau", "en": "Guinea-Bissau"},
    "KE": {"fr": "Kenya", "en": "Kenya"},
    "LS": {"fr": "Lesotho", "en": "Lesotho"},
    "LR": {"fr": "Libéria", "en": "Liberia"},
    "LY": {"fr": "Libye", "en": "Libya"},
    "MG": {"fr": "Madagascar", "en": "Madagascar"},
    "MW": {"fr": "Malawi", "en": "Malawi"},
    "ML": {"fr": "Mali", "en": "Mali"},
    "MR": {"fr": "Mauritanie", "en": "Mauritania"},
    "MU": {"fr": "Maurice", "en": "Mauritius"},
    "MA": {"fr": "Maroc", "en": "Morocco"},
    "MZ": {"fr": "Mozambique", "en": "Mozambique"},
    "NA": {"fr": "Namibie", "en": "Namibia"},
    "NE": {"fr": "Niger", "en": "Niger"},
    "NG": {"fr": "Nigéria", "en": "Nigeria"},
    "RW": {"fr": "Rwanda", "en": "Rwanda"},
    "ST": {"fr": "São Tomé-et-Príncipe", "en": "São Tomé and Príncipe"},
    "SN": {"fr": "Sénégal", "en": "Senegal"},
    "SC": {"fr": "Seychelles", "en": "Seychelles"},
    "SL": {"fr": "Sierra Leone", "en": "Sierra Leone"},
    "SO": {"fr": "Somalie", "en": "Somalia"},
    "ZA": {"fr": "Afrique du Sud", "en": "South Africa"},
    "SS": {"fr": "Soudan du Sud", "en": "South Sudan"},
    "SD": {"fr": "Soudan", "en": "Sudan"},
    "TZ": {"fr": "Tanzanie", "en": "Tanzania"},
    "TG": {"fr": "Togo", "en": "Togo"},
    "TN": {"fr": "Tunisie", "en": "Tunisia"},
    "UG": {"fr": "Ouganda", "en": "Uganda"},
    "ZM": {"fr": "Zambie", "en": "Zambia"},
    "ZW": {"fr": "Zimbabwe", "en": "Zimbabwe"}
}

REGION_TRANSLATIONS = {
    "Afrique du Nord": {"fr": "Afrique du Nord", "en": "North Africa"},
    "Afrique de l'Ouest": {"fr": "Afrique de l'Ouest", "en": "West Africa"},
    "Afrique de l'Est": {"fr": "Afrique de l'Est", "en": "East Africa"},
    "Afrique Centrale": {"fr": "Afrique Centrale", "en": "Central Africa"},
    "Afrique Australe": {"fr": "Afrique Australe", "en": "Southern Africa"}
}

RULES_TRANSLATIONS = {
    "Entièrement obtenus": {"fr": "Entièrement obtenus", "en": "Wholly obtained"},
    "Transformation substantielle": {"fr": "Transformation substantielle", "en": "Substantial transformation"},
    "Extraction ou transformation substantielle": {"fr": "Extraction ou transformation substantielle", "en": "Extraction or substantial transformation"},
    "Extraction": {"fr": "Extraction", "en": "Extraction"},
    "100% africain": {"fr": "100% africain", "en": "100% African"},
    "40% valeur ajoutée africaine": {"fr": "40% valeur ajoutée africaine", "en": "40% African value added"},
    "35% valeur ajoutée africaine": {"fr": "35% valeur ajoutée africaine", "en": "35% African value added"},
    "45% valeur ajoutée africaine": {"fr": "45% valeur ajoutée africaine", "en": "45% African value added"},
    "Entièrement extraits en Afrique": {"fr": "Entièrement extraits en Afrique", "en": "Wholly extracted in Africa"}
}

def translate_country_name(code: str, lang: str = "fr") -> str:
    """Get translated country name"""
    if code in COUNTRY_TRANSLATIONS:
        return COUNTRY_TRANSLATIONS[code].get(lang, COUNTRY_TRANSLATIONS[code]["fr"])
    return code

def translate_region(region: str, lang: str = "fr") -> str:
    """Get translated region name"""
    if region in REGION_TRANSLATIONS:
        return REGION_TRANSLATIONS[region].get(lang, region)
    return region

def translate_rule(text: str, lang: str = "fr") -> str:
    """Get translated rule text"""
    if text in RULES_TRANSLATIONS:
        return RULES_TRANSLATIONS[text].get(lang, text)
    return text

# Load gold reserves and GAI data
def load_gold_reserves_gai():
    """Load gold reserves and Global Attractiveness Index 2025 data"""
    try:
        with open(ROOT_DIR / '../gold_reserves_gai_2025.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load gold_reserves_gai_2025.json: {e}")
        return {"gold_reserves": {}, "global_attractiveness_index_2025": {}}

GOLD_RESERVES_GAI_DATA = load_gold_reserves_gai()
print(f"✅ Loaded gold reserves for {len(GOLD_RESERVES_GAI_DATA['gold_reserves'])} countries")
print(f"✅ Loaded GAI 2025 for {len(GOLD_RESERVES_GAI_DATA['global_attractiveness_index_2025'])} countries")

# Create the main app without a prefix
app = FastAPI(title="Système Commercial ZLECAf - API Complète", version="2.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Pays membres de la ZLECAf avec données économiques
AFRICAN_COUNTRIES = [
    {"code": "DZ", "name": "Algérie", "region": "Afrique du Nord", "iso3": "DZA", "wb_code": "DZA", "population": 44700000},
    {"code": "AO", "name": "Angola", "region": "Afrique Centrale", "iso3": "AGO", "wb_code": "AGO", "population": 32800000},
    {"code": "BJ", "name": "Bénin", "region": "Afrique de l'Ouest", "iso3": "BEN", "wb_code": "BEN", "population": 12100000},
    {"code": "BW", "name": "Botswana", "region": "Afrique Australe", "iso3": "BWA", "wb_code": "BWA", "population": 2400000},
    {"code": "BF", "name": "Burkina Faso", "region": "Afrique de l'Ouest", "iso3": "BFA", "wb_code": "BFA", "population": 21500000},
    {"code": "BI", "name": "Burundi", "region": "Afrique de l'Est", "iso3": "BDI", "wb_code": "BDI", "population": 12000000},
    {"code": "CM", "name": "Cameroun", "region": "Afrique Centrale", "iso3": "CMR", "wb_code": "CMR", "population": 26500000},
    {"code": "CV", "name": "Cap-Vert", "region": "Afrique de l'Ouest", "iso3": "CPV", "wb_code": "CPV", "population": 560000},
    {"code": "CF", "name": "République Centrafricaine", "region": "Afrique Centrale", "iso3": "CAF", "wb_code": "CAF", "population": 5400000},
    {"code": "TD", "name": "Tchad", "region": "Afrique Centrale", "iso3": "TCD", "wb_code": "TCD", "population": 16400000},
    {"code": "KM", "name": "Comores", "region": "Afrique de l'Est", "iso3": "COM", "wb_code": "COM", "population": 870000},
    {"code": "CG", "name": "République du Congo", "region": "Afrique Centrale", "iso3": "COG", "wb_code": "COG", "population": 5500000},
    {"code": "CD", "name": "République Démocratique du Congo", "region": "Afrique Centrale", "iso3": "COD", "wb_code": "COD", "population": 89600000},
    {"code": "CI", "name": "Côte d'Ivoire", "region": "Afrique de l'Ouest", "iso3": "CIV", "wb_code": "CIV", "population": 26400000},
    {"code": "DJ", "name": "Djibouti", "region": "Afrique de l'Est", "iso3": "DJI", "wb_code": "DJI", "population": 990000},
    {"code": "EG", "name": "Égypte", "region": "Afrique du Nord", "iso3": "EGY", "wb_code": "EGY", "population": 102300000},
    {"code": "GQ", "name": "Guinée Équatoriale", "region": "Afrique Centrale", "iso3": "GNQ", "wb_code": "GNQ", "population": 1400000},
    {"code": "ER", "name": "Érythrée", "region": "Afrique de l'Est", "iso3": "ERI", "wb_code": "ERI", "population": 3500000},
    {"code": "SZ", "name": "Eswatini", "region": "Afrique Australe", "iso3": "SWZ", "wb_code": "SWZ", "population": 1160000},
    {"code": "ET", "name": "Éthiopie", "region": "Afrique de l'Est", "iso3": "ETH", "wb_code": "ETH", "population": 115000000},
    {"code": "GA", "name": "Gabon", "region": "Afrique Centrale", "iso3": "GAB", "wb_code": "GAB", "population": 2200000},
    {"code": "GM", "name": "Gambie", "region": "Afrique de l'Ouest", "iso3": "GMB", "wb_code": "GMB", "population": 2400000},
    {"code": "GH", "name": "Ghana", "region": "Afrique de l'Ouest", "iso3": "GHA", "wb_code": "GHA", "population": 31100000},
    {"code": "GN", "name": "Guinée", "region": "Afrique de l'Ouest", "iso3": "GIN", "wb_code": "GIN", "population": 13100000},
    {"code": "GW", "name": "Guinée-Bissau", "region": "Afrique de l'Ouest", "iso3": "GNB", "wb_code": "GNB", "population": 2000000},
    {"code": "KE", "name": "Kenya", "region": "Afrique de l'Est", "iso3": "KEN", "wb_code": "KEN", "population": 53800000},
    {"code": "LS", "name": "Lesotho", "region": "Afrique Australe", "iso3": "LSO", "wb_code": "LSO", "population": 2100000},
    {"code": "LR", "name": "Libéria", "region": "Afrique de l'Ouest", "iso3": "LBR", "wb_code": "LBR", "population": 5100000},
    {"code": "LY", "name": "Libye", "region": "Afrique du Nord", "iso3": "LBY", "wb_code": "LBY", "population": 6900000},
    {"code": "MG", "name": "Madagascar", "region": "Afrique de l'Est", "iso3": "MDG", "wb_code": "MDG", "population": 28000000},
    {"code": "MW", "name": "Malawi", "region": "Afrique de l'Est", "iso3": "MWI", "wb_code": "MWI", "population": 19100000},
    {"code": "ML", "name": "Mali", "region": "Afrique de l'Ouest", "iso3": "MLI", "wb_code": "MLI", "population": 20300000},
    {"code": "MR", "name": "Mauritanie", "region": "Afrique de l'Ouest", "iso3": "MRT", "wb_code": "MRT", "population": 4600000},
    {"code": "MU", "name": "Maurice", "region": "Afrique de l'Est", "iso3": "MUS", "wb_code": "MUS", "population": 1300000},
    {"code": "MA", "name": "Maroc", "region": "Afrique du Nord", "iso3": "MAR", "wb_code": "MAR", "population": 37000000},
    {"code": "MZ", "name": "Mozambique", "region": "Afrique de l'Est", "iso3": "MOZ", "wb_code": "MOZ", "population": 31300000},
    {"code": "NA", "name": "Namibie", "region": "Afrique Australe", "iso3": "NAM", "wb_code": "NAM", "population": 2500000},
    {"code": "NE", "name": "Niger", "region": "Afrique de l'Ouest", "iso3": "NER", "wb_code": "NER", "population": 24200000},
    {"code": "NG", "name": "Nigéria", "region": "Afrique de l'Ouest", "iso3": "NGA", "wb_code": "NGA", "population": 218500000},
    {"code": "RW", "name": "Rwanda", "region": "Afrique de l'Est", "iso3": "RWA", "wb_code": "RWA", "population": 13000000},
    {"code": "ST", "name": "São Tomé-et-Príncipe", "region": "Afrique Centrale", "iso3": "STP", "wb_code": "STP", "population": 220000},
    {"code": "SN", "name": "Sénégal", "region": "Afrique de l'Ouest", "iso3": "SEN", "wb_code": "SEN", "population": 17200000},
    {"code": "SC", "name": "Seychelles", "region": "Afrique de l'Est", "iso3": "SYC", "wb_code": "SYC", "population": 98000},
    {"code": "SL", "name": "Sierra Leone", "region": "Afrique de l'Ouest", "iso3": "SLE", "wb_code": "SLE", "population": 8000000},
    {"code": "SO", "name": "Somalie", "region": "Afrique de l'Est", "iso3": "SOM", "wb_code": "SOM", "population": 16000000},
    {"code": "ZA", "name": "Afrique du Sud", "region": "Afrique Australe", "iso3": "ZAF", "wb_code": "ZAF", "population": 59300000},
    {"code": "SS", "name": "Soudan du Sud", "region": "Afrique de l'Est", "iso3": "SSD", "wb_code": "SSD", "population": 11200000},
    {"code": "SD", "name": "Soudan", "region": "Afrique du Nord", "iso3": "SDN", "wb_code": "SDN", "population": 44900000},
    {"code": "TZ", "name": "Tanzanie", "region": "Afrique de l'Est", "iso3": "TZA", "wb_code": "TZA", "population": 59700000},
    {"code": "TG", "name": "Togo", "region": "Afrique de l'Ouest", "iso3": "TGO", "wb_code": "TGO", "population": 8300000},
    {"code": "TN", "name": "Tunisie", "region": "Afrique du Nord", "iso3": "TUN", "wb_code": "TUN", "population": 11800000},
    {"code": "UG", "name": "Ouganda", "region": "Afrique de l'Est", "iso3": "UGA", "wb_code": "UGA", "population": 45700000},
    {"code": "ZM", "name": "Zambie", "region": "Afrique de l'Est", "iso3": "ZMB", "wb_code": "ZMB", "population": 18400000},
    {"code": "ZW", "name": "Zimbabwe", "region": "Afrique de l'Est", "iso3": "ZWE", "wb_code": "ZWE", "population": 15000000}
]

# Règles d'origine ZLECAf par secteur/code SH
ZLECAF_RULES_OF_ORIGIN = {
    "01": {"rule": "Entièrement obtenus", "requirement": "100% africain", "regional_content": 100},
    "02": {"rule": "Entièrement obtenus", "requirement": "100% africain", "regional_content": 100},
    "03": {"rule": "Entièrement obtenus", "requirement": "100% africain", "regional_content": 100},
    "04": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "05": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "06": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "07": {"rule": "Entièrement obtenus", "requirement": "100% africain", "regional_content": 100},
    "08": {"rule": "Entièrement obtenus", "requirement": "100% africain", "regional_content": 100},
    "09": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "10": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "11": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "12": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "13": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "14": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "15": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "16": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "17": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "18": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "19": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "20": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "21": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "22": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "23": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "24": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "25": {"rule": "Extraction ou transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "26": {"rule": "Extraction", "requirement": "Entièrement extraits en Afrique", "regional_content": 100},
    "27": {"rule": "Extraction", "requirement": "Entièrement extraits en Afrique", "regional_content": 100},
    "28": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "29": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "30": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "31": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "32": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "33": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "34": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "35": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "36": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "37": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "38": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "39": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "40": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "41": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "42": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "43": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "44": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "45": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "46": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "47": {"rule": "Transformation substantielle", "requirement": "35% valeur ajoutée africaine", "regional_content": 35},
    "48": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "49": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "50": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "51": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "52": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "53": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "54": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "55": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "56": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "57": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "58": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "59": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "60": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "61": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "62": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "63": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "64": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "65": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "66": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "67": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "68": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "69": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "70": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "71": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "72": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "73": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "74": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "75": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "76": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "78": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "79": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "80": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "81": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "82": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "83": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "84": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "85": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "86": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "87": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "88": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "89": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "90": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "91": {"rule": "Transformation substantielle", "requirement": "45% valeur ajoutée africaine", "regional_content": 45},
    "92": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "93": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "94": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "95": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "96": {"rule": "Transformation substantielle", "requirement": "40% valeur ajoutée africaine", "regional_content": 40},
    "97": {"rule": "Œuvres d'art", "requirement": "Création africaine", "regional_content": 100},
}

# API Clients pour données externes
class WorldBankAPIClient:
    def __init__(self):
        self.base_url = "https://api.worldbank.org/v2"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'ZLECAf-API/1.0'})

    async def get_country_data(self, country_codes: List[str], indicators: List[str] = None) -> Dict[str, Any]:
        """Récupérer les données économiques des pays depuis la Banque Mondiale"""
        if indicators is None:
            indicators = ['NY.GDP.MKTP.CD', 'SP.POP.TOTL', 'NY.GDP.PCAP.CD', 'FP.CPI.TOTL.ZG']
        
        try:
            all_data = {}
            for country in country_codes:
                country_data = {}
                for indicator in indicators:
                    url = f"{self.base_url}/country/{country}/indicator/{indicator}"
                    params = {
                        'format': 'json',
                        'date': '2020:2023',
                        'per_page': 10
                    }
                    
                    response = self.session.get(url, params=params, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if len(data) > 1 and data[1]:
                            latest_data = data[1][0] if data[1] else None
                            if latest_data and latest_data['value']:
                                country_data[indicator] = {
                                    'value': latest_data['value'],
                                    'date': latest_data['date']
                                }
                
                all_data[country] = country_data
            
            return all_data
        except Exception as e:
            logging.error(f"Erreur World Bank API: {e}")
            return {}

class OECAPIClient:
    def __init__(self):
        self.base_url = "https://api-v2.oec.world"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'ZLECAf-API/1.0'})

    async def get_top_producers(self, hs_code: str, year: int = 2021) -> List[Dict[str, Any]]:
        """Récupérer le top 5 des pays africains producteurs pour un code SH"""
        try:
            endpoint = "tesseract/data.jsonrecords"
            params = {
                'cube': 'trade_i_hs4_eci',
                'drilldowns': 'Reporter',
                'measures': 'Export Value',
                'Product': hs_code[:4] if len(hs_code) > 4 else hs_code,
                'time': str(year),
                'Trade Flow': '2'  # Exports
            }
            
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and data['data']:
                    # Filtrer pour les pays africains seulement
                    african_codes = [country['iso3'] for country in AFRICAN_COUNTRIES]
                    african_exports = []
                    
                    for item in data['data']:
                        if item.get('Reporter') in african_codes:
                            african_exports.append({
                                'country_code': item.get('Reporter'),
                                'country_name': next((c['name'] for c in AFRICAN_COUNTRIES if c['iso3'] == item.get('Reporter')), item.get('Reporter')),
                                'export_value': item.get('Export Value', 0),
                                'year': year
                            })
                    
                    # Trier par valeur d'export et prendre le top 5
                    african_exports.sort(key=lambda x: x['export_value'], reverse=True)
                    return african_exports[:5]
            
            return []
        except Exception as e:
            logging.error(f"Erreur OEC API: {e}")
            return []

# Clients API globaux
wb_client = WorldBankAPIClient()
oec_client = OECAPIClient()

# Define Models
class CountryInfo(BaseModel):
    code: str  # ISO3 (code principal)
    iso2: str = ""  # ISO2 (pour les drapeaux)
    iso3: str  # ISO3 
    name: str
    region: str
    wb_code: str
    population: int

class TariffCalculationRequest(BaseModel):
    origin_country: str
    destination_country: str
    hs_code: str
    value: float

class TariffCalculationResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    origin_country: str
    destination_country: str
    hs_code: str
    hs6_code: Optional[str] = None  # Code SH6 extrait
    value: float
    # Tarifs normaux (hors ZLECAf)
    normal_tariff_rate: float
    normal_tariff_amount: float
    # Tarifs ZLECAf
    zlecaf_tariff_rate: float
    zlecaf_tariff_amount: float
    # TVA et autres taxes - Normal
    normal_vat_rate: float
    normal_vat_amount: float
    normal_statistical_fee: float
    normal_community_levy: float
    normal_ecowas_levy: float
    normal_other_taxes_total: float
    normal_total_cost: float
    # TVA et autres taxes - ZLECAf
    zlecaf_vat_rate: float
    zlecaf_vat_amount: float
    zlecaf_statistical_fee: float
    zlecaf_community_levy: float
    zlecaf_ecowas_levy: float
    zlecaf_other_taxes_total: float
    zlecaf_total_cost: float
    # Économies
    savings: float
    savings_percentage: float
    total_savings_with_taxes: float
    total_savings_percentage: float
    # Journal de calcul et traçabilité
    normal_calculation_journal: List[Dict[str, Any]]
    zlecaf_calculation_journal: List[Dict[str, Any]]
    computation_order_ref: str
    last_verified: str
    confidence_level: str
    # Précision tarifaire et sous-positions nationales
    tariff_precision: str = "chapter"  # sub_position, hs6_country, chapter
    sub_position_used: Optional[str] = None  # Code 8-12 chiffres si utilisé
    sub_position_description: Optional[str] = None
    has_varying_sub_positions: bool = False  # Si d'autres taux existent pour ce HS6
    available_sub_positions_count: int = 0
    # Règles d'origine
    rules_of_origin: Dict[str, Any]
    # Top producteurs africains
    top_african_producers: List[Dict[str, Any]]
    # Données économiques des pays
    origin_country_data: Dict[str, Any]
    destination_country_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CountryEconomicProfile(BaseModel):
    country_code: str
    country_name: str
    population: Optional[int] = None
    gdp_usd: Optional[float] = None
    gdp_per_capita: Optional[float] = None
    inflation_rate: Optional[float] = None
    region: str
    trade_profile: Dict[str, Any] = {}
    projections: Dict[str, Any] = {}
    risk_ratings: Dict[str, Any] = {}
    customs: Dict[str, Any] = {}
    infrastructure_ranking: Dict[str, Any] = {}
    ongoing_projects: List[Dict[str, Any]] = []

# Routes
@api_router.get("/")
async def root():
    return {"message": "Système Commercial ZLECAf API - Version Complète"}

@api_router.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "service": "ZLECAf API",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@api_router.get("/health/status")
async def detailed_health_status():
    """Detailed health status with system checks"""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "ZLECAf API",
        "version": "2.0.0",
        "checks": {}
    }
    
    # Check database connection
    try:
        await db.command("ping")
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "MongoDB connection active"
        }
    except Exception as e:
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "message": f"Database connection error: {str(e)}"
        }
        health_status["status"] = "unhealthy"
    
    # Check API endpoints availability
    health_status["checks"]["api_endpoints"] = {
        "status": "healthy",
        "available_endpoints": [
            "/api/",
            "/api/health",
            "/api/health/status",
            "/api/countries",
            "/api/country-profile/{country_code}",
            "/api/calculate-tariff",
            "/api/rules-of-origin/{hs_code}",
            "/api/statistics"
        ]
    }
    
    # Check data availability
    health_status["checks"]["data"] = {
        "status": "healthy",
        "countries_count": len(AFRICAN_COUNTRIES),
        "rules_of_origin_sectors": len(ZLECAF_RULES_OF_ORIGIN)
    }
    
    return health_status

@api_router.get("/countries")
async def get_countries(lang: str = "fr"):
    """Récupérer la liste des pays membres de la ZLECAf avec traduction
    
    Retourne ISO3 comme code principal, ISO2 conservé pour compatibilité (drapeaux)
    """
    countries = []
    for country in AFRICAN_COUNTRIES:
        translated_country = {
            "code": country["iso3"],  # ISO3 comme code principal
            "iso2": country["code"],  # ISO2 conservé pour les drapeaux
            "iso3": country["iso3"],
            "name": translate_country_name(country["code"], lang),
            "region": translate_region(country["region"], lang),
            "wb_code": country.get("wb_code", country["iso3"]),
            "population": country["population"]
        }
        countries.append(CountryInfo(**translated_country))
    return countries

@api_router.get("/country-profile/{country_code}")
async def get_country_profile(country_code: str) -> CountryEconomicProfile:
    """Récupérer le profil économique complet d'un pays avec données réelles et commerce 2024
    
    Accepte les codes ISO2 (ex: DZ) ou ISO3 (ex: DZA)
    """
    code_upper = country_code.upper()
    
    # Chercher par ISO3 d'abord, puis ISO2 (rétrocompatibilité)
    country = next((c for c in AFRICAN_COUNTRIES if c['iso3'] == code_upper), None)
    if not country:
        country = next((c for c in AFRICAN_COUNTRIES if c['code'] == code_upper), None)
    
    if not country:
        raise HTTPException(status_code=404, detail="Pays non trouvé dans la ZLECAf")
    
    # Utiliser ISO3 pour toutes les requêtes de données
    iso3_code = country['iso3']
    
    # Récupérer les données de commerce enrichies 2024
    commerce_data = get_country_commerce_profile(iso3_code)
    
    # Récupérer les données réelles du pays (fallback)
    real_data = get_country_data(iso3_code)
    
    # Construire le profil avec données commerce 2024 en priorité
    if commerce_data:
        profile = CountryEconomicProfile(
            country_code=iso3_code,  # Retourner ISO3
            country_name=commerce_data['country'],
            population=int(commerce_data['population_2024_million'] * 1000000) if commerce_data['population_2024_million'] else country['population'],
            region=country['region']
        )
        
        # Données économiques 2024
        profile.gdp_usd = commerce_data['gdp_2024_billion_usd'] * 1000000000 if commerce_data['gdp_2024_billion_usd'] else None
        profile.gdp_per_capita = commerce_data['gdp_per_capita_2024']
        profile.inflation_rate = None
        
        # Projections enrichies avec données commerce
        profile.projections = {
            "gdp_growth_forecast_2024": f"{commerce_data['growth_rate_2024']}%" if commerce_data['growth_rate_2024'] else '3.0%',
            "gdp_growth_projection_2025": real_data.get('growth_projection_2025', '3.2%'),
            "gdp_growth_projection_2026": real_data.get('growth_projection_2026', '3.5%'),
            "development_index": commerce_data['hdi_2024'] if commerce_data['hdi_2024'] else 0.500,
            "africa_rank": real_data.get('africa_rank', 25),
            "key_sectors": [f"{sector['name']} ({sector['pib_share']}% PIB): {sector['description']}" 
                           for sector in real_data.get('key_sectors', [])],
            "zlecaf_potential_level": real_data.get('zlecaf_potential', {}).get('level', 'Modéré'),
            "zlecaf_potential_description": real_data.get('zlecaf_potential', {}).get('description', ''),
            "zlecaf_opportunities": real_data.get('zlecaf_potential', {}).get('key_opportunities', []),
            "main_exports": commerce_data['export_products'],
            "main_imports": commerce_data['import_products'],
            "export_partners": commerce_data['export_partners'],
            "import_partners": commerce_data['import_partners'],
            "exports_2024_billion_usd": commerce_data['exports_2024_billion_usd'],
            "imports_2024_billion_usd": commerce_data['imports_2024_billion_usd'],
            "trade_balance_2024_billion_usd": commerce_data['trade_balance_2024_billion_usd'],
            "zlecaf_ratified": commerce_data['zlecaf_ratified'],
            "zlecaf_ratification_date": commerce_data['zlecaf_ratification_date'],
            "investment_climate_score": "B+",
            "infrastructure_index": 6.7,
            "business_environment_rank": real_data.get('africa_rank', 25),
            # Infrastructure data from CSV
            "international_ports": commerce_data.get('infrastructure', {}).get('international_ports', 2),
            "domestic_ports": commerce_data.get('infrastructure', {}).get('domestic_ports', 5),
            "international_airports": commerce_data.get('infrastructure', {}).get('international_airports', 2),
            "domestic_airports": commerce_data.get('infrastructure', {}).get('domestic_airports', 10),
            "railways_km": commerce_data.get('infrastructure', {}).get('railways_km', 0),
            "external_debt_gdp_pct": commerce_data.get('infrastructure', {}).get('external_debt_pct_gdp', 60.0),
            "energy_cost_kwh": commerce_data.get('infrastructure', {}).get('energy_cost_usd_kwh', 0.20)
        }
        
        # World Bank Data360 indicators
        wb_data = commerce_data.get('world_bank_data', {})
        if wb_data:
            for key, value in wb_data.items():
                if value is not None:
                    profile.projections[key] = value
        
        # Gold reserves data
        gold_data = GOLD_RESERVES_GAI_DATA['gold_reserves'].get(country['iso3'], {})
        if gold_data:
            profile.projections['gold_reserves_tonnes'] = gold_data.get('tonnes', 0.0)
            profile.projections['gold_reserves_rank_africa'] = gold_data.get('rank_africa')
            profile.projections['gold_reserves_rank_global'] = gold_data.get('rank_global')
        
        # Global Attractiveness Index 2025
        gai_data = GOLD_RESERVES_GAI_DATA['global_attractiveness_index_2025'].get(country['iso3'], {})
        if gai_data:
            profile.projections['gai_2025_score'] = gai_data.get('score')
            profile.projections['gai_2025_rank_africa'] = gai_data.get('rank_africa')
            profile.projections['gai_2025_rank_global'] = gai_data.get('rank_global')
            profile.projections['gai_2025_rating'] = gai_data.get('rating')
            profile.projections['gai_2025_trend'] = gai_data.get('trend')
        
        # Notations de risque 2024
        profile.risk_ratings = commerce_data['ratings']
        
        # Customs information
        customs_info = get_country_customs_info(commerce_data['country'])
        profile.customs = customs_info if customs_info else {}
        
        # Infrastructure ranking - avec normalisation robuste des noms
        import unicodedata
        def normalize_name(s):
            # D'ABORD remplacer les apostrophes typographiques par ASCII AVANT l'encodage
            s = s.replace('\u2019', "'").replace('\u2018', "'")  # ' et ' → '
            # Puis normaliser les accents et convertir en minuscules
            normalized = unicodedata.normalize('NFD', s.lower()).encode('ascii', 'ignore').decode('ascii')
            return normalized
        
        country_search_name = commerce_data['country']
        infra_ranking = None
        
        # Charger directement le fichier JSON
        try:
            import json
            with open('/app/classement_infrastructure_afrique.json', 'r') as f:
                infra_data = json.load(f)
            
            # Normaliser le nom de recherche et gérer les apostrophes
            search_name = normalize_name(country_search_name)
            
            for entry in infra_data:
                entry_name = normalize_name(entry['pays'])
                # Comparaison stricte et partielle pour plus de robustesse
                if entry_name == search_name or search_name in entry_name or entry_name in search_name:
                    infra_ranking = {
                        'africa_rank': entry['rang_afrique'],
                        'lpi_infrastructure_score': entry['score_infrastructure_ipl'],
                        'lpi_world_rank': entry['rang_mondial_ipl'],
                        'aidi_transport_score': entry.get('score_aidi_2024', entry.get('score_transport_aidi', 0))
                    }
                    logging.info(f"✅ Infrastructure trouvée pour {country_search_name}: LPI={infra_ranking['lpi_infrastructure_score']}, AIDI={infra_ranking['aidi_transport_score']}")
                    break
        except Exception as e:
            logging.error(f"Erreur chargement infrastructure: {e}")
        
        # Projets structurants
        profile.ongoing_projects = get_country_ongoing_projects(iso3_code)
        profile.infrastructure_ranking = infra_ranking if infra_ranking else {}
    else:
        # Fallback to old data
        profile = CountryEconomicProfile(
            country_code=country['code'],
            country_name=country['name'],
            population=real_data.get('population_2024', country['population']),
            region=country['region']
        )
        
        profile.gdp_usd = real_data.get('gdp_usd_2024')
        profile.gdp_per_capita = real_data.get('gdp_per_capita_2024')
        profile.inflation_rate = None
        
        profile.projections = {
            "gdp_growth_forecast_2024": real_data.get('growth_forecast_2024', '3.0%'),
            "gdp_growth_projection_2025": real_data.get('growth_projection_2025', '3.2%'),
            "gdp_growth_projection_2026": real_data.get('growth_projection_2026', '3.5%'),
            "development_index": real_data.get('development_index', 0.500),
            "africa_rank": real_data.get('africa_rank', 25),
            "key_sectors": [f"{sector['name']} ({sector['pib_share']}% PIB): {sector['description']}" 
                           for sector in real_data.get('key_sectors', [])],
            "zlecaf_potential_level": real_data.get('zlecaf_potential', {}).get('level', 'Modéré'),
            "zlecaf_potential_description": real_data.get('zlecaf_potential', {}).get('description', ''),
            "zlecaf_opportunities": real_data.get('zlecaf_potential', {}).get('key_opportunities', []),
            "main_exports": real_data.get('main_exports', []),
            "main_imports": real_data.get('main_imports', []),
            "investment_climate_score": "B+",
            "infrastructure_index": 6.7,
            "business_environment_rank": real_data.get('africa_rank', 25)
        }
        
        # Gold reserves data
        gold_data = GOLD_RESERVES_GAI_DATA['gold_reserves'].get(country['iso3'], {})
        if gold_data:
            profile.projections['gold_reserves_tonnes'] = gold_data.get('tonnes', 0.0)
            profile.projections['gold_reserves_rank_africa'] = gold_data.get('rank_africa')
            profile.projections['gold_reserves_rank_global'] = gold_data.get('rank_global')
        
        # Global Attractiveness Index 2025
        gai_data = GOLD_RESERVES_GAI_DATA['global_attractiveness_index_2025'].get(country['iso3'], {})
        if gai_data:
            profile.projections['gai_2025_score'] = gai_data.get('score')
            profile.projections['gai_2025_rank_africa'] = gai_data.get('rank_africa')
            profile.projections['gai_2025_rank_global'] = gai_data.get('rank_global')
            profile.projections['gai_2025_rating'] = gai_data.get('rating')
            profile.projections['gai_2025_trend'] = gai_data.get('trend')
        
        profile.risk_ratings = real_data.get('risk_ratings', {
            "sp": "NR",
            "moodys": "NR", 
            "fitch": "NR",
            "scope": "NR",
            "global_risk": "Non évalué"
        })
        
        # Customs information
        customs_info = get_country_customs_info(country['name'])
        profile.customs = customs_info if customs_info else {}
        
        # Projets structurants
        profile.ongoing_projects = get_country_ongoing_projects(country['iso3'])
        # Infrastructure ranking
        infra_ranking = get_country_infrastructure_ranking(country['name'])
        profile.infrastructure_ranking = infra_ranking if infra_ranking else {}
    
    return profile

@api_router.get("/rules-of-origin/{hs_code}")
async def get_rules_of_origin(hs_code: str, lang: str = "fr"):
    """Récupérer les règles d'origine ZLECAf pour un code SH"""
    
    # Obtenir le code à 2 chiffres pour les règles générales
    sector_code = hs_code[:2]
    
    if sector_code not in ZLECAF_RULES_OF_ORIGIN:
        error_msg = "Rules of origin not found for this HS code" if lang == "en" else "Règles d'origine non trouvées pour ce code SH"
        raise HTTPException(status_code=404, detail=error_msg)
    
    rules = ZLECAF_RULES_OF_ORIGIN[sector_code]
    
    # Translate rules
    translated_rules = {
        "rule": translate_rule(rules["rule"], lang),
        "requirement": translate_rule(rules["requirement"], lang),
        "regional_content": rules["regional_content"]
    }
    
    # Documentation labels
    if lang == "en":
        docs = [
            "AfCFTA Certificate of Origin",
            "Commercial Invoice",
            "Packing List",
            "Supplier Declaration"
        ]
        validity = "12 months"
        authority = "Competent authority of exporting country"
    else:
        docs = [
            "Certificat d'origine ZLECAf",
            "Facture commerciale",
            "Liste de colisage",
            "Déclaration du fournisseur"
        ]
        validity = "12 mois"
        authority = "Autorité compétente du pays exportateur"
    
    return {
        "hs_code": hs_code,
        "sector_code": sector_code,
        "rules": translated_rules,
        "explanation": {
            "rule_type": translated_rules["rule"],
            "requirement": translated_rules["requirement"],
            "regional_content_minimum": f"{rules['regional_content']}%",
            "documentation_required": docs,
            "validity_period": validity,
            "issuing_authority": authority
        }
    }

@api_router.post("/calculate-tariff", response_model=TariffCalculationResponse)
async def calculate_comprehensive_tariff(request: TariffCalculationRequest):
    """Calculer les tarifs complets avec données officielles 2025 et règles d'origine
    
    Accepte les codes ISO2 (ex: DZ) ou ISO3 (ex: DZA) pour les pays
    Supporte les codes HS de 6 à 12 chiffres pour plus de précision
    
    ORDRE DE PRIORITÉ DES TARIFS:
    1. Sous-position nationale (8-12 chiffres) si fournie
    2. Tarif SH6 spécifique au pays
    3. Tarif par chapitre du pays
    """
    
    # Chercher par ISO3 d'abord, puis ISO2 (rétrocompatibilité)
    origin_country = next((c for c in AFRICAN_COUNTRIES if c['iso3'] == request.origin_country.upper()), None)
    if not origin_country:
        origin_country = next((c for c in AFRICAN_COUNTRIES if c['code'] == request.origin_country.upper()), None)
    
    dest_country = next((c for c in AFRICAN_COUNTRIES if c['iso3'] == request.destination_country.upper()), None)
    if not dest_country:
        dest_country = next((c for c in AFRICAN_COUNTRIES if c['code'] == request.destination_country.upper()), None)
    
    if not origin_country or not dest_country:
        raise HTTPException(status_code=400, detail="L'un des pays sélectionnés n'est pas membre de la ZLECAf")
    
    # Utiliser ISO3 pour les calculs
    dest_iso3 = dest_country['iso3']
    origin_iso3 = origin_country['iso3']
    
    # Nettoyer et normaliser le code HS
    hs_code_clean = request.hs_code.replace(".", "").replace(" ", "")
    hs6_code = hs_code_clean[:6].zfill(6)
    sector_code = hs6_code[:2]
    
    # Variables pour traçabilité
    tariff_precision = "chapter"
    sub_position_used = None
    sub_position_description = None
    
    # ============================================================
    # PRIORITÉ 1: Sous-position nationale (8-12 chiffres)
    # ============================================================
    if len(hs_code_clean) > 6:
        rate, description, source = get_sub_position_rate(dest_iso3, hs_code_clean)
        if rate is not None:
            normal_rate = rate
            npf_source = f"Sous-position nationale {dest_iso3} ({hs_code_clean})"
            tariff_precision = "sub_position"
            sub_position_used = hs_code_clean
            sub_position_description = description
    
    # ============================================================
    # PRIORITÉ 2: Tarifs SH6 RÉELS par pays de destination
    # ============================================================
    if tariff_precision == "chapter":
        hs6_tariff = get_country_hs6_tariff(dest_iso3, hs6_code)
        
        if hs6_tariff:
            normal_rate = hs6_tariff["dd"]
            npf_source = f"Tarif SH6 {dest_iso3} ({hs6_code})"
            tariff_precision = "hs6_country"
        else:
            # PRIORITÉ 3: Fallback vers taux par chapitre du pays
            normal_rate, npf_source = get_tariff_rate_for_country(dest_iso3, hs6_code)
            tariff_precision = "chapter"
    
    # Obtenir le taux ZLECAf calculé selon le calendrier de libéralisation
    # Le taux ZLECAf est calculé à partir du taux normal avec réduction progressive
    from etl.country_tariffs_complete import get_product_category, get_zlecaf_reduction_factor
    product_category = get_product_category(hs6_code)
    reduction_factor = get_zlecaf_reduction_factor(dest_iso3, product_category)
    zlecaf_rate = normal_rate * reduction_factor
    zlecaf_source = f"ZLECAf ({product_category})"
    
    # Obtenir le taux de TVA du pays
    vat_rate, vat_source = get_vat_rate_for_country(dest_iso3)
    
    # Obtenir les autres taxes du pays
    other_taxes_rate, other_taxes_detail = get_other_taxes_for_country(dest_iso3)
    
    # Source de tarif pour affichage
    rate_source = f"Tarif officiel {dest_iso3} - {npf_source}"
    
    # Période de transition selon le secteur
    tariff_corrections = get_tariff_corrections()
    transition_periods = tariff_corrections.get('transition_periods', {})
    transition_period = transition_periods.get(sector_code, 'immediate')
    
    # ============================================================
    # CALCULS DES MONTANTS
    # ============================================================
    
    # Droits de douane
    normal_customs = request.value * normal_rate
    zlecaf_customs = request.value * zlecaf_rate
    
    # Autres taxes (sur valeur CIF)
    other_taxes_amount = request.value * other_taxes_rate
    
    # TVA calculée sur (Valeur + DD + Autres taxes)
    normal_vat_base = request.value + normal_customs + other_taxes_amount
    zlecaf_vat_base = request.value + zlecaf_customs + other_taxes_amount
    
    normal_vat_amount = normal_vat_base * vat_rate
    zlecaf_vat_amount = zlecaf_vat_base * vat_rate
    
    # Totaux
    normal_total = request.value + normal_customs + other_taxes_amount + normal_vat_amount
    zlecaf_total = request.value + zlecaf_customs + other_taxes_amount + zlecaf_vat_amount
    
    # Économies
    savings = normal_customs - zlecaf_customs
    savings_percentage = (savings / normal_customs) * 100 if normal_customs > 0 else 0
    total_savings_with_taxes = normal_total - zlecaf_total
    total_savings_percentage = (total_savings_with_taxes / normal_total) * 100 if normal_total > 0 else 0
    
    # Préparer les détails des taxes pour le journal de calcul
    # Extraire les composantes des autres taxes
    rs_rate = other_taxes_detail.get('rs', 0) / 100 if other_taxes_detail.get('rs') else 0
    pcs_rate = other_taxes_detail.get('pcs', 0) / 100 if other_taxes_detail.get('pcs') else 0
    cedeao_rate = other_taxes_detail.get('cedeao', 0) / 100 if other_taxes_detail.get('cedeao') else 0
    tci_rate = other_taxes_detail.get('tci', 0) / 100 if other_taxes_detail.get('tci') else 0
    
    # Créer le journal de calcul détaillé pour NPF
    normal_journal = [
        {"step": 1, "component": "Valeur CIF", "base": request.value, "rate": "-", "amount": request.value, "cumulative": request.value},
        {"step": 2, "component": "Droits de douane", "base": request.value, "rate": f"{normal_rate*100:.1f}%", "amount": round(normal_customs, 2), "cumulative": round(request.value + normal_customs, 2)},
    ]
    step = 3
    if rs_rate > 0:
        normal_journal.append({"step": step, "component": "Redevance statistique", "base": request.value, "rate": f"{rs_rate*100:.1f}%", "amount": round(request.value * rs_rate, 2), "cumulative": round(request.value + normal_customs + request.value * rs_rate, 2)})
        step += 1
    if pcs_rate > 0:
        normal_journal.append({"step": step, "component": "PCS UEMOA", "base": request.value, "rate": f"{pcs_rate*100:.1f}%", "amount": round(request.value * pcs_rate, 2), "cumulative": round(request.value + normal_customs + other_taxes_amount, 2)})
        step += 1
    if cedeao_rate > 0:
        normal_journal.append({"step": step, "component": "Prélèvement CEDEAO", "base": request.value, "rate": f"{cedeao_rate*100:.1f}%", "amount": round(request.value * cedeao_rate, 2), "cumulative": round(request.value + normal_customs + other_taxes_amount, 2)})
        step += 1
    if tci_rate > 0:
        normal_journal.append({"step": step, "component": "TCI CEMAC", "base": request.value, "rate": f"{tci_rate*100:.1f}%", "amount": round(request.value * tci_rate, 2), "cumulative": round(request.value + normal_customs + other_taxes_amount, 2)})
        step += 1
    normal_journal.append({"step": step, "component": "TVA", "base": round(normal_vat_base, 2), "rate": f"{vat_rate*100:.1f}%", "amount": round(normal_vat_amount, 2), "cumulative": round(normal_total, 2)})
    
    # Créer le journal de calcul détaillé pour ZLECAf
    zlecaf_journal = [
        {"step": 1, "component": "Valeur CIF", "base": request.value, "rate": "-", "amount": request.value, "cumulative": request.value},
        {"step": 2, "component": "Droits de douane ZLECAf", "base": request.value, "rate": f"{zlecaf_rate*100:.1f}%", "amount": round(zlecaf_customs, 2), "cumulative": round(request.value + zlecaf_customs, 2)},
    ]
    step = 3
    if other_taxes_rate > 0:
        zlecaf_journal.append({"step": step, "component": "Autres taxes", "base": request.value, "rate": f"{other_taxes_rate*100:.1f}%", "amount": round(other_taxes_amount, 2), "cumulative": round(request.value + zlecaf_customs + other_taxes_amount, 2)})
        step += 1
    zlecaf_journal.append({"step": step, "component": "TVA", "base": round(zlecaf_vat_base, 2), "rate": f"{vat_rate*100:.1f}%", "amount": round(zlecaf_vat_amount, 2), "cumulative": round(zlecaf_total, 2)})
    
    # Règles d'origine
    rules = ZLECAF_RULES_OF_ORIGIN.get(sector_code, {
        "rule": "Transformation substantielle",
        "requirement": "40% valeur ajoutée africaine",
        "regional_content": 40
    })
    
    # Récupérer les top producteurs africains
    top_producers = await oec_client.get_top_producers(request.hs_code)
    
    # Récupérer les données économiques des pays
    wb_data = await wb_client.get_country_data([origin_country['wb_code'], dest_country['wb_code']])
    
    # Vérifier si des sous-positions alternatives existent pour ce HS6
    sub_positions_available = get_all_sub_positions(dest_iso3, hs6_code)
    has_varying, min_rate, max_rate = has_varying_rates(dest_iso3, hs6_code)
    
    # Création de la réponse complète avec toutes les taxes
    result = TariffCalculationResponse(
        origin_country=request.origin_country,
        destination_country=request.destination_country,
        hs_code=request.hs_code,
        hs6_code=hs6_code,
        value=request.value,
        # Tarifs de douane
        normal_tariff_rate=normal_rate,
        normal_tariff_amount=round(normal_customs, 2),
        zlecaf_tariff_rate=zlecaf_rate,
        zlecaf_tariff_amount=round(zlecaf_customs, 2),
        # Taxes normales (NPF)
        normal_vat_rate=vat_rate,
        normal_vat_amount=round(normal_vat_amount, 2),
        normal_statistical_fee=round(request.value * rs_rate, 2),
        normal_community_levy=round(request.value * pcs_rate, 2),
        normal_ecowas_levy=round(request.value * cedeao_rate, 2),
        normal_other_taxes_total=round(other_taxes_amount, 2),
        normal_total_cost=round(normal_total, 2),
        # Taxes ZLECAf
        zlecaf_vat_rate=vat_rate,
        zlecaf_vat_amount=round(zlecaf_vat_amount, 2),
        zlecaf_statistical_fee=round(request.value * rs_rate, 2),
        zlecaf_community_levy=round(request.value * pcs_rate, 2),
        zlecaf_ecowas_levy=round(request.value * cedeao_rate, 2),
        zlecaf_other_taxes_total=round(other_taxes_amount, 2),
        zlecaf_total_cost=round(zlecaf_total, 2),
        # Économies
        savings=round(savings, 2),
        savings_percentage=round(savings_percentage, 1),
        total_savings_with_taxes=round(total_savings_with_taxes, 2),
        total_savings_percentage=round(total_savings_percentage, 1),
        # Journal de calcul et traçabilité
        normal_calculation_journal=normal_journal,
        zlecaf_calculation_journal=zlecaf_journal,
        computation_order_ref="Codes douaniers nationaux + Directives CEDEAO/UEMOA/CEMAC/EAC/SACU",
        last_verified="2025-01",
        confidence_level="high" if tariff_precision in ["sub_position", "hs6_country"] else "medium",
        # Précision tarifaire et sous-positions
        tariff_precision=tariff_precision,
        sub_position_used=sub_position_used,
        sub_position_description=sub_position_description,
        has_varying_sub_positions=has_varying,
        available_sub_positions_count=len(sub_positions_available),
        # Autres données
        rules_of_origin=rules,
        top_african_producers=top_producers,
        origin_country_data=wb_data.get(origin_country['wb_code'], {}),
        destination_country_data=wb_data.get(dest_country['wb_code'], {})
    )
    
    # Sauvegarder en base de données
    await db.comprehensive_calculations.insert_one(result.dict())
    
    return result

@api_router.get("/statistics")
async def get_comprehensive_statistics():
    """Récupérer les statistiques complètes ZLECAf avec données enrichies 2024"""
    
    # Charger les statistiques enrichies depuis le JSON 2024
    enhanced_stats = get_enhanced_statistics()
    
    # Statistiques de base de la DB
    total_calculations = await db.comprehensive_calculations.count_documents({})
    
    # Économies totales
    pipeline_savings = [
        {"$group": {"_id": None, "total_savings": {"$sum": "$savings"}}}
    ]
    savings_result = await db.comprehensive_calculations.aggregate(pipeline_savings).to_list(1)
    total_savings = savings_result[0]["total_savings"] if savings_result else 0
    
    # Pays les plus actifs
    pipeline_countries = [
        {"$group": {"_id": "$origin_country", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    countries_result = await db.comprehensive_calculations.aggregate(pipeline_countries).to_list(10)
    
    # Codes SH les plus utilisés
    pipeline_hs = [
        {"$group": {"_id": "$hs_code", "count": {"$sum": 1}, "avg_savings": {"$avg": "$savings"}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    hs_result = await db.comprehensive_calculations.aggregate(pipeline_hs).to_list(10)
    
    # Secteurs les plus bénéficiaires
    pipeline_sectors = [
        {"$addFields": {"sector": {"$substr": ["$hs_code", 0, 2]}}},
        {"$group": {"_id": "$sector", "count": {"$sum": 1}, "total_savings": {"$sum": "$savings"}}},
        {"$sort": {"total_savings": -1}},
        {"$limit": 10}
    ]
    sectors_result = await db.comprehensive_calculations.aggregate(pipeline_sectors).to_list(10)
    
    # Calcul de l'impact économique potentiel
    african_population = sum([country['population'] for country in AFRICAN_COUNTRIES])
    
    # Utiliser les données enrichies 2024 pour l'overview
    overview_enhanced = enhanced_stats.get('overview', {})
    
    # Générer le VRAI Top 10 exportateurs et importateurs depuis les données complètes
    trade_data_all = get_all_countries_trade_performance()
    
    # Top 10 exportateurs (triés par exports décroissants)
    top_10_exporters = sorted(trade_data_all, key=lambda x: x['exports_2024'], reverse=True)[:10]
    total_exports = sum([c['exports_2024'] for c in trade_data_all])
    top_exporters_formatted = [
        {
            "rank": idx + 1,
            "country": country['code'],
            "name": country['country'],
            "exports_2024": country['exports_2024'] * 1e9,  # Convert to USD
            "share_pct": round((country['exports_2024'] / total_exports) * 100, 1) if total_exports > 0 else 0
        }
        for idx, country in enumerate(top_10_exporters)
    ]
    
    # Top 10 importateurs (triés par imports décroissants)
    top_10_importers = sorted(trade_data_all, key=lambda x: x['imports_2024'], reverse=True)[:10]
    total_imports = sum([c['imports_2024'] for c in trade_data_all])
    top_importers_formatted = [
        {
            "rank": idx + 1,
            "country": country['code'],
            "name": country['country'],
            "imports_2024": country['imports_2024'] * 1e9,  # Convert to USD
            "share_pct": round((country['imports_2024'] / total_imports) * 100, 1) if total_imports > 0 else 0
        }
        for idx, country in enumerate(top_10_importers)
    ]
    
    # Top 5 PIB avec comparaison échanges intra-africains vs monde
    top_5_gdp = sorted(trade_data_all, key=lambda x: x['gdp_2024'], reverse=True)[:5]
    top_5_gdp_formatted = []
    
    # Charger les données intra-africaines
    intra_response = await get_trade_performance_intra_african()
    intra_data_dict = {item['code']: item for item in intra_response['countries_intra_african']}
    
    for country in top_5_gdp:
        intra_info = intra_data_dict.get(country['code'], {})
        top_5_gdp_formatted.append({
            "country": country['country'],
            "code": country['code'],
            "gdp_2024": country['gdp_2024'],
            "exports_world": country['exports_2024'],
            "imports_world": country['imports_2024'],
            "exports_intra_african": intra_info.get('exports_2024', 0),
            "imports_intra_african": intra_info.get('imports_2024', 0),
            "intra_african_percentage": intra_info.get('intra_african_percentage', 17)
        })
    
    # Top 10 PIB 2024 avec projections de croissance 2025
    from country_data import REAL_COUNTRY_DATA
    top_10_gdp = sorted(trade_data_all, key=lambda x: x['gdp_2024'], reverse=True)[:10]
    top_10_gdp_formatted = []
    
    # Mapping code ISO2 -> ISO3
    iso2_to_iso3 = {c['code']: c['iso3'] for c in AFRICAN_COUNTRIES}
    
    for idx, country in enumerate(top_10_gdp):
        iso3_code = iso2_to_iso3.get(country['code'], country['code'])
        country_real_data = REAL_COUNTRY_DATA.get(iso3_code, {})
        
        top_10_gdp_formatted.append({
            "rank": idx + 1,
            "country": country['country'],
            "code": country['code'],
            "gdp_2024_billion": round(country['gdp_2024'], 2),
            "growth_2024": country.get('growth_rate_2024', country_real_data.get('growth_forecast_2024', 'N/A')),
            "growth_projection_2025": country_real_data.get('growth_projection_2025', 'N/A'),
            "population_million": round(country_real_data.get('population_2024', 0) / 1e6, 1) if country_real_data.get('population_2024') else 'N/A',
            "gdp_per_capita": country_real_data.get('gdp_per_capita_2024', 'N/A')
        })
    
    
    # Calculer totaux pour trade_evolution
    trade_evolution_data = enhanced_stats.get('trade_evolution', {})
    trade_evolution_data.update({
        "total_exports_2024": round(total_exports, 1),
        "total_imports_2024": round(total_imports, 1),
        "intra_african_trade_2023": trade_evolution_data.get("intra_african_trade_2023", 192.4),
        "intra_african_trade_2024": trade_evolution_data.get("intra_african_trade_2024", 218.7),
        "projected_intra_trade_2030": trade_evolution_data.get("projected_intra_trade_2030", 385.0),
        "growth_rate_2023_2024": trade_evolution_data.get("growth_rate_2023_2024", 13.7)
    })
    
    return {
        "overview": {
            "total_calculations": overview_enhanced.get('total_calculations', total_calculations),
            "total_savings": overview_enhanced.get('total_savings', total_savings),
            "african_countries_members": overview_enhanced.get('african_countries_members', len(AFRICAN_COUNTRIES)),
            "combined_population": overview_enhanced.get('combined_population', african_population),
            "estimated_combined_gdp": overview_enhanced.get('estimated_combined_gdp', 2706000000000),
            "zlecaf_implementation_status": overview_enhanced.get('zlecaf_implementation_status', '')
        },
        "trade_evolution": trade_evolution_data,
        "top_exporters_2024": top_exporters_formatted,
        "top_importers_2024": top_importers_formatted,
        "top_10_gdp_2024": top_10_gdp_formatted,
        "top_5_gdp_trade_comparison": top_5_gdp_formatted,
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
            "intra_african_trade_target": "25% d'ici 2030",
            "current_intra_african_trade": "15.2%",
            "poverty_reduction": "30 millions de personnes d'ici 2035",
            "income_gains_2035": "450 milliards USD",
            "export_increase_2035": "560 milliards USD (forte composante manufacturière)"
        },
        "projections": {
            "2025": enhanced_stats.get('projections_updated', {}).get('2025', {
                "trade_volume_increase": "15%",
                "tariff_eliminations": "90%",
                "new_trade_corridors": 45,
                "gti_active_corridors": "8 corridors prioritaires"
            }),
            "2030": enhanced_stats.get('projections_updated', {}).get('2030', {
                "trade_volume_increase": "52%",
                "gdp_increase": "7%",
                "industrialization_boost": "35%",
                "tariff_revenue_change": "+3% (malgré baisse des taux)"
            }),
            "2035": {
                "income_gains": "450 milliards USD",
                "poverty_reduction": "30 millions de personnes",
                "export_increase": "560 milliards USD",
                "intra_african_trade": "25-30%"
            },
            "2040": {
                "trade_volume_increase_conservative": "15%",
                "trade_volume_increase_median": "20%",
                "trade_volume_increase_ambitious": "25%",
                "estimated_additional_trade": "50-70 milliards USD"
            }
        },
        "scenarios": {
            "conservative": {
                "description": "Mise en œuvre lente, obstacles persistants",
                "trade_increase_2040": "15%",
                "additional_value": "50 milliards USD"
            },
            "median": {
                "description": "Mise en œuvre progressive, réduction graduelle NTB",
                "trade_increase_2040": "20%",
                "additional_value": "60 milliards USD"
            },
            "ambitious": {
                "description": "Mise en œuvre rapide, élimination NTB, infrastructure optimale",
                "trade_increase_2040": "25%",
                "additional_value": "70 milliards USD"
            }
        },
        "key_mechanisms": {
            "digital_trade_protocol": {
                "adoption_date": "2024-02-18",
                "status": "Adopté",
                "focus": "Harmonisation règles, flux transfrontières, confiance numérique"
            },
            "ntb_platform": {
                "url": "https://tradebarriers.africa",
                "status": "Opérationnel",
                "purpose": "Signalement et résolution obstacles non tarifaires"
            },
            "papss_payments": {
                "status": "Déploiement en cours",
                "purpose": "Système panafricain de paiements et règlements"
            },
            "gti": {
                "status": "Actif",
                "purpose": "Guided Trade Initiative - montée en charge progressive"
            }
        },
        "data_sources": [
            {
                "source": "Union Africaine - AfCFTA Secretariat",
                "url": "https://au.int/en/cfta",
                "verified": "2025-01-11"
            },
            {
                "source": "Banque Mondiale - The African Continental Free Trade Area",
                "url": "https://www.worldbank.org/en/topic/trade/publication/the-african-continental-free-trade-area",
                "key_findings": "Gains de 450 Md$, 30M sorties pauvreté (2035)",
                "verified": "2025-01-11"
            },
            {
                "source": "UNECA - Economic Commission for Africa",
                "url": "https://www.uneca.org/",
                "key_findings": "Projections +15-25% échanges intra-africains (2040)",
                "verified": "2025-01-11"
            },
            {
                "source": "UNCTAD - Trade Data",
                "url": "https://unctad.org/",
                "verified": "2025-01-11"
            },
            {
                "source": "tralac - Trade Law Centre",
                "url": "https://www.tralac.org/",
                "focus": "GTI, transposition nationale, suivi juridique",
                "verified": "2025-01-11"
            },
            {
                "source": "AfCFTA NTB Platform",
                "url": "https://tradebarriers.africa",
                "status": "Opérationnel",
                "verified": "2025-01-11"
            }
        ],
        "last_updated": datetime.now().isoformat()
    }

@api_router.get("/trade-performance")
async def get_trade_performance():
    """Récupérer les données de performance commerciale 2024 pour tous les pays"""
    
    # Charger les données de commerce enrichies (COMMERCE MONDIAL)
    trade_data = get_all_countries_trade_performance()
    
    return {
        "countries_global": trade_data,
        "data_source": "Observatory of Economic Complexity (OEC) 2024, World Bank, IMF",
        "last_updated": "2024-09-16",
        "year": 2024,
        "trade_type": "global",
        "description": "Commerce total avec tous les partenaires mondiaux (Europe, Asie, Amériques, etc.)"
    }

@api_router.get("/trade-performance-intra-african")
async def get_trade_performance_intra_african():
    """Récupérer les données de commerce INTRA-AFRICAIN uniquement (entre pays africains)"""
    
    # Charger les données de commerce global
    global_trade_data = get_all_countries_trade_performance()
    
    # Calculer le commerce intra-africain (environ 15-17% du commerce global pour la plupart des pays)
    # Source: UNCTAD, AfDB, CEA - Rapport sur l'intégration africaine 2024
    intra_african_percentages = {
        'ZAF': 0.19,  # Afrique du Sud: 19% (forte intégration régionale SADC)
        'EGY': 0.12,  # Égypte: 12% (orientée vers Europe/Asie)
        'NGA': 0.11,  # Nigeria: 11% (orientée vers Europe/Asie pour pétrole)
        'DZA': 0.04,  # Algérie: 4% (très faible, orientée Europe pour gaz)
        'MAR': 0.09,  # Maroc: 9% (orienté Europe)
        'KEN': 0.34,  # Kenya: 34% (hub régional EAC, très intégré)
        'ETH': 0.28,  # Éthiopie: 28% (forte intégration EAC)
        'TZA': 0.32,  # Tanzanie: 32% (forte intégration EAC)
        'UGA': 0.38,  # Ouganda: 38% (très intégré EAC)
        'GHA': 0.42,  # Ghana: 42% (très intégré CEDEAO)
        'CIV': 0.38,  # Côte d'Ivoire: 38% (hub CEDEAO)
        'SEN': 0.31,  # Sénégal: 31% (intégré CEDEAO)
        'CMR': 0.29,  # Cameroun: 29% (intégré CEMAC)
        'AGO': 0.06,  # Angola: 6% (pétrole vers Asie/Europe)
        'TUN': 0.08,  # Tunisie: 8% (orientée Europe)
        'ZWE': 0.48,  # Zimbabwe: 48% (très intégré SADC)
        'ZMB': 0.52,  # Zambie: 52% (très intégré SADC)
        'BWA': 0.65,  # Botswana: 65% (très intégré SADC)
        'MWI': 0.58,  # Malawi: 58% (intégré SADC)
        'NAM': 0.55,  # Namibie: 55% (intégré SADC)
        'RWA': 0.41,  # Rwanda: 41% (intégré EAC)
        'BDI': 0.44,  # Burundi: 44% (intégré EAC)
        'TCD': 0.35,  # Tchad: 35% (intégré CEMAC)
        'NER': 0.33,  # Niger: 33% (intégré CEDEAO)
        'MLI': 0.36,  # Mali: 36% (intégré CEDEAO)
        'BFA': 0.40,  # Burkina Faso: 40% (intégré CEDEAO)
        'MDG': 0.18,  # Madagascar: 18% (insulaire, moins intégré)
        'BEN': 0.35,  # Bénin: 35% (intégré CEDEAO)
        'TGO': 0.37,  # Togo: 37% (intégré CEDEAO)
    }
    
    # Pourcentage par défaut pour les pays non listés
    default_percentage = 0.17  # 17% moyenne africaine
    
    intra_african_data = []
    for country in global_trade_data:
        code = country['code']
        intra_pct = intra_african_percentages.get(code, default_percentage)
        
        intra_african_data.append({
            'country': country['country'],
            'code': country['code'],
            'exports_2024': round(country['exports_2024'] * intra_pct, 2),
            'imports_2024': round(country['imports_2024'] * intra_pct, 2),
            'trade_balance_2024': round(country['trade_balance_2024'] * intra_pct, 2),
            'intra_african_percentage': round(intra_pct * 100, 1),
            'global_exports_2024': country['exports_2024'],
            'global_imports_2024': country['imports_2024']
        })
    
    # Trier par exports intra-africains
    intra_african_data.sort(key=lambda x: x['exports_2024'], reverse=True)
    
    return {
        "countries_intra_african": intra_african_data,
        "data_source": "Calculé à partir OEC 2024 + UNCTAD/AfDB/CEA pourcentages intra-africains",
        "last_updated": "2024-09-16",
        "year": 2024,
        "trade_type": "intra_african",
        "description": "Commerce uniquement entre pays africains (excluant Europe, Asie, Amériques)",
        "average_intra_african_percentage": 17,
        "note": "Les pourcentages intra-africains varient selon l'intégration régionale (SADC, EAC, CEDEAO, etc.)"
    }

# ==========================================
# LOGISTICS MARITIME ENDPOINTS
# ==========================================

@api_router.get("/logistics/ports")
async def get_ports(country_iso: Optional[str] = None):
    """
    Get all maritime ports or filter by country ISO code
    Query params:
    - country_iso: Filter ports by country (e.g., MAR, NGA, ZAF)
    """
    try:
        ports = get_all_ports(country_iso=country_iso)
        return {
            "count": len(ports),
            "ports": ports
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading ports data: {str(e)}")

@api_router.get("/logistics/ports/{port_id}")
async def get_port_details(port_id: str):
    """
    Get detailed information for a specific port
    """
    port = get_port_by_id(port_id)
    
    if not port:
        raise HTTPException(status_code=404, detail=f"Port {port_id} not found")
    
    return port

@api_router.get("/logistics/ports/type/{port_type}")
async def get_ports_filtered_by_type(port_type: str):
    """
    Get ports filtered by type
    Port types: Hub Transhipment, Hub Regional, Maritime Commercial
    """
    valid_types = ["Hub Transhipment", "Hub Regional", "Maritime Commercial"]
    
    if port_type not in valid_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid port type. Valid types: {', '.join(valid_types)}"
        )
    
    ports = get_ports_by_type(port_type)
    return {
        "port_type": port_type,
        "count": len(ports),
        "ports": ports
    }

@api_router.get("/logistics/ports/top/teu")
async def get_top_ports_teu(limit: int = 20):
    """
    Get top ports by container throughput (TEU)
    Query params:
    - limit: Number of ports to return (default: 20, max: 50)
    """
    if limit > 50:
        limit = 50
    
    ports = get_top_ports_by_teu(limit=limit)
    return {
        "count": len(ports),
        "ports": ports
    }

@api_router.get("/logistics/ports/search")
async def search_ports_endpoint(q: str):
    """
    Search ports by name, UN LOCODE, or country name
    Query params:
    - q: Search query string
    """
    if len(q) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    results = search_ports(q)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

@api_router.get("/logistics/statistics")
async def get_logistics_statistics():
    """
    Get global logistics statistics for African ports
    """
    all_ports = get_all_ports()
    
    total_teu = sum(
        p.get('latest_stats', {}).get('container_throughput_teu', 0) 
        for p in all_ports
    )
    
    total_cargo = sum(
        p.get('latest_stats', {}).get('cargo_throughput_tons', 0) 
        for p in all_ports
    )
    
    # Count ports by type
    port_types = {}
    for port in all_ports:
        ptype = port.get('port_type', 'Unknown')
        port_types[ptype] = port_types.get(ptype, 0) + 1
    
    # Count ports by country
    ports_by_country = {}
    for port in all_ports:
        country = port.get('country_name', 'Unknown')
        ports_by_country[country] = ports_by_country.get(country, 0) + 1
    
    return {
        "total_ports": len(all_ports),
        "total_container_throughput_teu": total_teu,
        "total_cargo_throughput_tons": total_cargo,
        "ports_by_type": port_types,
        "ports_by_country": dict(sorted(ports_by_country.items(), key=lambda x: x[1], reverse=True)),
        "year": 2024
    }



# ==========================================
# LOGISTICS AIR CARGO ENDPOINTS
# ==========================================

@api_router.get("/logistics/air/airports")
async def get_airports(country_iso: Optional[str] = None):
    """
    Get all airports or filter by country ISO code
    Query params:
    - country_iso: Filter airports by country (e.g., ZAF, ETH, KEN)
    """
    try:
        airports = get_all_airports(country_iso=country_iso)
        return {
            "count": len(airports),
            "airports": airports
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading airports data: {str(e)}")

# ==========================================
# FREE ZONES ENDPOINTS
# ==========================================

@api_router.get("/logistics/free-zones")
async def get_free_zones(country_iso: Optional[str] = None):
    """
    Get African Free Trade Zones (Zones Franches)
    Query params:
    - country_iso: Filter by country (e.g., MAR, DZA, EGY)
    """
    try:
        zones = get_free_zones_by_country(country_iso)
        return {
            "count": len(zones),
            "zones": zones
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading free zones data: {str(e)}")


@api_router.get("/logistics/air/airports/{airport_id}")
async def get_airport_details(airport_id: str):
    """
    Get detailed information for a specific airport
    """
    airport = get_airport_by_id(airport_id)
    
    if not airport:
        raise HTTPException(status_code=404, detail=f"Airport {airport_id} not found")
    
    return airport

@api_router.get("/logistics/air/airports/top/cargo")
async def get_top_airports_cargo(limit: int = 20):
    """
    Get top airports by cargo throughput (tons)
    Query params:
    - limit: Number of airports to return (default: 20, max: 50)
    """
    if limit > 50:
        limit = 50
    
    airports = get_top_airports_by_cargo(limit=limit)
    return {
        "count": len(airports),
        "airports": airports
    }

@api_router.get("/logistics/air/airports/search")
async def search_airports_endpoint(q: str):
    """
    Search airports by name, IATA code, or country name
    Query params:
    - q: Search query string
    """
    if len(q) < 2:
        raise HTTPException(status_code=400, detail="Search query must be at least 2 characters")
    
    results = search_airports(q)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

@api_router.get("/logistics/air/statistics")
async def get_air_logistics_statistics():
    """
    Get global air cargo statistics for African airports
    """
    all_airports = get_all_airports()
    
    total_cargo = sum(
        a.get('historical_stats', [{}])[0].get('cargo_throughput_tons', 0) if a.get('historical_stats') else 0
        for a in all_airports
    )
    
    total_mail = sum(
        a.get('historical_stats', [{}])[0].get('mail_throughput_tons', 0) if a.get('historical_stats') else 0
        for a in all_airports
    )
    
    # Count airports by country
    airports_by_country = {}
    for airport in all_airports:
        country = airport.get('country_name', 'Unknown')
        airports_by_country[country] = airports_by_country.get(country, 0) + 1
    
    return {
        "total_airports": len(all_airports),
        "total_cargo_throughput_tons": total_cargo,
        "total_mail_throughput_tons": total_mail,
        "airports_by_country": dict(sorted(airports_by_country.items(), key=lambda x: x[1], reverse=True)),
        "year": 2024
    }


# ==========================================
# ETL PIPELINE ENDPOINTS
# ==========================================

@api_router.post("/etl/run")
async def run_etl_pipeline():
    """
    Exécute le pipeline ETL pour mettre à jour les données portuaires.
    
    Met à jour:
    - Données TRS (Time Release Study) officielles WCO
    - Données LPI (Logistics Performance Index) World Bank 2023
    - Benchmarks globaux UNCTAD
    
    IMPORTANT: Seules les données officielles sont utilisées.
    Les ports sans données officielles sont marqués "NA".
    """
    try:
        import sys
        sys.path.insert(0, str(ROOT_DIR))
        from etl.ports_etl import run_etl
        
        result = run_etl()
        return {
            "status": "success",
            "message": "Pipeline ETL exécuté avec succès",
            "details": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur ETL: {str(e)}")


@api_router.get("/etl/status")
async def get_etl_status():
    """
    Retourne le statut du dernier pipeline ETL.
    """
    try:
        log_file = ROOT_DIR / 'etl' / 'etl_log.json'
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            # Dernière exécution
            last_entries = log_data[-68:] if len(log_data) >= 68 else log_data
            last_timestamp = last_entries[-1]['timestamp'] if last_entries else None
            
            return {
                "last_run": last_timestamp,
                "total_updates": len(log_data),
                "ports_with_trs_data": 4,
                "ports_without_trs_data": 64,
                "data_sources": [
                    "WCO Time Release Studies",
                    "World Bank LPI 2023",
                    "World Bank CPPI 2023-2024",
                    "UNCTAD Review of Maritime Transport 2024",
                    "Kenya Ports Authority (KPA)",
                    "Transnet Port Terminals (South Africa)",
                    "Tanger Med Port Authority",
                    "ANP Maroc"
                ]
            }
        else:
            return {
                "last_run": None,
                "message": "Aucun pipeline ETL exécuté"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


@api_router.get("/etl/trs-coverage")
async def get_trs_coverage():
    """
    Retourne la couverture des données TRS officielles par port.
    """
    try:
        ports = get_all_ports()
        
        with_data = []
        without_data = []
        
        for port in ports:
            trs = port.get('trs_analysis', {})
            dwell = trs.get('container_dwell_time_days')
            
            port_info = {
                "port_id": port.get('port_id'),
                "port_name": port.get('port_name'),
                "country": port.get('country_name'),
                "country_iso": port.get('country_iso')
            }
            
            if dwell and dwell != "NA":
                port_info.update({
                    "dwell_time_days": dwell,
                    "source": trs.get('source'),
                    "data_year": trs.get('data_year'),
                    "methodology": trs.get('methodology')
                })
                with_data.append(port_info)
            else:
                port_info["notes"] = trs.get('notes', 'NA')
                without_data.append(port_info)
        
        return {
            "total_ports": len(ports),
            "ports_with_official_trs": len(with_data),
            "ports_without_trs": len(without_data),
            "coverage_percentage": round(len(with_data) / len(ports) * 100, 1),
            "ports_with_data": with_data,
            "ports_without_data": without_data,
            "note": "Seules les données TRS officielles (WCO, autorités portuaires) sont incluses. Aucune estimation."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur: {str(e)}")


# ==========================================
# LAND LOGISTICS ENDPOINTS (TERRESTRIAL)
# ==========================================

from logistics_land_data import (
    get_all_corridors,
    get_corridor_by_id,
    get_corridors_by_country,
    get_all_nodes,
    get_nodes_by_type,
    get_osbp_nodes,
    get_all_operators,
    get_operators_by_type,
    get_corridors_statistics,
    search_corridors
)
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

@api_router.get("/logistics/land/corridors")
async def get_land_corridors(
    corridor_type: str = None,
    importance: str = None,
    country_iso: str = None
):
    """
    Get all land corridors (road/rail) with optional filters
    
    Query parameters:
    - corridor_type: 'road', 'rail', 'multimodal'
    - importance: 'high', 'medium'
    - country_iso: ISO3 country code (e.g., 'CIV')
    """
    if country_iso:
        corridors = get_corridors_by_country(country_iso)
    else:
        corridors = get_all_corridors(corridor_type=corridor_type, importance=importance)
    
    return {
        "count": len(corridors),
        "corridors": corridors
    }

@api_router.get("/logistics/land/corridors/{corridor_id}")
async def get_land_corridor_details(corridor_id: str):
    """Get detailed information for a specific land corridor"""
    corridor = get_corridor_by_id(corridor_id)
    if not corridor:
        raise HTTPException(status_code=404, detail=f"Corridor {corridor_id} not found")
    return corridor

@api_router.get("/logistics/land/nodes")
async def get_land_nodes(node_type: str = None, osbp_only: bool = False):
    """
    Get all logistical nodes (border crossings, dry ports, terminals)
    
    Query parameters:
    - node_type: 'border_crossing', 'dry_port', 'rail_terminal', 'intermodal_hub'
    - osbp_only: true to get only One-Stop Border Posts
    """
    if osbp_only:
        nodes = get_osbp_nodes()
    elif node_type:
        nodes = get_nodes_by_type(node_type)
    else:
        nodes = get_all_nodes()
    
    return {
        "count": len(nodes),
        "nodes": nodes
    }

@api_router.get("/logistics/land/operators")
async def get_land_operators(operator_type: str = None):
    """
    Get all land transport operators
    
    Query parameters:
    - operator_type: 'rail_operator', 'trucking_company'
    """
    if operator_type:
        operators = get_operators_by_type(operator_type)
    else:
        operators = get_all_operators()
    
    return {
        "count": len(operators),
        "operators": operators
    }

@api_router.get("/logistics/land/search")
async def search_land_corridors(q: str):
    """Search corridors by name, country, or description"""
    if not q or len(q) < 2:
        raise HTTPException(status_code=400, detail="Query must be at least 2 characters")
    
    results = search_corridors(q)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

@api_router.get("/logistics/land/statistics")
async def get_land_logistics_statistics():
    """Get global statistics about African land corridors"""
    return get_corridors_statistics()


# ==========================================
# PRODUCTION DATA ENDPOINTS
# ==========================================

@api_router.get("/production/statistics")
async def get_production_stats():
    """
    Get global production statistics for all African countries
    Returns overview of data coverage across 4 dimensions
    """
    return get_production_statistics()

@api_router.get("/production/macro")
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

@api_router.get("/production/macro/{country_iso3}")
async def get_macro_by_country(country_iso3: str):
    """
    Get all macro value added series for a specific country
    Organized by sector with time series
    """
    return get_value_added_by_country(country_iso3)

@api_router.get("/production/agriculture")
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

@api_router.get("/production/agriculture/{country_iso3}")
async def get_agri_by_country(country_iso3: str):
    """
    Get all agricultural production for a specific country
    Organized by commodity with time series
    """
    return get_agriculture_by_country(country_iso3)

@api_router.get("/production/manufacturing")
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

@api_router.get("/production/manufacturing/{country_iso3}")
async def get_manuf_by_country(country_iso3: str):
    """
    Get all manufacturing production for a specific country
    Organized by ISIC sector with time series
    """
    return get_manufacturing_by_country(country_iso3)

@api_router.get("/production/mining")
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

@api_router.get("/production/mining/{country_iso3}")
async def get_mining_by_country(country_iso3: str):
    """
    Get all mining production for a specific country
    Organized by commodity with time series
    """
    return get_mining_by_country_data(country_iso3)

@api_router.get("/production/overview/{country_iso3}")
async def get_country_production_full_overview(country_iso3: str):
    """
    Get complete production overview for a country
    Includes all 4 dimensions: macro, agriculture, manufacturing, mining
    """
    return get_country_production_overview(country_iso3)


# ==========================================

# ==========================================
# HS CODES (HARMONIZED SYSTEM) ENDPOINTS
# ==========================================

@api_router.get("/hs-codes/chapters")
async def get_all_hs_chapters():
    """
    Get all HS chapters (2-digit codes) with labels in FR and EN
    """
    return {
        "chapters": get_hs_chapters(),
        "total": len(get_hs_chapters()),
        "source": "World Customs Organization (WCO) HS 2022"
    }

@api_router.get("/hs-codes/all")
async def get_all_hs6_codes_endpoint(language: str = Query("fr", description="Language: fr or en")):
    """
    Get all HS6 codes with their labels from the complete database (5800+ codes)
    """
    result = []
    chapters = get_hs_chapters()
    for code, data in HS6_DATABASE.items():
        desc_key = "description_fr" if language == "fr" else "description_en"
        result.append({
            "code": code,
            "label": data.get(desc_key, data.get("description_fr", "")),
            "chapter": code[:2],
            "chapter_name": chapters.get(code[:2], {}).get(language, "")
        })
    
    return {
        "codes": result,
        "total": len(result),
        "language": language,
        "source": "World Customs Organization (WCO) HS 2022 + AfCFTA Database"
    }

@api_router.get("/hs-codes/code/{hs_code}")
async def get_single_hs_code(hs_code: str, language: str = Query("fr", description="Language: fr or en")):
    """
    Get a specific HS6 code with its label from complete database
    """
    # Try complete database first
    if hs_code in HS6_DATABASE:
        data = HS6_DATABASE[hs_code]
        desc_key = "description_fr" if language == "fr" else "description_en"
        chapters = get_hs_chapters()
        return {
            "code": hs_code,
            "label": data.get(desc_key, data.get("description_fr", "")),
            "chapter": hs_code[:2],
            "chapter_name": chapters.get(hs_code[:2], {}).get(language, ""),
            "category": data.get("category", ""),
            "sensitivity": data.get("sensitivity", "normal")
        }
    
    # Fallback to old database for backwards compatibility
    result = get_hs6_code(hs_code, language)
    if not result:
        raise HTTPException(status_code=404, detail=f"HS code {hs_code} not found")
    return result

@api_router.get("/hs-codes/search")
async def search_hs_codes_endpoint(
    q: str = Query(..., min_length=2, description="Search query (code or label)"),
    language: str = Query("fr", description="Language: fr or en"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results")
):
    """
    Search HS codes by code or label keyword using complete database (5800+ codes)
    """
    # Use search_hs6_codes from hs6_database.py which has accent-insensitive search
    results = search_hs6_codes(q, language, limit)
    return {
        "query": q,
        "results": results,
        "count": len(results),
        "language": language
    }

@api_router.get("/hs-codes/chapter/{chapter}")
async def get_hs_codes_by_chapter(
    chapter: str,
    language: str = Query("fr", description="Language: fr or en")
):
    """
    Get all HS6 codes for a specific chapter (2-digit code) from complete database
    """
    chapters = get_hs_chapters()
    if len(chapter) != 2 or chapter not in chapters:
        raise HTTPException(status_code=404, detail=f"Chapter {chapter} not found")
    
    # Get codes from complete database
    codes = []
    desc_key = "description_fr" if language == "fr" else "description_en"
    for code, data in HS6_DATABASE.items():
        if code[:2] == chapter:
            codes.append({
                "code": code,
                "label": data.get(desc_key, data.get("description_fr", "")),
                "chapter": chapter,
                "category": data.get("category", ""),
                "sensitivity": data.get("sensitivity", "normal")
            })
    
    # Sort codes
    codes.sort(key=lambda x: x["code"])
    
    chapter_info = chapters.get(chapter, {})
    
    return {
        "chapter": chapter,
        "chapter_name_fr": chapter_info.get('fr', ''),
        "chapter_name_en": chapter_info.get('en', ''),
        "codes": codes,
        "count": len(codes)
    }

@api_router.get("/hs-codes/statistics")
async def get_hs_codes_statistics():
    """
    Get HS codes database statistics from complete database (5800+ codes)
    """
    chapters = get_hs_chapters()
    db_stats = get_database_stats()
    
    # Count codes per chapter from complete database
    codes_per_chapter = {}
    for code in HS6_DATABASE.keys():
        ch = code[:2]
        codes_per_chapter[ch] = codes_per_chapter.get(ch, 0) + 1
    
    top_chapters = sorted(codes_per_chapter.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "total_chapters": len(chapters),
        "total_codes": db_stats.get("total_codes", len(HS6_DATABASE)),
        "top_chapters": [
            {
                "chapter": ch,
                "chapter_name_fr": chapters.get(ch, {}).get('fr', ''),
                "code_count": count
            }
            for ch, count in top_chapters
        ],
        "source": "World Customs Organization (WCO) HS 2022 + AfCFTA Database",
        "last_updated": "2025-01"
    }


# =============================================================================
# SH6 TARIFFS ENDPOINTS - Tarifs précis par code SH6
# =============================================================================

@api_router.get("/hs6-tariffs/search")
async def search_hs6_tariffs_endpoint(
    q: str = Query(..., description="Search query"),
    language: str = Query("fr", description="Language: fr or en"),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Rechercher des codes SH6 avec leurs tarifs par mot-clé
    Retourne les taux NPF et ZLECAf avec les économies potentielles
    """
    results = search_hs6_tariffs(q, language, limit)
    return {
        "query": q,
        "count": len(results),
        "results": results
    }


@api_router.get("/hs6-tariffs/code/{hs6_code}")
async def get_hs6_tariff_endpoint(hs6_code: str, language: str = Query("fr")):
    """
    Obtenir les tarifs détaillés pour un code SH6 spécifique
    Inclut taux NPF, taux ZLECAf, et économies potentielles
    """
    tariff = get_hs6_tariff(hs6_code)
    if not tariff:
        # Fallback vers les informations du code sans tarif spécifique
        hs_info = get_hs6_code(hs6_code, language)
        if hs_info:
            return {
                "code": hs6_code,
                "has_specific_tariff": False,
                "hs_info": hs_info,
                "message": "Pas de tarif SH6 spécifique - utiliser le taux par chapitre"
            }
        raise HTTPException(status_code=404, detail=f"Code SH6 {hs6_code} non trouvé")
    
    desc_key = f"description_{language}"
    return {
        "code": hs6_code,
        "has_specific_tariff": True,
        "description": tariff.get(desc_key, tariff.get("description_fr")),
        "normal_rate": tariff["normal"],
        "normal_rate_pct": f"{tariff['normal'] * 100:.1f}%",
        "zlecaf_rate": tariff["zlecaf"],
        "zlecaf_rate_pct": f"{tariff['zlecaf'] * 100:.1f}%",
        "savings_pct": round((tariff["normal"] - tariff["zlecaf"]) / tariff["normal"] * 100, 1) if tariff["normal"] > 0 else 0,
        "chapter": hs6_code[:2],
        "chapter_name": get_hs_chapters().get(hs6_code[:2], {}).get(language, "")
    }


@api_router.get("/hs6-tariffs/chapter/{chapter}")
async def get_hs6_tariffs_chapter_endpoint(
    chapter: str,
    language: str = Query("fr")
):
    """
    Obtenir tous les codes SH6 avec tarifs spécifiques pour un chapitre
    """
    results = get_hs6_tariffs_by_chapter(chapter)
    chapter_info = get_hs_chapters().get(chapter.zfill(2), {})
    
    return {
        "chapter": chapter.zfill(2),
        "chapter_name": chapter_info.get(language, chapter_info.get("fr", "")),
        "count": len(results),
        "codes": results
    }


@api_router.get("/hs6-tariffs/statistics")
async def get_hs6_tariffs_statistics_endpoint():
    """
    Obtenir les statistiques sur les tarifs SH6 disponibles
    """
    return get_hs6_statistics()


@api_router.get("/hs6-tariffs/products/african-exports")
async def get_african_export_products(language: str = Query("fr")):
    """
    Obtenir la liste des produits africains clés avec leurs tarifs SH6
    Groupés par catégorie (agriculture, mining, manufactured)
    """
    from etl.hs6_tariffs import HS6_TARIFFS_AGRICULTURE, HS6_TARIFFS_MINING, HS6_TARIFFS_MANUFACTURED
    
    desc_key = f"description_{language}"
    
    def format_products(products_dict, category_name):
        return [
            {
                "code": code,
                "description": data.get(desc_key, data.get("description_fr")),
                "normal_rate_pct": f"{data['normal'] * 100:.1f}%",
                "zlecaf_rate_pct": f"{data['zlecaf'] * 100:.1f}%",
                "savings_pct": round((data["normal"] - data["zlecaf"]) / data["normal"] * 100, 1) if data["normal"] > 0 else 0
            }
            for code, data in sorted(products_dict.items())
        ]
    
    return {
        "agriculture": {
            "name_fr": "Produits Agricoles",
            "name_en": "Agricultural Products",
            "count": len(HS6_TARIFFS_AGRICULTURE),
            "products": format_products(HS6_TARIFFS_AGRICULTURE, "agriculture")
        },
        "mining": {
            "name_fr": "Produits Miniers et Énergétiques",
            "name_en": "Mining and Energy Products",
            "count": len(HS6_TARIFFS_MINING),
            "products": format_products(HS6_TARIFFS_MINING, "mining")
        },
        "manufactured": {
            "name_fr": "Produits Manufacturés",
            "name_en": "Manufactured Products",
            "count": len(HS6_TARIFFS_MANUFACTURED),
            "products": format_products(HS6_TARIFFS_MANUFACTURED, "manufactured")
        },
        "total_products": len(HS6_TARIFFS_AGRICULTURE) + len(HS6_TARIFFS_MINING) + len(HS6_TARIFFS_MANUFACTURED)
    }


# =============================================================================
# COUNTRY TARIFFS ENDPOINTS - Taux par pays
# =============================================================================

@api_router.get("/country-tariffs/{country_code}")
async def get_country_tariffs_endpoint(
    country_code: str,
    hs_code: str = Query("18", description="HS code (2-6 digits)")
):
    """
    Obtenir les tarifs douaniers spécifiques à un pays
    Retourne les taux NPF, ZLECAf, TVA et autres taxes
    """
    # Normaliser le code pays
    from etl.country_tariffs_complete import ISO2_TO_ISO3
    if len(country_code) == 2:
        country_iso3 = ISO2_TO_ISO3.get(country_code.upper(), country_code.upper())
    else:
        country_iso3 = country_code.upper()
    
    # Obtenir les taux
    npf_rate, npf_source = get_tariff_rate_for_country(country_iso3, hs_code)
    zlecaf_rate, zlecaf_source = get_zlecaf_tariff_rate(country_iso3, hs_code)
    vat_rate, vat_source = get_vat_rate_for_country(country_iso3)
    other_rate, other_detail = get_other_taxes_for_country(country_iso3)
    
    # Trouver le pays
    country = next((c for c in AFRICAN_COUNTRIES if c['iso3'] == country_iso3), None)
    country_name = country['name'] if country else country_iso3
    
    return {
        "country_code": country_iso3,
        "country_name": country_name,
        "hs_code": hs_code,
        "chapter": hs_code[:2],
        "tariffs": {
            "npf_rate": npf_rate,
            "npf_rate_pct": f"{npf_rate * 100:.1f}%",
            "zlecaf_rate": zlecaf_rate,
            "zlecaf_rate_pct": f"{zlecaf_rate * 100:.1f}%",
            "potential_savings_pct": round((npf_rate - zlecaf_rate) / npf_rate * 100, 1) if npf_rate > 0 else 0
        },
        "taxes": {
            "vat_rate": vat_rate,
            "vat_rate_pct": f"{vat_rate * 100:.1f}%",
            "other_taxes_rate": other_rate,
            "other_taxes_pct": f"{other_rate * 100:.1f}%",
            "other_taxes_detail": other_detail
        },
        "sources": {
            "tariff": npf_source,
            "zlecaf": zlecaf_source,
            "vat": vat_source
        },
        "last_updated": "2025-01"
    }


@api_router.get("/country-tariffs-comparison")
async def compare_country_tariffs(
    countries: str = Query("NGA,GHA,KEN,ZAF,EGY", description="Comma-separated country codes"),
    hs_code: str = Query("18", description="HS code")
):
    """
    Comparer les tarifs entre plusieurs pays africains
    """
    country_list = [c.strip().upper() for c in countries.split(",")]
    
    results = []
    for cc in country_list:
        from etl.country_tariffs_complete import ISO2_TO_ISO3
        if len(cc) == 2:
            iso3 = ISO2_TO_ISO3.get(cc, cc)
        else:
            iso3 = cc
        
        npf_rate, _ = get_tariff_rate_for_country(iso3, hs_code)
        zlecaf_rate, _ = get_zlecaf_tariff_rate(iso3, hs_code)
        vat_rate, _ = get_vat_rate_for_country(iso3)
        other_rate, _ = get_other_taxes_for_country(iso3)
        
        country = next((c for c in AFRICAN_COUNTRIES if c['iso3'] == iso3), None)
        
        results.append({
            "country_code": iso3,
            "country_name": country['name'] if country else iso3,
            "npf_rate_pct": f"{npf_rate * 100:.1f}%",
            "zlecaf_rate_pct": f"{zlecaf_rate * 100:.1f}%",
            "vat_rate_pct": f"{vat_rate * 100:.1f}%",
            "other_taxes_pct": f"{other_rate * 100:.1f}%",
            "total_cost_factor_npf": round(1 + npf_rate + vat_rate * (1 + npf_rate) + other_rate, 3),
            "total_cost_factor_zlecaf": round(1 + zlecaf_rate + vat_rate * (1 + zlecaf_rate) + other_rate, 3)
        })
    
    # Trier par coût total NPF
    results.sort(key=lambda x: x['total_cost_factor_npf'])
    
    return {
        "hs_code": hs_code,
        "chapter": hs_code[:2],
        "countries_compared": len(results),
        "comparison": results,
        "note": "total_cost_factor = multiplicateur du coût d'importation (1.0 = pas de taxes)"
    }


@api_router.get("/all-country-rates")
async def get_all_rates_endpoint():
    """
    Obtenir un aperçu de tous les taux par pays africain
    Pour validation et vérification des données
    """
    return get_all_country_rates()


# =============================================================================
# SH6 TARIFFS BY COUNTRY ENDPOINTS
# =============================================================================

@api_router.get("/country-hs6-tariffs/{country_code}/search")
async def search_country_hs6_endpoint(
    country_code: str,
    q: str = Query(..., description="Search query"),
    language: str = Query("fr", description="Language: fr or en"),
    limit: int = Query(20, ge=1, le=100)
):
    """
    Rechercher des codes SH6 avec tarifs réels dans un pays spécifique
    """
    results = search_country_hs6_tariffs(country_code, q, language, limit)
    
    return {
        "country_code": country_code.upper(),
        "query": q,
        "count": len(results),
        "results": results
    }


@api_router.get("/country-hs6-tariffs/{country_code}/{hs6_code}")
async def get_country_hs6_tariff_endpoint(
    country_code: str,
    hs6_code: str,
    language: str = Query("fr")
):
    """
    Obtenir le tarif SH6 réel pour un pays et un code spécifique
    """
    tariff = get_country_hs6_tariff(country_code, hs6_code)
    
    if not tariff:
        # Fallback vers le taux par chapitre
        from etl.country_tariffs_complete import get_tariff_rate_for_country
        chapter_rate, source = get_tariff_rate_for_country(country_code, hs6_code)
        return {
            "country_code": country_code.upper(),
            "hs6_code": hs6_code,
            "has_hs6_specific_rate": False,
            "dd_rate": chapter_rate,
            "dd_rate_pct": f"{chapter_rate * 100:.1f}%",
            "source": source,
            "note": "Taux par chapitre utilisé (pas de tarif SH6 spécifique disponible)"
        }
    
    desc_key = f"description_{language}"
    return {
        "country_code": country_code.upper(),
        "hs6_code": hs6_code,
        "has_hs6_specific_rate": True,
        "dd_rate": tariff["dd"],
        "dd_rate_pct": f"{tariff['dd'] * 100:.1f}%",
        "description": tariff.get(desc_key, tariff.get("description_fr", "")),
        "source": f"Tarif SH6 officiel {country_code.upper()}"
    }


@api_router.get("/country-hs6-tariffs/available")
async def get_available_hs6_tariffs():
    """
    Obtenir la liste des pays avec tarifs SH6 détaillés disponibles
    """
    available = get_available_country_tariffs()
    return {
        "countries_with_hs6_tariffs": len(available),
        "countries": available,
        "note": "Pour les pays non listés, les taux par chapitre sont utilisés"
    }


@api_router.get("/country-hs6-tariffs/{country_code}/all")
async def get_all_country_hs6_tariffs(country_code: str, language: str = Query("fr")):
    """
    Obtenir tous les tarifs SH6 disponibles pour un pays
    """
    from etl.country_hs6_tariffs import COUNTRY_HS6_TARIFFS, ISO2_TO_ISO3
    
    # Normaliser le code pays
    if len(country_code) == 2:
        iso3 = ISO2_TO_ISO3.get(country_code.upper(), country_code.upper())
    else:
        iso3 = country_code.upper()
    
    tariffs = COUNTRY_HS6_TARIFFS.get(iso3, {})
    
    if not tariffs:
        return {
            "country_code": iso3,
            "has_hs6_tariffs": False,
            "count": 0,
            "tariffs": [],
            "note": "Pas de tarifs SH6 spécifiques pour ce pays - utiliser taux par chapitre"
        }
    
    desc_key = f"description_{language}"
    formatted_tariffs = [
        {
            "hs6_code": code,
            "dd_rate": data["dd"],
            "dd_rate_pct": f"{data['dd'] * 100:.1f}%",
            "description": data.get(desc_key, data.get("description_fr", ""))
        }
        for code, data in sorted(tariffs.items())
    ]
    
    return {
        "country_code": iso3,
        "has_hs6_tariffs": True,
        "count": len(formatted_tariffs),
        "tariffs": formatted_tariffs
    }


# =============================================================================
# SOUS-POSITIONS NATIONALES ENDPOINTS (8-12 chiffres)
# =============================================================================

@api_router.get("/tariffs/detailed/{country_code}/{hs_code}")
async def get_detailed_tariff_endpoint(
    country_code: str, 
    hs_code: str, 
    language: str = Query("fr")
):
    """
    Obtenir le tarif détaillé avec toutes les sous-positions pour un pays et code HS
    
    Args:
        country_code: Code ISO3 du pays (ex: NGA, CIV, ZAF)
        hs_code: Code HS (6-12 chiffres)
        language: Langue (fr ou en)
    
    Returns:
        Informations détaillées incluant taux par défaut et sous-positions
    """
    summary = get_tariff_summary(country_code.upper(), hs_code)
    
    if not summary.get("has_detailed_tariffs"):
        raise HTTPException(
            status_code=404, 
            detail=f"Pas de tarifs détaillés pour {country_code.upper()} / {hs_code}. Utiliser l'endpoint /country-hs6-tariffs/{country_code}/{hs_code[:6]}"
        )
    
    # Adapter les descriptions selon la langue
    desc_key = f"description_{language}"
    if language == "en":
        summary["description"] = summary.get("description_en", summary.get("description_fr", ""))
    else:
        summary["description"] = summary.get("description_fr", "")
    
    # Formater les sous-positions avec la bonne langue
    for sp in summary.get("sub_positions", []):
        sp["description"] = sp.get(desc_key, sp.get("description_fr", ""))
    
    return summary


@api_router.get("/tariffs/sub-position/{country_code}/{full_code}")
async def get_sub_position_tariff_endpoint(
    country_code: str, 
    full_code: str,
    language: str = Query("fr")
):
    """
    Obtenir le taux de droits de douane pour une sous-position nationale spécifique
    
    Args:
        country_code: Code ISO3 du pays
        full_code: Code national complet (8-12 chiffres, ex: 8703231000)
    
    Returns:
        Taux DD spécifique à cette sous-position ou taux par défaut
    """
    rate, description, source = get_sub_position_rate(country_code.upper(), full_code)
    
    hs6 = full_code[:6].zfill(6)
    detailed = get_detailed_tariff(country_code.upper(), hs6)
    
    if rate is None:
        # Pas de tarif détaillé, fallback vers tarif SH6 standard
        hs6_tariff = get_country_hs6_tariff(country_code.upper(), hs6)
        if hs6_tariff:
            rate = hs6_tariff["dd"]
            description = hs6_tariff.get(f"description_{language}", hs6_tariff.get("description_fr", ""))
            source = f"Tarif SH6 standard (pas de sous-position)"
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Aucun tarif trouvé pour {country_code.upper()} / {full_code}"
            )
    
    return {
        "country_code": country_code.upper(),
        "full_code": full_code,
        "hs6_code": hs6,
        "dd_rate": rate,
        "dd_rate_pct": f"{rate * 100:.1f}%",
        "description": description,
        "source": source,
        "has_sub_position_match": source.startswith("Sous-position")
    }


@api_router.get("/tariffs/sub-positions/{country_code}/{hs6_code}")
async def get_all_sub_positions_endpoint(
    country_code: str, 
    hs6_code: str,
    language: str = Query("fr")
):
    """
    Obtenir toutes les sous-positions nationales pour un code HS6 dans un pays
    
    Returns:
        Liste des sous-positions avec leurs taux respectifs
    """
    hs6 = hs6_code[:6].zfill(6)
    sub_positions = get_all_sub_positions(country_code.upper(), hs6)
    
    # Obtenir les infos générales du HS6
    detailed = get_detailed_tariff(country_code.upper(), hs6)
    
    if not sub_positions:
        return {
            "country_code": country_code.upper(),
            "hs6_code": hs6,
            "has_sub_positions": False,
            "count": 0,
            "sub_positions": [],
            "note": "Pas de sous-positions détaillées pour ce code dans ce pays"
        }
    
    # Adapter les descriptions selon la langue
    desc_key = f"description_{language}"
    for sp in sub_positions:
        sp["description"] = sp.get(desc_key, sp.get("description_fr", ""))
    
    has_variations, min_rate, max_rate = has_varying_rates(country_code.upper(), hs6)
    
    return {
        "country_code": country_code.upper(),
        "hs6_code": hs6,
        "hs6_description": detailed.get(f"description_{language}", detailed.get("description_fr", "")) if detailed else "",
        "default_dd_rate": detailed.get("default_dd", 0) if detailed else 0,
        "default_dd_rate_pct": f"{detailed.get('default_dd', 0) * 100:.1f}%" if detailed else "N/A",
        "has_sub_positions": True,
        "has_varying_rates": has_variations,
        "rate_range": {
            "min_pct": f"{min_rate * 100:.1f}%",
            "max_pct": f"{max_rate * 100:.1f}%"
        } if has_variations else None,
        "count": len(sub_positions),
        "sub_positions": sub_positions
    }


@api_router.get("/tariffs/detailed-countries")
async def get_detailed_tariff_countries():
    """
    Obtenir la liste des pays avec tarifs détaillés (sous-positions nationales)
    """
    countries_data = {}
    for iso3, tariffs in COUNTRY_HS6_DETAILED.items():
        total_sub_positions = sum(
            len(hs6_data.get("sub_positions", {}))
            for hs6_data in tariffs.values()
        )
        countries_data[iso3] = {
            "hs6_codes_count": len(tariffs),
            "sub_positions_count": total_sub_positions,
            "hs6_codes": list(tariffs.keys())
        }
    
    return {
        "countries_with_detailed_tariffs": len(countries_data),
        "countries": countries_data,
        "note": "Ces pays ont des tarifs avec sous-positions nationales (8-12 chiffres)"
    }


# =============================================================================
# RECHERCHE INTELLIGENTE HS6 + SOUS-POSITIONS
# =============================================================================

@api_router.get("/hs6/search")
async def search_hs6(
    query: str = Query(..., min_length=2, description="Terme de recherche (code ou description)"),
    language: str = Query("fr"),
    limit: int = Query(20, le=50)
):
    """
    Recherche intelligente dans la base HS6
    - Par code (ex: "8703", "870323")
    - Par mot-clé (ex: "voiture", "café", "riz")
    - Par catégorie (ex: "vehicles", "coffee")
    """
    results = search_hs6_codes(query, language, limit)
    return {
        "query": query,
        "count": len(results),
        "results": results
    }


@api_router.get("/hs6/info/{hs_code}")
async def get_hs6_information(
    hs_code: str,
    language: str = Query("fr")
):
    """
    Obtenir les informations complètes d'un code HS6:
    - Description
    - Catégorie
    - Sensibilité ZLECAf
    - Types de sous-positions disponibles
    - Règle d'origine
    """
    info = get_hs6_info(hs_code, language)
    if not info:
        raise HTTPException(
            status_code=404,
            detail=f"Code HS6 {hs_code[:6]} non trouvé dans la base"
        )
    return info


@api_router.get("/hs6/suggestions/{hs_code}")
async def get_hs6_sub_position_suggestions(
    hs_code: str,
    country_code: str = Query(None, description="Code ISO3 du pays pour obtenir les sous-positions nationales"),
    language: str = Query("fr")
):
    """
    Obtenir les suggestions intelligentes de sous-positions pour un code HS6
    
    Retourne:
    - Types de distinctions possibles (neuf/occasion, âge, qualité, etc.)
    - Options avec suffixes de code
    - Si country_code fourni: sous-positions nationales réelles du pays
    """
    hs6 = hs_code[:6].zfill(6)
    
    # Suggestions génériques basées sur la base HS6
    generic_suggestions = get_sub_position_suggestions(hs6, language)
    
    # Si un pays est spécifié, obtenir les sous-positions nationales réelles
    country_sub_positions = []
    if country_code:
        country_sub_positions = get_all_sub_positions(country_code.upper(), hs6)
    
    # Info de base sur le HS6
    hs6_info = get_hs6_info(hs6, language)
    
    return {
        "hs6_code": hs6,
        "description": hs6_info.get("description") if hs6_info else None,
        "category": hs6_info.get("category") if hs6_info else None,
        "generic_suggestions": generic_suggestions,
        "country_code": country_code.upper() if country_code else None,
        "country_sub_positions": country_sub_positions,
        "has_country_specific_rates": len(country_sub_positions) > 0
    }


@api_router.get("/hs6/rule-of-origin/{hs_code}")
async def get_hs6_rule_of_origin(
    hs_code: str,
    language: str = Query("fr")
):
    """
    Obtenir la règle d'origine ZLECAf pour un code HS6
    """
    hs6 = hs_code[:6].zfill(6)
    rule = get_rule_of_origin(hs6, language)
    
    if not rule:
        # Règle par défaut si non trouvée
        return {
            "hs6_code": hs6,
            "type": "substantial_transformation",
            "requirement": "Transformation substantielle - 40% valeur ajoutée africaine" if language == "fr" else "Substantial transformation - 40% African value added",
            "regional_content": 40,
            "note": "Règle par défaut - vérifier auprès des autorités compétentes"
        }
    
    return rule


@api_router.get("/hs6/categories")
async def get_hs6_categories():
    """
    Obtenir toutes les catégories de produits disponibles
    """
    categories = get_all_categories()
    return {
        "count": len(categories),
        "categories": categories
    }


@api_router.get("/hs6/category/{category}")
async def get_hs6_by_category(
    category: str,
    language: str = Query("fr")
):
    """
    Obtenir tous les codes HS6 d'une catégorie
    """
    codes = get_codes_by_category(category, language)
    if not codes:
        raise HTTPException(
            status_code=404,
            detail=f"Catégorie '{category}' non trouvée"
        )
    return {
        "category": category,
        "count": len(codes),
        "codes": codes
    }


@api_router.get("/hs6/statistics")
async def get_hs6_database_statistics():
    """
    Obtenir les statistiques de la base HS6
    """
    stats = get_database_stats()
    
    # Ajouter les stats des sous-positions nationales
    country_stats = {}
    for iso3, tariffs in COUNTRY_HS6_DETAILED.items():
        total_sub = sum(len(hs6_data.get("sub_positions", {})) for hs6_data in tariffs.values())
        country_stats[iso3] = {
            "hs6_codes": len(tariffs),
            "sub_positions": total_sub
        }
    
    total_country_hs6 = sum(v["hs6_codes"] for v in country_stats.values())
    total_country_sub = sum(v["sub_positions"] for v in country_stats.values())
    
    return {
        "hs6_base": {
            "total_codes": stats["total_codes"],
            "with_sub_positions": stats["with_sub_positions"],
            "categories": stats["categories"],
            "sensitivities": stats["sensitivities"]
        },
        "national_sub_positions": {
            "countries_covered": len(country_stats),
            "total_hs6_with_national_rates": total_country_hs6,
            "total_sub_positions": total_country_sub,
            "by_country": country_stats
        }
    }


@api_router.get("/hs6/smart-search")
async def smart_search_with_suggestions(
    query: str = Query(..., min_length=2),
    country_code: str = Query(None),
    language: str = Query("fr"),
    include_sub_positions: bool = Query(True)
):
    """
    Recherche intelligente avec suggestions de sous-positions
    
    Combine:
    - Recherche HS6 par mot-clé
    - Suggestions de sous-positions
    - Sous-positions nationales si pays spécifié
    - Règles d'origine
    """
    # Rechercher les codes HS6
    hs6_results = search_hs6_codes(query, language, limit=10)
    
    # Enrichir chaque résultat avec les sous-positions
    enriched_results = []
    for result in hs6_results:
        enriched = result.copy()
        
        if include_sub_positions and result["has_sub_positions"]:
            # Suggestions génériques
            enriched["sub_position_suggestions"] = get_sub_position_suggestions(result["code"], language)
            
            # Sous-positions nationales si pays fourni
            if country_code:
                country_subs = get_all_sub_positions(country_code.upper(), result["code"])
                enriched["country_sub_positions"] = country_subs
                enriched["has_varying_rates"] = len(country_subs) > 1
        
        # Règle d'origine
        rule = get_rule_of_origin(result["code"], language)
        if rule:
            enriched["rule_of_origin"] = rule
        
        enriched_results.append(enriched)
    
    return {
        "query": query,
        "country_code": country_code.upper() if country_code else None,
        "count": len(enriched_results),
        "results": enriched_results
    }


# FAOSTAT ENRICHED DATA ENDPOINTS
# ==========================================

from etl import (
    get_faostat_country_data,
    get_africa_top_producers,
    get_all_commodities,
    get_all_faostat_data,
    get_fisheries_rankings,
    get_faostat_statistics,
    get_unido_country_data,
    get_all_unido_data,
    get_isic_sectors,
    get_countries_by_mva,
    get_sector_analysis,
    get_unido_statistics
)

@api_router.get("/production/faostat/statistics")
async def get_faostat_stats():
    """
    Get global FAOSTAT statistics for all African countries
    """
    return get_faostat_statistics()

@api_router.get("/production/faostat/commodities")
async def get_faostat_commodities():
    """
    Get list of all agricultural commodities available in FAOSTAT data
    """
    return {"commodities": get_all_commodities()}

@api_router.get("/production/faostat/top-producers/{commodity}")
async def get_commodity_top_producers(commodity: str):
    """
    Get top African producers for a specific commodity
    """
    producers = get_africa_top_producers(commodity)
    if not producers:
        return {"message": f"No ranking data available for '{commodity}'", "commodity": commodity, "producers": []}
    return {"commodity": commodity, "producers": producers}

@api_router.get("/production/faostat/fisheries")
async def get_fisheries_data():
    """
    Get fisheries and aquaculture rankings for Africa
    """
    return get_fisheries_rankings()

@api_router.get("/production/faostat/{country_iso3}")
async def get_faostat_country(country_iso3: str):
    """
    Get detailed FAOSTAT agricultural data for a specific country
    Includes: main crops, production, evolution, livestock, fisheries, key indicators
    """
    data = get_faostat_country_data(country_iso3.upper())
    if not data:
        return {"message": f"No FAOSTAT data available for country '{country_iso3}'", "country_iso3": country_iso3}
    return data

@api_router.get("/production/faostat")
async def get_all_faostat():
    """
    Get all FAOSTAT data for all African countries
    """
    return get_all_faostat_data()


# ==========================================
# UNIDO ENRICHED DATA ENDPOINTS
# ==========================================

@api_router.get("/production/unido/statistics")
async def get_unido_stats():
    """
    Get global UNIDO industrial statistics for Africa
    """
    return get_unido_statistics()

@api_router.get("/production/unido/isic-sectors")
async def get_unido_isic_sectors():
    """
    Get ISIC Rev.4 sector classification
    """
    return {"sectors": get_isic_sectors()}

@api_router.get("/production/unido/ranking")
async def get_unido_mva_ranking():
    """
    Get countries ranked by Manufacturing Value Added (MVA)
    """
    return {"ranking": get_countries_by_mva()}

@api_router.get("/production/unido/sector-analysis/{isic_code}")
async def get_unido_sector(isic_code: str):
    """
    Get analysis of a specific ISIC sector across all African countries
    """
    analysis = get_sector_analysis(isic_code)
    sectors = get_isic_sectors()
    sector_name = sectors.get(isic_code, "Unknown")
    return {
        "isic_code": isic_code,
        "sector_name": sector_name,
        "countries": analysis
    }

@api_router.get("/production/unido/{country_iso3}")
async def get_unido_country(country_iso3: str):
    """
    Get detailed UNIDO industrial data for a specific country
    Includes: MVA, top sectors, growth rate, key products, industrial zones
    """
    data = get_unido_country_data(country_iso3.upper())
    if not data:
        return {"message": f"No UNIDO data available for country '{country_iso3}'", "country_iso3": country_iso3}
    return data

@api_router.get("/production/unido")
async def get_all_unido():
    """
    Get all UNIDO industrial data for all African countries
    """
    return get_all_unido_data()


# ==========================================
# TRADE PRODUCTS ENDPOINTS (TOP 20)
# ==========================================

from etl.trade_products_data import (
    get_top_imports_from_world,
    get_top_exports_to_world,
    get_top_intra_african_imports,
    get_top_intra_african_exports,
    get_all_trade_products_data,
    get_trade_summary
)
from etl.translations import translate_product, translate_country_list

def translate_products_list(products: list, language: str = 'fr') -> list:
    """Translate product names and country names in a products list"""
    if language == 'fr':
        return products
    
    translated = []
    for product in products:
        translated_product = product.copy()
        translated_product['product'] = translate_product(product['product'], language)
        if 'top_importers' in product:
            translated_product['top_importers'] = translate_country_list(product['top_importers'], language)
        if 'top_exporters' in product:
            translated_product['top_exporters'] = translate_country_list(product['top_exporters'], language)
        if 'main_origins' in product:
            translated_product['main_origins'] = translate_country_list(product['main_origins'], language)
        translated.append(translated_product)
    return translated

@api_router.get("/statistics/trade-products/summary")
async def get_trade_products_summary():
    """
    Get summary of trade products data
    """
    return get_trade_summary()

@api_router.get("/statistics/trade-products/imports-world")
async def get_imports_from_world(lang: str = 'fr'):
    """
    Get Top 20 products imported by Africa from the world
    """
    titles = {
        'fr': "Top 20 Produits Importés par l'Afrique du Monde",
        'en': "Top 20 Products Imported by Africa from the World"
    }
    return {
        "title": titles.get(lang, titles['fr']),
        "source": "UNCTAD/ITC Trade Map 2023",
        "year": 2023,
        "products": translate_products_list(get_top_imports_from_world(), lang)
    }

@api_router.get("/statistics/trade-products/exports-world")
async def get_exports_to_world(lang: str = 'fr'):
    """
    Get Top 20 products exported by Africa to the world
    """
    titles = {
        'fr': "Top 20 Produits Exportés par l'Afrique vers le Monde",
        'en': "Top 20 Products Exported by Africa to the World"
    }
    return {
        "title": titles.get(lang, titles['fr']),
        "source": "UNCTAD/ITC Trade Map 2023",
        "year": 2023,
        "products": translate_products_list(get_top_exports_to_world(), lang)
    }

@api_router.get("/statistics/trade-products/intra-imports")
async def get_intra_imports(lang: str = 'fr'):
    """
    Get Top 20 products imported in intra-African trade
    """
    titles = {
        'fr': "Top 20 Produits Importés en Commerce Intra-Africain",
        'en': "Top 20 Products Imported in Intra-African Trade"
    }
    return {
        "title": titles.get(lang, titles['fr']),
        "source": "UNCTAD/AfCFTA Secretariat 2023",
        "year": 2023,
        "products": translate_products_list(get_top_intra_african_imports(), lang)
    }

@api_router.get("/statistics/trade-products/intra-exports")
async def get_intra_exports(lang: str = 'fr'):
    """
    Get Top 20 products exported in intra-African trade
    """
    titles = {
        'fr': "Top 20 Produits Exportés en Commerce Intra-Africain",
        'en': "Top 20 Products Exported in Intra-African Trade"
    }
    return {
        "title": titles.get(lang, titles['fr']),
        "source": "UNCTAD/AfCFTA Secretariat 2023",
        "year": 2023,
        "products": translate_products_list(get_top_intra_african_exports(), lang)
    }

@api_router.get("/statistics/trade-products")
async def get_all_trade_products():
    """
    Get all trade products data (imports, exports, intra-African)
    """
    return get_all_trade_products_data()


# =============================================================================
# UNCTAD DATA ENDPOINTS
# =============================================================================

from etl.unctad_data import (
    get_unctad_port_statistics,
    get_unctad_trade_flows,
    get_unctad_lsci,
    get_all_unctad_data
)

@api_router.get("/statistics/unctad/ports")
async def get_unctad_ports():
    """
    Get UNCTAD port statistics for African ports
    Source: UNCTAD Review of Maritime Transport 2023
    """
    return get_unctad_port_statistics()

@api_router.get("/statistics/unctad/trade-flows")
async def get_unctad_flows():
    """
    Get UNCTAD trade flow statistics
    Source: UNCTAD COMTRADE 2023
    """
    return get_unctad_trade_flows()

@api_router.get("/statistics/unctad/lsci")
async def get_unctad_liner_connectivity():
    """
    Get UNCTAD Liner Shipping Connectivity Index for Africa
    Source: UNCTAD 2023
    """
    return get_unctad_lsci()

@api_router.get("/statistics/unctad")
async def get_all_unctad():
    """
    Get all UNCTAD data (ports, trade flows, LSCI)
    """
    return get_all_unctad_data()


# =====================================================
# ENDPOINTS ACTUALITÉS ÉCONOMIQUES AFRICAINES
# Sources: Agence Ecofin, AllAfrica
# =====================================================

@api_router.get("/news")
async def get_economic_news(
    force_refresh: bool = Query(False, description="Forcer le rafraîchissement du cache"),
    region: Optional[str] = Query(None, description="Filtrer par région (ex: Afrique du Nord)"),
    category: Optional[str] = Query(None, description="Filtrer par catégorie (ex: Finance, Commerce)")
):
    """
    Récupérer les actualités économiques africaines
    Sources: Agence Ecofin, AllAfrica
    Mise à jour: Une fois par jour (ou force_refresh=true)
    """
    try:
        news_data = await get_news(force_refresh=force_refresh)
        articles = news_data.get("articles", [])
        
        # Filtrer par région si spécifié
        if region:
            articles = [a for a in articles if a.get("region", "").lower() == region.lower()]
        
        # Filtrer par catégorie si spécifié
        if category:
            articles = [a for a in articles if a.get("category", "").lower() == category.lower()]
        
        return {
            "success": True,
            "last_update": news_data.get("last_update"),
            "source": news_data.get("source"),
            "total_articles": len(articles),
            "articles": articles,
            "filters_applied": {
                "region": region,
                "category": category
            }
        }
    except Exception as e:
        logging.error(f"Erreur récupération actualités: {e}")
        return {
            "success": False,
            "error": str(e),
            "articles": []
        }


@api_router.get("/news/by-region")
async def get_news_grouped_by_region(force_refresh: bool = Query(False)):
    """Récupérer les actualités groupées par région africaine"""
    try:
        news_data = await get_news(force_refresh=force_refresh)
        articles = news_data.get("articles", [])
        by_region = get_news_by_region(articles)
        region_counts = {region: len(arts) for region, arts in by_region.items()}
        
        return {
            "success": True,
            "last_update": news_data.get("last_update"),
            "regions": list(by_region.keys()),
            "region_counts": region_counts,
            "articles_by_region": by_region
        }
    except Exception as e:
        logging.error(f"Erreur récupération news par région: {e}")
        return {"success": False, "error": str(e)}


@api_router.get("/news/by-category")
async def get_news_grouped_by_category(force_refresh: bool = Query(False)):
    """Récupérer les actualités groupées par catégorie économique"""
    try:
        news_data = await get_news(force_refresh=force_refresh)
        articles = news_data.get("articles", [])
        by_category = get_news_by_category(articles)
        category_counts = {cat: len(arts) for cat, arts in by_category.items()}
        
        return {
            "success": True,
            "last_update": news_data.get("last_update"),
            "categories": list(by_category.keys()),
            "category_counts": category_counts,
            "articles_by_category": by_category
        }
    except Exception as e:
        logging.error(f"Erreur récupération news par catégorie: {e}")
        return {"success": False, "error": str(e)}


# =====================================================
# ENDPOINTS STATISTIQUES COMMERCIALES OEC
# Source: Observatory of Economic Complexity (OEC/BACI)
# =====================================================

@api_router.get("/oec/countries")
async def get_oec_african_countries(
    language: str = Query("fr", description="Langue (fr/en)")
):
    """Liste des pays africains disponibles pour les statistiques OEC"""
    return {
        "success": True,
        "total": len(AFRICAN_COUNTRIES_OEC),
        "countries": get_african_countries_list(language),
        "source": "OEC/BACI"
    }

@api_router.get("/oec/years")
async def get_oec_available_years():
    """Années disponibles dans les données OEC"""
    years = await oec_service.get_available_years()
    return {"success": True, "years": years, "source": "OEC/BACI"}

@api_router.get("/oec/exports/{country_iso3}")
async def get_oec_country_exports(
    country_iso3: str,
    year: int = Query(2022),
    hs_level: str = Query("HS4"),
    limit: int = Query(50)
):
    """Exportations d'un pays africain par produit HS"""
    result = await oec_service.get_exports_by_product(country_iso3, year, hs_level, limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@api_router.get("/oec/imports/{country_iso3}")
async def get_oec_country_imports(
    country_iso3: str,
    year: int = Query(2022),
    hs_level: str = Query("HS4"),
    limit: int = Query(50)
):
    """Importations d'un pays africain par produit HS"""
    result = await oec_service.get_imports_by_product(country_iso3, year, hs_level, limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@api_router.get("/oec/product/{hs_code}")
async def get_oec_product_trade(
    hs_code: str,
    year: int = Query(2022),
    trade_flow: str = Query("exports"),
    limit: int = Query(50)
):
    """Statistiques commerciales mondiales pour un code HS"""
    result = await oec_service.get_trade_by_hs_code(hs_code, year, trade_flow, limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@api_router.get("/oec/product/{hs_code}/africa")
async def get_oec_african_exporters(
    hs_code: str,
    year: int = Query(2022),
    limit: int = Query(20)
):
    """Top exportateurs africains pour un produit HS"""
    result = await oec_service.get_top_african_exporters(hs_code, year, limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@api_router.get("/oec/bilateral/{exporter_iso3}/{importer_iso3}")
async def get_oec_bilateral_trade(
    exporter_iso3: str,
    importer_iso3: str,
    year: int = Query(2022),
    hs_level: str = Query("HS4"),
    limit: int = Query(50)
):
    """Commerce bilatéral entre deux pays africains"""
    result = await oec_service.get_bilateral_trade(exporter_iso3, importer_iso3, year, hs_level, limit)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


# Include the router in the main app
app.include_router(api_router)