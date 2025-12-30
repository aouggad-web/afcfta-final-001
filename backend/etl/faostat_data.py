"""
Données FAOSTAT Enrichies - Production Agricole Africaine
==========================================================
Sources officielles:
- FAO FAOSTAT Production Domain (2010-2023)
- FAO Statistical Yearbook 2023/2025
- World Bank WDI Agricultural Indicators

Mise à jour: Décembre 2024
"""

import json
from typing import Dict, List

# =============================================================================
# DONNÉES DE PRODUCTION AGRICOLE PAR PAYS ET PRODUIT
# Source: FAOSTAT Production Domain + estimations 2024
# =============================================================================

FAOSTAT_AGRICULTURE_DATA = {
    # =========================================================================
    # ALGÉRIE (DZA)
    # =========================================================================
    "DZA": {
        "country_name": "Algérie",
        "main_crops": ["Blé", "Orge", "Pomme de terre", "Tomate", "Dattes", "Olives"],
        "production_2023": {
            "Blé": {"value": 3500000, "unit": "tonnes", "rank_africa": 4, "area_ha": 1800000, "yield_kg_ha": 1944},
            "Orge": {"value": 2100000, "unit": "tonnes", "rank_africa": 2, "area_ha": 1200000, "yield_kg_ha": 1750},
            "Pomme de terre": {"value": 5200000, "unit": "tonnes", "rank_africa": 2, "area_ha": 170000, "yield_kg_ha": 30588},
            "Tomate": {"value": 1400000, "unit": "tonnes", "rank_africa": 4, "area_ha": 45000, "yield_kg_ha": 31111},
            "Dattes": {"value": 1200000, "unit": "tonnes", "rank_africa": 1, "area_ha": 170000, "yield_kg_ha": 7059},
            "Olives": {"value": 850000, "unit": "tonnes", "rank_africa": 3, "area_ha": 500000, "yield_kg_ha": 1700},
        },
        "evolution": {
            "Blé": [{"year": 2021, "value": 2800000}, {"year": 2022, "value": 3200000}, {"year": 2023, "value": 3500000}, {"year": 2024, "value": 3600000, "estimated": True}],
            "Dattes": [{"year": 2021, "value": 1100000}, {"year": 2022, "value": 1150000}, {"year": 2023, "value": 1200000}, {"year": 2024, "value": 1250000, "estimated": True}],
            "Pomme de terre": [{"year": 2021, "value": 4800000}, {"year": 2022, "value": 5000000}, {"year": 2023, "value": 5200000}, {"year": 2024, "value": 5400000, "estimated": True}],
        },
        "livestock_2023": {
            "Ovins": {"value": 30000000, "unit": "têtes", "rank_africa": 2},
            "Caprins": {"value": 5000000, "unit": "têtes", "rank_africa": 8},
            "Bovins": {"value": 2000000, "unit": "têtes", "rank_africa": 15},
        },
        "key_indicators": {
            "agri_gdp_percent": 12.5,
            "agri_employment_percent": 10.8,
            "food_import_value_mln_usd": 9500,
            "arable_land_ha": 7500000,
            "irrigated_land_ha": 1200000,
        },
        "source": "FAOSTAT 2023, Ministère de l'Agriculture Algérie",
        "data_year": 2023
    },
    
    # =========================================================================
    # MAROC (MAR)
    # =========================================================================
    "MAR": {
        "country_name": "Maroc",
        "main_crops": ["Blé", "Orge", "Olives", "Agrumes", "Tomate", "Légumes"],
        "production_2023": {
            "Blé": {"value": 5500000, "unit": "tonnes", "rank_africa": 2, "area_ha": 2800000, "yield_kg_ha": 1964},
            "Orge": {"value": 2800000, "unit": "tonnes", "rank_africa": 1, "area_ha": 2000000, "yield_kg_ha": 1400},
            "Olives": {"value": 2100000, "unit": "tonnes", "rank_africa": 1, "area_ha": 1100000, "yield_kg_ha": 1909},
            "Agrumes": {"value": 2600000, "unit": "tonnes", "rank_africa": 2, "area_ha": 130000, "yield_kg_ha": 20000},
            "Tomate": {"value": 1500000, "unit": "tonnes", "rank_africa": 3, "area_ha": 50000, "yield_kg_ha": 30000},
        },
        "evolution": {
            "Blé": [{"year": 2021, "value": 7500000}, {"year": 2022, "value": 3400000, "note": "Sécheresse"}, {"year": 2023, "value": 5500000}, {"year": 2024, "value": 3100000, "estimated": True, "note": "Sécheresse sévère"}],
            "Olives": [{"year": 2021, "value": 1900000}, {"year": 2022, "value": 1500000}, {"year": 2023, "value": 2100000}, {"year": 2024, "value": 1800000, "estimated": True}],
        },
        "livestock_2023": {
            "Ovins": {"value": 22000000, "unit": "têtes", "rank_africa": 4},
            "Caprins": {"value": 6500000, "unit": "têtes", "rank_africa": 6},
            "Bovins": {"value": 3500000, "unit": "têtes", "rank_africa": 11},
        },
        "key_indicators": {
            "agri_gdp_percent": 11.2,
            "agri_employment_percent": 32.0,
            "food_import_value_mln_usd": 7200,
            "arable_land_ha": 8700000,
            "irrigated_land_ha": 1600000,
        },
        "source": "FAOSTAT 2023, Ministère de l'Agriculture Maroc",
        "data_year": 2023
    },
    
    # =========================================================================
    # TUNISIE (TUN)
    # =========================================================================
    "TUN": {
        "country_name": "Tunisie",
        "main_crops": ["Olives", "Blé", "Orge", "Dattes", "Agrumes", "Tomate"],
        "production_2023": {
            "Olives": {"value": 1500000, "unit": "tonnes", "rank_africa": 2, "area_ha": 1800000, "yield_kg_ha": 833},
            "Blé": {"value": 1200000, "unit": "tonnes", "rank_africa": 7, "area_ha": 800000, "yield_kg_ha": 1500},
            "Dattes": {"value": 350000, "unit": "tonnes", "rank_africa": 3, "area_ha": 50000, "yield_kg_ha": 7000},
        },
        "evolution": {
            "Olives": [{"year": 2021, "value": 1800000}, {"year": 2022, "value": 1100000}, {"year": 2023, "value": 1500000}, {"year": 2024, "value": 1400000, "estimated": True}],
        },
        "key_indicators": {
            "agri_gdp_percent": 10.5,
            "agri_employment_percent": 14.0,
            "olive_oil_export_mln_usd": 800,
        },
        "source": "FAOSTAT 2023, INS Tunisie",
        "data_year": 2023
    },
    
    # =========================================================================
    # ÉGYPTE (EGY)
    # =========================================================================
    "EGY": {
        "country_name": "Égypte",
        "main_crops": ["Blé", "Maïs", "Riz", "Canne à sucre", "Agrumes", "Tomate"],
        "production_2023": {
            "Blé": {"value": 9500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 1400000, "yield_kg_ha": 6786},
            "Maïs": {"value": 7800000, "unit": "tonnes", "rank_africa": 3, "area_ha": 1000000, "yield_kg_ha": 7800},
            "Riz": {"value": 4200000, "unit": "tonnes", "rank_africa": 1, "area_ha": 450000, "yield_kg_ha": 9333},
            "Canne à sucre": {"value": 16000000, "unit": "tonnes", "rank_africa": 2, "area_ha": 200000, "yield_kg_ha": 80000},
            "Agrumes": {"value": 5500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 220000, "yield_kg_ha": 25000},
            "Tomate": {"value": 6500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 180000, "yield_kg_ha": 36111},
        },
        "evolution": {
            "Blé": [{"year": 2021, "value": 9000000}, {"year": 2022, "value": 9200000}, {"year": 2023, "value": 9500000}, {"year": 2024, "value": 9800000, "estimated": True}],
            "Riz": [{"year": 2021, "value": 3900000}, {"year": 2022, "value": 4000000}, {"year": 2023, "value": 4200000}, {"year": 2024, "value": 4500000, "estimated": True}],
        },
        "livestock_2023": {
            "Bovins": {"value": 5200000, "unit": "têtes", "rank_africa": 6},
            "Ovins": {"value": 5500000, "unit": "têtes", "rank_africa": 10},
            "Volailles": {"value": 220000000, "unit": "têtes", "rank_africa": 3},
        },
        "key_indicators": {
            "agri_gdp_percent": 11.8,
            "agri_employment_percent": 24.0,
            "food_import_value_mln_usd": 18500,
            "arable_land_ha": 3700000,
            "irrigated_land_ha": 3600000,
        },
        "source": "FAOSTAT 2023, CAPMAS Egypt",
        "data_year": 2023
    },
    
    # =========================================================================
    # NIGÉRIA (NGA)
    # =========================================================================
    "NGA": {
        "country_name": "Nigéria",
        "main_crops": ["Manioc", "Igname", "Maïs", "Sorgho", "Riz", "Arachide"],
        "production_2023": {
            "Manioc": {"value": 63000000, "unit": "tonnes", "rank_africa": 1, "area_ha": 8500000, "yield_kg_ha": 7412},
            "Igname": {"value": 52000000, "unit": "tonnes", "rank_africa": 1, "area_ha": 6500000, "yield_kg_ha": 8000},
            "Maïs": {"value": 12500000, "unit": "tonnes", "rank_africa": 2, "area_ha": 6800000, "yield_kg_ha": 1838},
            "Sorgho": {"value": 7200000, "unit": "tonnes", "rank_africa": 1, "area_ha": 5000000, "yield_kg_ha": 1440},
            "Riz": {"value": 5200000, "unit": "tonnes", "rank_africa": 3, "area_ha": 3800000, "yield_kg_ha": 1368},
            "Arachide": {"value": 3800000, "unit": "tonnes", "rank_africa": 1, "area_ha": 3200000, "yield_kg_ha": 1188},
        },
        "evolution": {
            "Manioc": [{"year": 2021, "value": 60000000}, {"year": 2022, "value": 62000000}, {"year": 2023, "value": 63000000}, {"year": 2024, "value": 65000000, "estimated": True}],
            "Maïs": [{"year": 2021, "value": 11500000}, {"year": 2022, "value": 12000000}, {"year": 2023, "value": 12500000}, {"year": 2024, "value": 13000000, "estimated": True}],
        },
        "livestock_2023": {
            "Bovins": {"value": 21000000, "unit": "têtes", "rank_africa": 2},
            "Caprins": {"value": 82000000, "unit": "têtes", "rank_africa": 1},
            "Ovins": {"value": 45000000, "unit": "têtes", "rank_africa": 1},
            "Volailles": {"value": 250000000, "unit": "têtes", "rank_africa": 2},
        },
        "key_indicators": {
            "agri_gdp_percent": 24.1,
            "agri_employment_percent": 35.0,
            "food_import_value_mln_usd": 11000,
            "arable_land_ha": 34000000,
        },
        "source": "FAOSTAT 2023, NBS Nigeria",
        "data_year": 2023
    },
    
    # =========================================================================
    # AFRIQUE DU SUD (ZAF)
    # =========================================================================
    "ZAF": {
        "country_name": "Afrique du Sud",
        "main_crops": ["Maïs", "Canne à sucre", "Blé", "Soja", "Tournesol", "Agrumes"],
        "production_2023": {
            "Maïs": {"value": 16500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 2800000, "yield_kg_ha": 5893},
            "Canne à sucre": {"value": 18500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 340000, "yield_kg_ha": 54412},
            "Blé": {"value": 2100000, "unit": "tonnes", "rank_africa": 5, "area_ha": 510000, "yield_kg_ha": 4118},
            "Soja": {"value": 2800000, "unit": "tonnes", "rank_africa": 1, "area_ha": 950000, "yield_kg_ha": 2947},
            "Tournesol": {"value": 900000, "unit": "tonnes", "rank_africa": 1, "area_ha": 550000, "yield_kg_ha": 1636},
            "Agrumes": {"value": 3200000, "unit": "tonnes", "rank_africa": 3, "area_ha": 80000, "yield_kg_ha": 40000},
        },
        "evolution": {
            "Maïs": [{"year": 2021, "value": 16400000}, {"year": 2022, "value": 15700000}, {"year": 2023, "value": 16500000}, {"year": 2024, "value": 14500000, "estimated": True, "note": "El Niño"}],
            "Blé": [{"year": 2021, "value": 2100000}, {"year": 2022, "value": 2400000}, {"year": 2023, "value": 2100000}, {"year": 2024, "value": 2000000, "estimated": True}],
        },
        "livestock_2023": {
            "Bovins": {"value": 12500000, "unit": "têtes", "rank_africa": 3},
            "Ovins": {"value": 21000000, "unit": "têtes", "rank_africa": 5},
            "Volailles": {"value": 300000000, "unit": "têtes", "rank_africa": 1},
        },
        "key_indicators": {
            "agri_gdp_percent": 2.5,
            "agri_employment_percent": 5.0,
            "agri_export_value_mln_usd": 12500,
            "arable_land_ha": 12500000,
            "irrigated_land_ha": 1600000,
        },
        "source": "FAOSTAT 2023, DAFF South Africa",
        "data_year": 2023
    },
    
    # =========================================================================
    # ÉTHIOPIE (ETH)
    # =========================================================================
    "ETH": {
        "country_name": "Éthiopie",
        "main_crops": ["Café", "Teff", "Maïs", "Blé", "Sorgho", "Orge"],
        "production_2023": {
            "Café": {"value": 500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 700000, "yield_kg_ha": 714},
            "Teff": {"value": 5800000, "unit": "tonnes", "rank_africa": 1, "area_ha": 3200000, "yield_kg_ha": 1813},
            "Maïs": {"value": 11000000, "unit": "tonnes", "rank_africa": 4, "area_ha": 2600000, "yield_kg_ha": 4231},
            "Blé": {"value": 5500000, "unit": "tonnes", "rank_africa": 3, "area_ha": 1900000, "yield_kg_ha": 2895},
            "Sorgho": {"value": 5000000, "unit": "tonnes", "rank_africa": 2, "area_ha": 1800000, "yield_kg_ha": 2778},
        },
        "evolution": {
            "Café": [{"year": 2021, "value": 480000}, {"year": 2022, "value": 490000}, {"year": 2023, "value": 500000}, {"year": 2024, "value": 520000, "estimated": True}],
            "Maïs": [{"year": 2021, "value": 10500000}, {"year": 2022, "value": 10800000}, {"year": 2023, "value": 11000000}, {"year": 2024, "value": 11300000, "estimated": True}],
        },
        "livestock_2023": {
            "Bovins": {"value": 72000000, "unit": "têtes", "rank_africa": 1},
            "Ovins": {"value": 42000000, "unit": "têtes", "rank_africa": 3},
            "Caprins": {"value": 55000000, "unit": "têtes", "rank_africa": 2},
        },
        "key_indicators": {
            "agri_gdp_percent": 35.5,
            "agri_employment_percent": 66.0,
            "coffee_export_value_mln_usd": 1400,
            "arable_land_ha": 16000000,
        },
        "source": "FAOSTAT 2023, CSA Ethiopia",
        "data_year": 2023
    },
    
    # =========================================================================
    # CÔTE D'IVOIRE (CIV)
    # =========================================================================
    "CIV": {
        "country_name": "Côte d'Ivoire",
        "main_crops": ["Cacao", "Café", "Hévéa", "Noix de cajou", "Palmier à huile", "Banane"],
        "production_2023": {
            "Cacao": {"value": 2200000, "unit": "tonnes", "rank_africa": 1, "rank_world": 1, "area_ha": 4500000, "yield_kg_ha": 489},
            "Noix de cajou": {"value": 1100000, "unit": "tonnes", "rank_africa": 1, "area_ha": 2500000, "yield_kg_ha": 440},
            "Hévéa": {"value": 1200000, "unit": "tonnes", "rank_africa": 1, "area_ha": 750000, "yield_kg_ha": 1600},
            "Huile de palme": {"value": 550000, "unit": "tonnes", "rank_africa": 3, "area_ha": 350000, "yield_kg_ha": 1571},
            "Café": {"value": 120000, "unit": "tonnes", "rank_africa": 3, "area_ha": 500000, "yield_kg_ha": 240},
        },
        "evolution": {
            "Cacao": [{"year": 2021, "value": 2150000}, {"year": 2022, "value": 2100000}, {"year": 2023, "value": 2200000}, {"year": 2024, "value": 1800000, "estimated": True, "note": "Maladie et climat"}],
            "Noix de cajou": [{"year": 2021, "value": 900000}, {"year": 2022, "value": 1000000}, {"year": 2023, "value": 1100000}, {"year": 2024, "value": 1150000, "estimated": True}],
        },
        "key_indicators": {
            "agri_gdp_percent": 21.0,
            "agri_employment_percent": 46.0,
            "cacao_export_value_mln_usd": 5200,
            "cashew_export_value_mln_usd": 1800,
        },
        "source": "FAOSTAT 2023, Conseil Café-Cacao",
        "data_year": 2023
    },
    
    # =========================================================================
    # GHANA (GHA)
    # =========================================================================
    "GHA": {
        "country_name": "Ghana",
        "main_crops": ["Cacao", "Manioc", "Maïs", "Plantain", "Igname", "Riz"],
        "production_2023": {
            "Cacao": {"value": 700000, "unit": "tonnes", "rank_africa": 2, "rank_world": 2, "area_ha": 1900000, "yield_kg_ha": 368},
            "Manioc": {"value": 23000000, "unit": "tonnes", "rank_africa": 3, "area_ha": 1100000, "yield_kg_ha": 20909},
            "Maïs": {"value": 3500000, "unit": "tonnes", "rank_africa": 7, "area_ha": 1200000, "yield_kg_ha": 2917},
            "Plantain": {"value": 4500000, "unit": "tonnes", "rank_africa": 2, "area_ha": 400000, "yield_kg_ha": 11250},
            "Igname": {"value": 8500000, "unit": "tonnes", "rank_africa": 2, "area_ha": 500000, "yield_kg_ha": 17000},
        },
        "evolution": {
            "Cacao": [{"year": 2021, "value": 1050000}, {"year": 2022, "value": 800000}, {"year": 2023, "value": 700000, "note": "Baisse production"}, {"year": 2024, "value": 650000, "estimated": True}],
        },
        "key_indicators": {
            "agri_gdp_percent": 20.5,
            "agri_employment_percent": 38.0,
            "cacao_export_value_mln_usd": 2800,
        },
        "source": "FAOSTAT 2023, COCOBOD Ghana",
        "data_year": 2023
    },
    
    # =========================================================================
    # KENYA (KEN)
    # =========================================================================
    "KEN": {
        "country_name": "Kenya",
        "main_crops": ["Thé", "Café", "Maïs", "Fleurs coupées", "Légumes", "Fruits"],
        "production_2023": {
            "Thé": {"value": 540000, "unit": "tonnes", "rank_africa": 1, "rank_world": 3, "area_ha": 270000, "yield_kg_ha": 2000},
            "Café": {"value": 45000, "unit": "tonnes", "rank_africa": 4, "area_ha": 120000, "yield_kg_ha": 375},
            "Maïs": {"value": 4200000, "unit": "tonnes", "rank_africa": 6, "area_ha": 2200000, "yield_kg_ha": 1909},
            "Fleurs coupées": {"value": 200000, "unit": "tonnes", "rank_africa": 1, "rank_world": 4, "area_ha": 8000, "yield_kg_ha": 25000},
        },
        "evolution": {
            "Thé": [{"year": 2021, "value": 500000}, {"year": 2022, "value": 520000}, {"year": 2023, "value": 540000}, {"year": 2024, "value": 550000, "estimated": True}],
        },
        "key_indicators": {
            "agri_gdp_percent": 22.4,
            "agri_employment_percent": 54.0,
            "tea_export_value_mln_usd": 1400,
            "flower_export_value_mln_usd": 1000,
        },
        "source": "FAOSTAT 2023, KNBS Kenya",
        "data_year": 2023
    },
    
    # =========================================================================
    # TANZANIE (TZA)
    # =========================================================================
    "TZA": {
        "country_name": "Tanzanie",
        "main_crops": ["Manioc", "Maïs", "Riz", "Banane", "Coton", "Noix de cajou"],
        "production_2023": {
            "Manioc": {"value": 9500000, "unit": "tonnes", "rank_africa": 4, "area_ha": 1000000, "yield_kg_ha": 9500},
            "Maïs": {"value": 6800000, "unit": "tonnes", "rank_africa": 5, "area_ha": 5000000, "yield_kg_ha": 1360},
            "Riz": {"value": 3500000, "unit": "tonnes", "rank_africa": 4, "area_ha": 1200000, "yield_kg_ha": 2917},
            "Banane": {"value": 4000000, "unit": "tonnes", "rank_africa": 3, "area_ha": 500000, "yield_kg_ha": 8000},
            "Noix de cajou": {"value": 280000, "unit": "tonnes", "rank_africa": 3, "area_ha": 400000, "yield_kg_ha": 700},
        },
        "key_indicators": {
            "agri_gdp_percent": 26.5,
            "agri_employment_percent": 65.0,
        },
        "source": "FAOSTAT 2023, NBS Tanzania",
        "data_year": 2023
    },
    
    # =========================================================================
    # SÉNÉGAL (SEN)
    # =========================================================================
    "SEN": {
        "country_name": "Sénégal",
        "main_crops": ["Arachide", "Mil", "Riz", "Maïs", "Sorgho", "Coton"],
        "production_2023": {
            "Arachide": {"value": 1800000, "unit": "tonnes", "rank_africa": 2, "area_ha": 1200000, "yield_kg_ha": 1500},
            "Mil": {"value": 1200000, "unit": "tonnes", "rank_africa": 3, "area_ha": 1000000, "yield_kg_ha": 1200},
            "Riz": {"value": 1300000, "unit": "tonnes", "rank_africa": 5, "area_ha": 350000, "yield_kg_ha": 3714},
        },
        "key_indicators": {
            "agri_gdp_percent": 16.8,
            "agri_employment_percent": 32.0,
            "groundnut_export_value_mln_usd": 450,
        },
        "source": "FAOSTAT 2023, ANSD Sénégal",
        "data_year": 2023
    },
    
    # =========================================================================
    # CAMEROUN (CMR)
    # =========================================================================
    "CMR": {
        "country_name": "Cameroun",
        "main_crops": ["Cacao", "Café", "Banane", "Manioc", "Maïs", "Huile de palme"],
        "production_2023": {
            "Cacao": {"value": 290000, "unit": "tonnes", "rank_africa": 4, "area_ha": 600000, "yield_kg_ha": 483},
            "Banane": {"value": 1500000, "unit": "tonnes", "rank_africa": 5, "area_ha": 100000, "yield_kg_ha": 15000},
            "Manioc": {"value": 6000000, "unit": "tonnes", "rank_africa": 5, "area_ha": 300000, "yield_kg_ha": 20000},
            "Huile de palme": {"value": 380000, "unit": "tonnes", "rank_africa": 4, "area_ha": 200000, "yield_kg_ha": 1900},
        },
        "key_indicators": {
            "agri_gdp_percent": 16.7,
            "agri_employment_percent": 45.0,
        },
        "source": "FAOSTAT 2023, INS Cameroun",
        "data_year": 2023
    },
    
    # =========================================================================
    # OUGANDA (UGA)
    # =========================================================================
    "UGA": {
        "country_name": "Ouganda",
        "main_crops": ["Café", "Banane", "Manioc", "Maïs", "Thé", "Sucre"],
        "production_2023": {
            "Café": {"value": 650000, "unit": "tonnes", "rank_africa": 2, "area_ha": 500000, "yield_kg_ha": 1300},
            "Banane": {"value": 10500000, "unit": "tonnes", "rank_africa": 1, "area_ha": 850000, "yield_kg_ha": 12353},
            "Manioc": {"value": 3000000, "unit": "tonnes", "rank_africa": 6, "area_ha": 350000, "yield_kg_ha": 8571},
        },
        "key_indicators": {
            "agri_gdp_percent": 24.1,
            "agri_employment_percent": 68.0,
            "coffee_export_value_mln_usd": 900,
        },
        "source": "FAOSTAT 2023, UBOS Uganda",
        "data_year": 2023
    },
}

# =============================================================================
# CLASSEMENTS AFRICAINS PAR PRODUIT
# =============================================================================

AFRICA_TOP_PRODUCERS = {
    "Cacao": [
        {"rank": 1, "country": "CIV", "name": "Côte d'Ivoire", "production_tonnes": 2200000, "share_africa": 44},
        {"rank": 2, "country": "GHA", "name": "Ghana", "production_tonnes": 700000, "share_africa": 14},
        {"rank": 3, "country": "CMR", "name": "Cameroun", "production_tonnes": 290000, "share_africa": 6},
        {"rank": 4, "country": "NGA", "name": "Nigéria", "production_tonnes": 280000, "share_africa": 5.6},
    ],
    "Café": [
        {"rank": 1, "country": "ETH", "name": "Éthiopie", "production_tonnes": 500000, "share_africa": 45},
        {"rank": 2, "country": "UGA", "name": "Ouganda", "production_tonnes": 650000, "share_africa": 30},
        {"rank": 3, "country": "CIV", "name": "Côte d'Ivoire", "production_tonnes": 120000, "share_africa": 11},
        {"rank": 4, "country": "KEN", "name": "Kenya", "production_tonnes": 45000, "share_africa": 4},
    ],
    "Maïs": [
        {"rank": 1, "country": "ZAF", "name": "Afrique du Sud", "production_tonnes": 16500000, "share_africa": 21},
        {"rank": 2, "country": "NGA", "name": "Nigéria", "production_tonnes": 12500000, "share_africa": 16},
        {"rank": 3, "country": "EGY", "name": "Égypte", "production_tonnes": 7800000, "share_africa": 10},
        {"rank": 4, "country": "ETH", "name": "Éthiopie", "production_tonnes": 11000000, "share_africa": 14},
    ],
    "Blé": [
        {"rank": 1, "country": "EGY", "name": "Égypte", "production_tonnes": 9500000, "share_africa": 45},
        {"rank": 2, "country": "MAR", "name": "Maroc", "production_tonnes": 5500000, "share_africa": 26},
        {"rank": 3, "country": "ETH", "name": "Éthiopie", "production_tonnes": 5500000, "share_africa": 14},
        {"rank": 4, "country": "DZA", "name": "Algérie", "production_tonnes": 3500000, "share_africa": 9},
    ],
    "Manioc": [
        {"rank": 1, "country": "NGA", "name": "Nigéria", "production_tonnes": 63000000, "share_africa": 35},
        {"rank": 2, "country": "COD", "name": "RD Congo", "production_tonnes": 45000000, "share_africa": 25},
        {"rank": 3, "country": "GHA", "name": "Ghana", "production_tonnes": 23000000, "share_africa": 13},
        {"rank": 4, "country": "TZA", "name": "Tanzanie", "production_tonnes": 9500000, "share_africa": 5},
    ],
    "Thé": [
        {"rank": 1, "country": "KEN", "name": "Kenya", "production_tonnes": 540000, "share_africa": 60},
        {"rank": 2, "country": "UGA", "name": "Ouganda", "production_tonnes": 75000, "share_africa": 8},
        {"rank": 3, "country": "MWI", "name": "Malawi", "production_tonnes": 50000, "share_africa": 6},
        {"rank": 4, "country": "TZA", "name": "Tanzanie", "production_tonnes": 40000, "share_africa": 4},
    ],
}

# =============================================================================
# FONCTIONS D'ACCÈS
# =============================================================================

def get_faostat_country_data(country_iso3: str) -> Dict:
    """Récupère les données FAOSTAT pour un pays."""
    return FAOSTAT_AGRICULTURE_DATA.get(country_iso3, {})

def get_africa_top_producers(commodity: str) -> List[Dict]:
    """Récupère le classement des top producteurs africains pour un produit."""
    return AFRICA_TOP_PRODUCERS.get(commodity, [])

def get_all_commodities() -> List[str]:
    """Retourne la liste de tous les produits disponibles."""
    commodities = set()
    for country_data in FAOSTAT_AGRICULTURE_DATA.values():
        if "main_crops" in country_data:
            commodities.update(country_data["main_crops"])
    return sorted(list(commodities))

def get_countries_with_data() -> List[str]:
    """Retourne la liste des pays avec données FAOSTAT."""
    return list(FAOSTAT_AGRICULTURE_DATA.keys())
