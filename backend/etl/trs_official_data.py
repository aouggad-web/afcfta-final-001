"""
TRS (Time Release Study) - Données Officielles WCO et Sources Vérifiées
=========================================================================
Expert Senior en Stratégie Maritime et Opérationnelle

Ce module contient UNIQUEMENT des données officielles vérifiées.
- Source WCO: World Customs Organization Time Release Studies
- Source UNCTAD: Review of Maritime Transport
- Source World Bank: Container Port Performance Index (CPPI)
- Sources Nationales: Autorités Portuaires, Ministères

RÈGLE ABSOLUE: Aucune estimation. Si pas de données → "NA"
Chaque donnée inclut: source, année, date de publication
"""

# Données TRS Officielles par Port (ISO_PORT_ID)
# Structure: dwell_time_days, source, year, methodology, publication_date

TRS_OFFICIAL_DATA = {
    # =============================================================================
    # MAROC
    # =============================================================================
    "MAR-TAN-001": {  # Tanger Med
        "container_dwell_time_days": 7.8,
        "source": "Beacon Port Congestion Report / Tanger Med Port Authority",
        "data_year": 2024,
        "publication_date": "2024-09",
        "methodology": "Port Authority Statistics",
        "notes": "Données septembre 2024. Port catégorie 0.5-4M TEU. Congestion Méditerranée Ouest.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 4,
        "cppi_year": 2023
    },
    "MAR-CAS-001": {  # Casablanca
        "container_dwell_time_days": 8.4,
        "source": "Aujourd'hui le Maroc / ANP Maroc",
        "data_year": 2023,
        "publication_date": "2024-01",
        "methodology": "Port Authority Annual Report",
        "notes": "Import containers. Export: ~9 jours. Amélioration vs 14 jours en 2007.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": 2023
    },
    "MAR-AGA-001": {  # Agadir
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS officielle disponible.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # ALGÉRIE
    # =============================================================================
    "DZA-ALG-001": {  # Alger
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    "DZA-ORA-001": {  # Oran
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    "DZA-BEJ-001": {  # Béjaïa
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # TUNISIE
    # =============================================================================
    "TUN-RAD-001": {  # Radès
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    "TUN-SFX-001": {  # Sfax
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # ÉGYPTE
    # =============================================================================
    "EGY-ALE-001": {  # Alexandrie
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    "EGY-PSD-001": {  # Port Saïd
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    "EGY-DAM-001": {  # Damiette
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # AFRIQUE DU SUD
    # =============================================================================
    "ZAF-DUR-001": {  # Durban
        "container_dwell_time_days": 2.7,
        "source": "Transnet Port Terminals Official Report",
        "data_year": 2024,
        "publication_date": "2024-Q4",
        "methodology": "Transnet Performance Metrics",
        "notes": "Pier 1 Import containers. Amélioration significative vs 21 jours précédemment.",
        "vessel_turnaround_hours": 83.2,
        "vessel_turnaround_source": "SAAFF Analysis 2023 (Pier 2)",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": 2023
    },
    "ZAF-CPT-001": {  # Cape Town
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Amélioration CPPI +237.9 points en 2024 vs 2023. Dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 405,
        "cppi_year": 2023
    },
    "ZAF-NGQ-001": {  # Ngqura
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS officielle disponible.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 404,
        "cppi_year": 2023
    },
    
    # =============================================================================
    # NAMIBIE - DONNÉES WCO OFFICIELLES
    # =============================================================================
    "NAM-WAL-001": {  # Walvis Bay
        "container_dwell_time_days": "NA",
        "source": "WCO / NAMRA Time Release Study Report",
        "data_year": 2023,
        "publication_date": "2023-12-01",
        "methodology": "WCO Time Release Study (Standard)",
        "notes": "Étude TRS officielle WCO. Mesure de 'entry inwards' à 'out of charge'. Goulots identifiés: usage limité ASYCUDA World, inspections hors-port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "wco_trs_published": True,
        "wco_report_url": "https://www.namra.org.na/documents/cms/uploaded/time-release-study-report--1-december-2023-9de0a050c1.pdf",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # KENYA
    # =============================================================================
    "KEN-MBA-001": {  # Mombasa
        "container_dwell_time_days": 3.5,
        "source": "Kenya Ports Authority (KPA) Official Statistics",
        "data_year": 2023,
        "publication_date": "2024-01",
        "methodology": "KPA Annual Performance Report",
        "notes": "Moyenne annuelle 2023. Amélioration de 3.9 jours (2022). Avril 2024: 2.73 jours.",
        "vessel_turnaround_hours": 64.1,
        "customs_clearance_hours": "NA",
        "import_cargo_dwell_hours_q1_2023": 86,
        "target_dwell_hours": 60,
        "cppi_rank": 335,
        "cppi_year": 2023
    },
    
    # =============================================================================
    # TANZANIE
    # =============================================================================
    "TZA-DAR-001": {  # Dar es Salaam
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "LSCI +50% depuis 2006. Améliorations clearance 2022. Dwell time officiel non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # NIGÉRIA - TRS WCO EN COURS
    # =============================================================================
    "NGA-TIN-001": {  # Tin Can Island
        "container_dwell_time_days": "NA",
        "source": "WCO - Time Release Study Launched",
        "data_year": 2024,
        "publication_date": "2024-02",
        "methodology": "WCO TRS (En cours)",
        "notes": "TRS lancée février 2024. Premier d'une série au Nigeria. Rapport attendu sous 6 mois.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "wco_trs_in_progress": True,
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    "NGA-APM-001": {  # Apapa
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # SÉNÉGAL
    # =============================================================================
    "SEN-DKR-001": {  # Dakar
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "1er port conteneurs Afrique subsaharienne CPPI 2024. Score +23 vs -82 en 2023. Dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 1,
        "cppi_region": "Sub-Saharan Africa",
        "cppi_year": 2024
    },
    
    # =============================================================================
    # CÔTE D'IVOIRE
    # =============================================================================
    "CIV-ABJ-001": {  # Abidjan
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Second terminal conteneurs opérationnel depuis 2022 (Côte d'Ivoire Terminal). Dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # CAMEROUN
    # =============================================================================
    "CMR-DLA-001": {  # Douala
        "free_time_days": 10,
        "container_dwell_time_days": "NA",
        "source": "Transit Fruits Eagle - Tarifs Surestaries 2024/2025",
        "data_year": 2024,
        "publication_date": "2024-12",
        "methodology": "Port Tariff Documentation",
        "notes": "Franchise 10 jours (incluant jour d'escale). Surestaries à partir J+11. Dwell time réel non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "lsci_improvement_2024": "+54%"
    },
    "CMR-KRI-001": {  # Kribi
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "LSCI +54% en 2024 (meilleure progression Afrique). Dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # DJIBOUTI
    # =============================================================================
    "DJI-DJI-001": {  # Djibouti
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # GHANA
    # =============================================================================
    "GHA-TEM-001": {  # Tema
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # TOGO
    # =============================================================================
    "TGO-LOM-001": {  # Lomé
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # BÉNIN
    # =============================================================================
    "BEN-COT-001": {  # Cotonou
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # LIBYE
    # =============================================================================
    "LBY-TRI-001": {  # Tripoli
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # MOZAMBIQUE
    # =============================================================================
    "MOZ-MPM-001": {  # Maputo
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # ANGOLA
    # =============================================================================
    "AGO-LUA-001": {  # Luanda
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # CONGO
    # =============================================================================
    "COG-PNR-001": {  # Pointe-Noire
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # GABON
    # =============================================================================
    "GAB-LBV-001": {  # Libreville/Owendo
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # MAURICE
    # =============================================================================
    "MUS-PLO-001": {  # Port Louis
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
    
    # =============================================================================
    # MADAGASCAR
    # =============================================================================
    "MDG-TMM-001": {  # Toamasina
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS WCO publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA"
    },
}

# Données LPI World Bank 2023 par pays
LPI_2023_DATA = {
    "ZAF": {"overall": 3.7, "customs": 3.3, "timeliness": 3.8, "rank": 19},
    "RWA": {"overall": 2.8, "customs": 2.5, "timeliness": 3.1, "rank": 73},
    "NGA": {"overall": 2.6, "customs": 2.4, "timeliness": 3.1, "rank": 88},
    "GMB": {"overall": 2.3, "customs": 1.8, "timeliness": "NA", "rank": 123},
    "ZWE": {"import_dwell_mean_days": 12.8, "import_dwell_median_days": 11.8},
}

# Benchmarks globaux UNCTAD 2023
GLOBAL_BENCHMARKS = {
    "container_dwell_time_days_global_median_h1_2023": 0.7,
    "container_dwell_time_days_global_median_h2_2023": 1.1,
    "container_dwell_time_days_africa_avg_2023": 2.6,
    "container_handling_time_seconds_2023": 36,
    "source": "UNCTAD Review of Maritime Transport 2024"
}


def get_trs_data(port_id: str) -> dict:
    """Récupère les données TRS officielles pour un port."""
    return TRS_OFFICIAL_DATA.get(port_id, {
        "container_dwell_time_days": "NA",
        "source": "NA",
        "data_year": "NA",
        "notes": "Aucune donnée TRS officielle disponible pour ce port."
    })


def get_lpi_data(country_iso: str) -> dict:
    """Récupère les données LPI 2023 pour un pays."""
    return LPI_2023_DATA.get(country_iso, {})
