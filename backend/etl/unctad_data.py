"""
UNCTAD Trade Statistics Data
=============================
Source: UNCTAD COMTRADE Database 2023
       UNCTAD Maritime Transport Review 2023
       UNCTAD Digital Economy Report 2023

Data covering African trade flows, maritime statistics and logistics
"""

from typing import Dict, List

# =============================================================================
# UNCTAD MARITIME STATISTICS - AFRICAN PORTS
# Source: UNCTAD Review of Maritime Transport 2023
# =============================================================================

UNCTAD_PORT_STATISTICS = {
    "total_african_port_throughput_teu_2023": 28500000,  # 28.5 million TEU
    "growth_rate_2022_2023": 4.2,
    "share_global_trade": 3.8,
    "top_ports": [
        {
            "port": "Tanger Med",
            "country": "Morocco",
            "country_fr": "Maroc",
            "throughput_teu": 7800000,
            "growth_rate": 8.5,
            "rank_africa": 1,
            "rank_global": 23
        },
        {
            "port": "Port Said",
            "country": "Egypt",
            "country_fr": "Égypte",
            "throughput_teu": 4200000,
            "growth_rate": 5.2,
            "rank_africa": 2,
            "rank_global": 45
        },
        {
            "port": "Durban",
            "country": "South Africa",
            "country_fr": "Afrique du Sud",
            "throughput_teu": 2900000,
            "growth_rate": 2.1,
            "rank_africa": 3,
            "rank_global": 58
        },
        {
            "port": "Lagos (Apapa/Tin Can)",
            "country": "Nigeria",
            "country_fr": "Nigéria",
            "throughput_teu": 1850000,
            "growth_rate": 6.3,
            "rank_africa": 4,
            "rank_global": 78
        },
        {
            "port": "Mombasa",
            "country": "Kenya",
            "country_fr": "Kenya",
            "throughput_teu": 1450000,
            "growth_rate": 4.8,
            "rank_africa": 5,
            "rank_global": 92
        },
        {
            "port": "Alger",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 1380000,
            "growth_rate": 5.8,
            "rank_africa": 6,
            "rank_global": 95
        },
        {
            "port": "Djibouti",
            "country": "Djibouti",
            "country_fr": "Djibouti",
            "throughput_teu": 1120000,
            "growth_rate": 12.5,
            "rank_africa": 7,
            "rank_global": 105
        },
        {
            "port": "Tema",
            "country": "Ghana",
            "country_fr": "Ghana",
            "throughput_teu": 1050000,
            "growth_rate": 9.8,
            "rank_africa": 8,
            "rank_global": 108
        },
        {
            "port": "Abidjan",
            "country": "Côte d'Ivoire",
            "country_fr": "Côte d'Ivoire",
            "throughput_teu": 980000,
            "growth_rate": 7.2,
            "rank_africa": 9,
            "rank_global": 112
        },
        {
            "port": "Oran",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 620000,
            "growth_rate": 6.2,
            "rank_africa": 10,
            "rank_global": 135
        },
        {
            "port": "Béjaïa",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 380000,
            "growth_rate": 4.5,
            "rank_africa": 14,
            "rank_global": 165
        },
        {
            "port": "Skikda",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 290000,
            "growth_rate": 3.8,
            "rank_africa": 18,
            "rank_global": 185
        },
        {
            "port": "Annaba",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 245000,
            "growth_rate": 4.1,
            "rank_africa": 21,
            "rank_global": 198
        },
        {
            "port": "Mostaganem",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 185000,
            "growth_rate": 7.5,
            "rank_africa": 25,
            "rank_global": 215
        },
        {
            "port": "Djen Djen",
            "country": "Algeria",
            "country_fr": "Algérie",
            "throughput_teu": 520000,
            "growth_rate": 15.2,
            "rank_africa": 12,
            "rank_global": 148
        }
    ],
    "algeria_ports_summary": {
        "total_throughput_teu": 3620000,
        "share_african_trade": 12.7,
        "growth_rate_2023": 6.8,
        "main_exports": ["Hydrocarbures", "Phosphates", "Produits chimiques", "Dattes"],
        "main_imports": ["Équipements industriels", "Céréales", "Véhicules", "Produits manufacturés"],
        "strategic_position": "Gateway to Maghreb and Sahel markets",
        "port_count": 11,
        "container_terminals": 6,
        "investment_2023_mln_usd": 850
    }
}
            "throughput_teu": 980000,
            "growth_rate": 7.2,
            "rank_africa": 7,
            "rank_global": 112
        },
        {
            "port": "Tema",
            "country": "Ghana",
            "country_fr": "Ghana",
            "throughput_teu": 1050000,
            "growth_rate": 9.8,
            "rank_africa": 8,
            "rank_global": 108
        }
    ]
}

# =============================================================================
# UNCTAD TRADE FLOW STATISTICS
# Source: UNCTAD COMTRADE 2023
# =============================================================================

UNCTAD_TRADE_FLOWS = {
    "intra_african_trade_2023": {
        "value_billion_usd": 192.5,
        "share_total_african_trade": 14.8,
        "growth_rate_2022_2023": 8.2,
        "projected_2030": 385.0,
        "projected_growth_with_afcfta": 52.3
    },
    "africa_world_trade_2023": {
        "total_exports_billion_usd": 556.8,
        "total_imports_billion_usd": 598.2,
        "trade_balance_billion_usd": -41.4,
        "top_export_partners": [
            {"partner": "China", "share": 15.2},
            {"partner": "EU", "share": 28.5},
            {"partner": "USA", "share": 8.3},
            {"partner": "India", "share": 9.1},
            {"partner": "UAE", "share": 4.2}
        ],
        "top_import_partners": [
            {"partner": "China", "share": 18.5},
            {"partner": "EU", "share": 25.2},
            {"partner": "USA", "share": 6.8},
            {"partner": "India", "share": 8.9},
            {"partner": "UAE", "share": 5.1}
        ]
    },
    "services_trade_2023": {
        "exports_billion_usd": 89.5,
        "imports_billion_usd": 142.3,
        "top_sectors": [
            {"sector": "Transport", "sector_fr": "Transport", "share": 28.5},
            {"sector": "Travel/Tourism", "sector_fr": "Voyage/Tourisme", "share": 35.2},
            {"sector": "ICT Services", "sector_fr": "Services TIC", "share": 12.8},
            {"sector": "Financial Services", "sector_fr": "Services financiers", "share": 8.5},
            {"sector": "Business Services", "sector_fr": "Services aux entreprises", "share": 15.0}
        ]
    }
}

# =============================================================================
# UNCTAD LINER SHIPPING CONNECTIVITY INDEX (LSCI)
# Source: UNCTAD 2023
# =============================================================================

UNCTAD_LSCI_AFRICA = [
    {"country": "Morocco", "country_fr": "Maroc", "lsci_2023": 72.5, "rank_africa": 1, "rank_global": 18},
    {"country": "Egypt", "country_fr": "Égypte", "lsci_2023": 68.2, "rank_africa": 2, "rank_global": 22},
    {"country": "South Africa", "country_fr": "Afrique du Sud", "lsci_2023": 42.8, "rank_africa": 3, "rank_global": 35},
    {"country": "Togo", "country_fr": "Togo", "lsci_2023": 28.5, "rank_africa": 4, "rank_global": 58},
    {"country": "Djibouti", "country_fr": "Djibouti", "lsci_2023": 26.2, "rank_africa": 5, "rank_global": 62},
    {"country": "Nigeria", "country_fr": "Nigéria", "lsci_2023": 24.8, "rank_africa": 6, "rank_global": 68},
    {"country": "Kenya", "country_fr": "Kenya", "lsci_2023": 22.5, "rank_africa": 7, "rank_global": 72},
    {"country": "Ghana", "country_fr": "Ghana", "lsci_2023": 21.2, "rank_africa": 8, "rank_global": 78},
    {"country": "Côte d'Ivoire", "country_fr": "Côte d'Ivoire", "lsci_2023": 20.5, "rank_africa": 9, "rank_global": 82},
    {"country": "Mauritius", "country_fr": "Maurice", "lsci_2023": 19.8, "rank_africa": 10, "rank_global": 85}
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_unctad_port_statistics() -> Dict:
    """Get UNCTAD port statistics for Africa"""
    return UNCTAD_PORT_STATISTICS

def get_unctad_trade_flows() -> Dict:
    """Get UNCTAD trade flow statistics"""
    return UNCTAD_TRADE_FLOWS

def get_unctad_lsci() -> List[Dict]:
    """Get UNCTAD Liner Shipping Connectivity Index for Africa"""
    return UNCTAD_LSCI_AFRICA

def get_all_unctad_data() -> Dict:
    """Get all UNCTAD data"""
    return {
        "port_statistics": UNCTAD_PORT_STATISTICS,
        "trade_flows": UNCTAD_TRADE_FLOWS,
        "liner_connectivity_index": UNCTAD_LSCI_AFRICA,
        "source": "UNCTAD",
        "year": 2023,
        "last_updated": "2023-12-15"
    }
