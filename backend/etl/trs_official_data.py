"""
TRS (Time Release Study) - Données Multi-Sources
=================================================
Expert Senior en Stratégie Maritime et Opérationnelle

Ce module contient:
1. DONNÉES OFFICIELLES WCO/TRS (priorité maximale)
2. DONNÉES DE SOURCES FIABLES DE 1ER PLAN (avec avertissement)
   - Autorités portuaires nationales
   - Études Time Release Study nationales
   - Banque Mondiale CPPI
   - UNCTAD Review of Maritime Transport
   - Rapports industriels vérifiés

RÈGLE: Chaque donnée inclut source, année, et niveau de fiabilité
"""

from typing import Dict, Any

# =============================================================================
# NIVEAUX DE FIABILITÉ DES SOURCES
# =============================================================================
SOURCE_RELIABILITY = {
    "OFFICIAL_WCO_TRS": {
        "level": 1,
        "label": "Officiel WCO",
        "description": "Étude Time Release Study officielle de l'Organisation Mondiale des Douanes",
        "warning": None
    },
    "NATIONAL_TRS": {
        "level": 2,
        "label": "TRS National",
        "description": "Étude Time Release Study conduite par l'autorité douanière nationale",
        "warning": None
    },
    "PORT_AUTHORITY": {
        "level": 2,
        "label": "Autorité Portuaire",
        "description": "Données officielles de l'autorité portuaire nationale",
        "warning": None
    },
    "WORLD_BANK_CPPI": {
        "level": 2,
        "label": "World Bank CPPI",
        "description": "Container Port Performance Index - Banque Mondiale",
        "warning": None
    },
    "INDUSTRY_REPORT": {
        "level": 3,
        "label": "Rapport Industriel",
        "description": "Rapport de source industrielle vérifiée (shipping lines, terminaux)",
        "warning": "⚠️ Source non-officielle: Données provenant de rapports industriels. À utiliser comme indication."
    },
    "AFDB_ESTIMATE": {
        "level": 3,
        "label": "Estimation AfDB",
        "description": "Estimation de la Banque Africaine de Développement",
        "warning": "⚠️ Estimation régionale: Moyenne indicative, non spécifique au port."
    },
    "ACADEMIC_STUDY": {
        "level": 3,
        "label": "Étude Académique",
        "description": "Publication académique ou étude de recherche",
        "warning": "⚠️ Source académique: Données de recherche, vérification indépendante recommandée."
    },
    "NO_DATA": {
        "level": 99,
        "label": "NA",
        "description": "Aucune donnée disponible",
        "warning": None
    }
}

# =============================================================================
# DONNÉES TRS PAR PORT
# =============================================================================
TRS_OFFICIAL_DATA: Dict[str, Dict[str, Any]] = {
    
    # =========================================================================
    # MAROC
    # =========================================================================
    "MAR-TAN-001": {  # Tanger Med
        "container_dwell_time_days": 7.8,
        "source": "Beacon Port Congestion Report / Tanger Med Port Authority",
        "source_type": "INDUSTRY_REPORT",
        "data_year": 2024,
        "publication_date": "2024-09",
        "methodology": "Port Authority Statistics / Industry Analysis",
        "notes": "Données septembre 2024. Port catégorie 0.5-4M TEU. Rang CPPI #4 mondial (2023).",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 4,
        "cppi_year": 2023,
        "teu_throughput_2024": 10241392,
        "warning": "⚠️ Donnée de source industrielle (Beacon). Non issue d'une étude TRS officielle WCO."
    },
    "MAR-CAS-001": {  # Casablanca
        "container_dwell_time_days": 8.4,
        "source": "Aujourd'hui le Maroc / ANP Maroc",
        "source_type": "PORT_AUTHORITY",
        "data_year": 2023,
        "publication_date": "2024-01",
        "methodology": "Port Authority Annual Report",
        "notes": "Import containers. Export: ~9 jours. Amélioration significative vs 14 jours en 2007.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": 2023,
        "warning": None
    },
    "MAR-AGD-001": {  # Agadir
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS officielle disponible.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # ALGÉRIE
    # =========================================================================
    "DZA-ALG-001": {  # Alger
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS publiée. Estimation régionale AfDB: 20 jours (moyenne Afrique).",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "regional_estimate_days": 20,
        "regional_estimate_source": "African Development Bank",
        "warning": None
    },
    "DZA-ORA-001": {  # Oran
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    "DZA-BEJ-001": {  # Béjaïa
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # ÉGYPTE - DONNÉES TRS OFFICIELLES NATIONALES (2024)
    # =========================================================================
    "EGY-ALE-001": {  # Alexandrie
        "container_dwell_time_days": 8.64,
        "source": "Egypt Customs Authority - Time Release Study #2",
        "source_type": "NATIONAL_TRS",
        "data_year": 2024,
        "publication_date": "2024-04",
        "methodology": "National Time Release Study (21-27 April 2024)",
        "notes": "Réduction de 46.1% vs TRS#1 (2021: 16.08 jours). Amélioration significative.",
        "trs_2021_baseline_days": 16.08,
        "improvement_percent": 46.1,
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "anchor_to_unload_days": 1.04,
        "unloading_duration_hours": 11.35,
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "source_url": "https://assets.mof.gov.eg/files/d06136d0-b7aa-11ef-9d21-798cef5fccf4.pdf",
        "warning": None
    },
    "EGY-DAM-001": {  # Damiette
        "container_dwell_time_days": 8.09,
        "source": "Egypt Customs Authority - Time Release Study #2",
        "source_type": "NATIONAL_TRS",
        "data_year": 2024,
        "publication_date": "2024-04",
        "methodology": "National Time Release Study (21-27 April 2024)",
        "notes": "Port de Damiette inclus dans l'étude TRS nationale égyptienne.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "source_url": "https://assets.mof.gov.eg/files/d06136d0-b7aa-11ef-9d21-798cef5fccf4.pdf",
        "warning": None
    },
    "EGY-PSD-001": {  # Port Saïd
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Non inclus dans TRS#2 Egypt (2024). Hub de transbordement principalement.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    "EGY-DEK-001": {  # El Dekheila
        "container_dwell_time_days": 9.40,
        "source": "Egypt Customs Authority - Time Release Study #2",
        "source_type": "NATIONAL_TRS",
        "data_year": 2024,
        "publication_date": "2024-04",
        "methodology": "National Time Release Study (21-27 April 2024)",
        "notes": "Partie du complexe portuaire d'Alexandrie.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "source_url": "https://assets.mof.gov.eg/files/d06136d0-b7aa-11ef-9d21-798cef5fccf4.pdf",
        "warning": None
    },
    
    # =========================================================================
    # TUNISIE
    # =========================================================================
    "TUN-RAD-001": {  # Radès
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    "TUN-SFX-001": {  # Sfax
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune étude TRS publiée pour ce port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # LIBYE
    # =========================================================================
    "LBY-TRP-001": {  # Tripoli
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée disponible. Contexte sécuritaire difficile.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # AFRIQUE DU SUD
    # =========================================================================
    "ZAF-DUR-001": {  # Durban
        "container_dwell_time_days": 2.7,
        "source": "Transnet Port Terminals Official Report",
        "source_type": "PORT_AUTHORITY",
        "data_year": 2024,
        "publication_date": "2024-Q4",
        "methodology": "Transnet Performance Metrics",
        "notes": "Pier 1 Import containers. Amélioration majeure vs 21 jours précédemment. Pier 2: 83.2h turnaround.",
        "vessel_turnaround_hours": 83.2,
        "vessel_turnaround_source": "SAAFF Analysis 2023 (Pier 2)",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": 2023,
        "warning": None
    },
    "ZAF-CPT-001": {  # Cape Town
        "container_dwell_time_days": "NA",
        "source": "World Bank CPPI 2024",
        "source_type": "WORLD_BANK_CPPI",
        "data_year": 2024,
        "publication_date": "2024",
        "methodology": "World Bank Container Port Performance Index",
        "notes": "Amélioration CPPI +237.9 points en 2024 vs 2023. Dwell time cargo non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 405,
        "cppi_improvement_points": 237.9,
        "cppi_year": 2024,
        "warning": None
    },
    "ZAF-NGQ-001": {  # Ngqura
        "container_dwell_time_days": "NA",
        "source": "World Bank CPPI 2023",
        "source_type": "WORLD_BANK_CPPI",
        "data_year": 2023,
        "publication_date": "2023",
        "methodology": "World Bank Container Port Performance Index",
        "notes": "Port moderne. CPPI rang disponible, dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 404,
        "cppi_year": 2023,
        "warning": None
    },
    
    # =========================================================================
    # NAMIBIE - DONNÉES WCO OFFICIELLES
    # =========================================================================
    "NAM-WAL-001": {  # Walvis Bay
        "container_dwell_time_days": "NA",
        "source": "WCO / NAMRA Time Release Study Report",
        "source_type": "OFFICIAL_WCO_TRS",
        "data_year": 2023,
        "publication_date": "2023-12-01",
        "methodology": "WCO Time Release Study (Standard)",
        "notes": "Étude TRS officielle WCO publiée. Mesure 'entry inwards' à 'out of charge'. Goulots: usage limité ASYCUDA World, inspections hors-port.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "wco_trs_published": True,
        "wco_report_url": "https://www.namra.org.na/documents/cms/uploaded/time-release-study-report--1-december-2023-9de0a050c1.pdf",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # KENYA
    # =========================================================================
    "KEN-MBA-001": {  # Mombasa
        "container_dwell_time_days": 3.5,
        "source": "Kenya Ports Authority (KPA) Official Statistics",
        "source_type": "PORT_AUTHORITY",
        "data_year": 2023,
        "publication_date": "2024-01",
        "methodology": "KPA Annual Performance Report",
        "notes": "Moyenne 2023. Amélioration vs 3.9 jours (2022). Avril 2024: record de 2.73 jours. Cible: 60 heures.",
        "vessel_turnaround_hours": 64.1,
        "customs_clearance_hours": "NA",
        "import_cargo_dwell_hours_q1_2023": 86,
        "target_dwell_hours": 60,
        "best_performance_days": 2.73,
        "best_performance_date": "2024-04",
        "cppi_rank": 335,
        "cppi_year": 2023,
        "warning": None
    },
    
    # =========================================================================
    # TANZANIE
    # =========================================================================
    "TZA-DAR-001": {  # Dar es Salaam
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "LSCI +50% depuis 2006. Améliorations clearance 2022. Dwell time officiel non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # NIGÉRIA
    # =========================================================================
    "NGA-TIN-001": {  # Tin Can Island
        "container_dwell_time_days": "NA",
        "source": "WCO - Time Release Study Launched",
        "source_type": "OFFICIAL_WCO_TRS",
        "data_year": 2024,
        "publication_date": "2024-02",
        "methodology": "WCO TRS (En cours)",
        "notes": "TRS lancée février 2024. Premier d'une série au Nigeria. Rapport final attendu.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "wco_trs_in_progress": True,
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    "NGA-LAG-001": {  # Apapa Lagos
        "container_dwell_time_days": 16.73,
        "source": "Academic Study - Port Reforms Analysis (2007-2021)",
        "source_type": "ACADEMIC_STUDY",
        "data_year": 2021,
        "publication_date": "2024-03",
        "methodology": "Post-reform performance analysis",
        "notes": "Délai moyen post-réforme 2007. 313.82% au-dessus du benchmark mondial (4 jours). Moyenne nigériane: 20-28 jours.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "benchmark_global_days": 4,
        "above_benchmark_percent": 313.82,
        "source_url": "https://www.gjournals.org/2024/03/13/022324028-mbachu-et-al/",
        "warning": "⚠️ Source académique (2021). Données de recherche post-réformes. Situation peut avoir évolué."
    },
    "NGA-LEK-001": {  # Lekki Deep Sea Port
        "container_dwell_time_days": 16,
        "source": "Lekki Port Authority / Maritime Today Online",
        "source_type": "PORT_AUTHORITY",
        "data_year": 2025,
        "publication_date": "2025-06",
        "methodology": "Port Operations Report",
        "notes": "Port opérationnel depuis 2023. Truck turnaround: <1h25. Vessel turnaround: 48h. Objectif: réduction via digitalisation.",
        "vessel_turnaround_hours": 48,
        "truck_turnaround_minutes": 85,
        "truck_park_dwell_days": 10,
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "teu_throughput_2024": 54000,
        "teu_projection_2025": 500000,
        "warning": "⚠️ Port nouveau (2023). Données préliminaires. Performance en amélioration continue."
    },
    
    # =========================================================================
    # CÔTE D'IVOIRE
    # =========================================================================
    "CIV-ABJ-001": {  # Abidjan
        "container_dwell_time_days": 3.54,
        "source": "Port Autonome d'Abidjan - PAA Infos Magazine",
        "source_type": "PORT_AUTHORITY",
        "data_year": 2023,
        "publication_date": "2023-08",
        "methodology": "Port Authority Statistics",
        "notes": "Moyenne 2023. Ancrage amélioré: 0.58 jours (vs 0.88 en Q1 2022). Cargo local: 3-5 jours. Transit: 5 jours.",
        "anchorage_wait_days_2023": 0.58,
        "anchorage_wait_days_2022_q1": 0.88,
        "local_cargo_dwell_days": "3-5",
        "transit_cargo_dwell_days": 5,
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "source_url": "https://www.portabidjan.ci/sites/default/files/paa_infos_magazine_ndeg112_-_juillet_et_aout_2023.pdf",
        "warning": None
    },
    
    # =========================================================================
    # SÉNÉGAL
    # =========================================================================
    "SEN-DKR-001": {  # Dakar
        "container_dwell_time_days": 7,
        "source": "PPIAF / World Bank Analysis (Historical)",
        "source_type": "WORLD_BANK_CPPI",
        "data_year": 2018,
        "publication_date": "2020-12",
        "methodology": "Shadow Rating Simulation",
        "notes": "Donnée 2018. #1 CPPI Sub-Saharan Africa 2024 (+23 points). Amélioration significative probable.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 1,
        "cppi_region": "Sub-Saharan Africa",
        "cppi_score_improvement": 104.7,
        "cppi_year": 2024,
        "monthly_throughput_teu_2024": 77680,
        "warning": "⚠️ Dwell time daté (2018). Performance CPPI 2024 indique amélioration majeure. Données récentes non publiées."
    },
    
    # =========================================================================
    # GHANA
    # =========================================================================
    "GHA-TEM-001": {  # Tema
        "container_dwell_time_days": "6-12",
        "source": "Ghana News / GPHA Reports",
        "source_type": "INDUSTRY_REPORT",
        "data_year": 2024,
        "publication_date": "2024",
        "methodology": "Industry Analysis",
        "notes": "Plage estimée. Benchmark global: 3-4 jours. ICUMS permet clearance en heures si docs complets. 95% du trafic Ghana.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "teu_throughput_2024": 1668688,
        "percent_ghana_traffic": 95,
        "warning": "⚠️ Plage indicative (6-12 jours). Non issue d'étude TRS officielle."
    },
    "GHA-TKD-001": {  # Takoradi
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Port principalement vrac. Aucune donnée TRS conteneurs publiée.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # TOGO
    # =========================================================================
    "TGO-LOM-001": {  # Lomé
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Hub régional majeur. Dwell time non publié officiellement.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # BÉNIN
    # =========================================================================
    "BEN-COT-001": {  # Cotonou
        "container_dwell_time_days": "NA",
        "source": "World Bank CPPI 2023",
        "source_type": "WORLD_BANK_CPPI",
        "data_year": 2023,
        "publication_date": "2023",
        "methodology": "World Bank Container Port Performance Index",
        "notes": "Rang CPPI 401/405. Performance vessel time in port. Cargo dwell non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": 401,
        "cppi_year": 2023,
        "warning": None
    },
    
    # =========================================================================
    # CAMEROUN
    # =========================================================================
    "CMR-DLA-001": {  # Douala
        "container_dwell_time_days": "NA",
        "source": "Transit Fruits Eagle - Tarifs Surestaries",
        "source_type": "INDUSTRY_REPORT",
        "data_year": 2024,
        "publication_date": "2024-12",
        "methodology": "Port Tariff Documentation",
        "notes": "Franchise 10 jours (incluant jour d'escale). Surestaries à partir J+11. LSCI +54% en 2024.",
        "free_time_days": 10,
        "demurrage_start_day": 11,
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "lsci_improvement_2024_percent": 54,
        "warning": "⚠️ Franchise (free time) ≠ Dwell time réel. Donnée indicative uniquement."
    },
    "CMR-KRI-001": {  # Kribi
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Port moderne en eau profonde. LSCI +54% en 2024. Dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # DJIBOUTI
    # =========================================================================
    "DJI-DJI-001": {  # Djibouti / Doraleh
        "container_dwell_time_days": "NA",
        "source": "SGTD Terminal Report",
        "source_type": "PORT_AUTHORITY",
        "data_year": 2024,
        "publication_date": "2024-11",
        "methodology": "Terminal Operator Statistics",
        "notes": "Record 1.24M TEU en 2024. CPPI controversé (379e vs 26e en 2022). Dwell cargo non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "quay_productivity_moves_per_hour": 120,
        "utilization_percent": 40,
        "teu_throughput_2024": 1236769,
        "cppi_rank": 379,
        "cppi_year": 2023,
        "cppi_2022_rank": 26,
        "warning": None
    },
    
    # =========================================================================
    # GABON
    # =========================================================================
    "GAB-LBV-001": {  # Owendo/Libreville
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS publiée.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # CONGO
    # =========================================================================
    "COG-PNR-001": {  # Pointe-Noire
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS publiée.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # ANGOLA
    # =========================================================================
    "AGO-LUA-001": {  # Luanda
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS publiée.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # MOZAMBIQUE
    # =========================================================================
    "MOZ-MPM-001": {  # Maputo
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS publiée.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # MAURICE
    # =========================================================================
    "MUS-PLO-001": {  # Port Louis
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Hub de transbordement. Dwell time non publié.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
    
    # =========================================================================
    # MADAGASCAR
    # =========================================================================
    "MDG-TMM-001": {  # Toamasina
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "publication_date": "NA",
        "methodology": "NA",
        "notes": "Aucune donnée TRS publiée.",
        "vessel_turnaround_hours": "NA",
        "customs_clearance_hours": "NA",
        "cppi_rank": "NA",
        "cppi_year": "NA",
        "warning": None
    },
}

# =============================================================================
# DONNÉES LPI WORLD BANK 2023
# =============================================================================
LPI_2023_DATA = {
    "ZAF": {"overall": 3.7, "customs": 3.3, "timeliness": 3.8, "rank": 19},
    "CIV": {"overall": 2.8, "customs": 2.4, "timeliness": 3.2, "rank": 79},
    "RWA": {"overall": 2.8, "customs": 2.5, "timeliness": 3.1, "rank": 73},
    "KEN": {"overall": 2.8, "customs": 2.6, "timeliness": 3.3, "rank": 68},
    "EGY": {"overall": 2.8, "customs": 2.5, "timeliness": 3.0, "rank": 77},
    "NGA": {"overall": 2.6, "customs": 2.4, "timeliness": 3.1, "rank": 88},
    "GHA": {"overall": 2.6, "customs": 2.3, "timeliness": 3.0, "rank": 95},
    "SEN": {"overall": 2.6, "customs": 2.4, "timeliness": 3.0, "rank": 92},
    "TZA": {"overall": 2.5, "customs": 2.3, "timeliness": 2.9, "rank": 100},
    "CMR": {"overall": 2.4, "customs": 2.1, "timeliness": 2.8, "rank": 115},
    "MAR": {"overall": 2.5, "customs": 2.3, "timeliness": 2.8, "rank": 106},
    "DZA": {"overall": 2.4, "customs": 2.2, "timeliness": 2.7, "rank": 117},
    "TUN": {"overall": 2.4, "customs": 2.2, "timeliness": 2.8, "rank": 112},
    "GMB": {"overall": 2.3, "customs": 1.8, "timeliness": "NA", "rank": 123},
    "ZWE": {"import_dwell_mean_days": 12.8, "import_dwell_median_days": 11.8},
}

# =============================================================================
# BENCHMARKS GLOBAUX
# =============================================================================
GLOBAL_BENCHMARKS = {
    "container_dwell_time_days_global_median_h1_2023": 0.7,
    "container_dwell_time_days_global_median_h2_2023": 1.1,
    "container_dwell_time_days_africa_avg": 20,
    "container_dwell_time_days_africa_avg_source": "African Development Bank",
    "container_dwell_time_days_afdb_note": "Moyenne continentale. Performance très variable selon les ports.",
    "container_handling_time_seconds_2023": 36,
    "source": "UNCTAD Review of Maritime Transport 2024 / African Development Bank"
}

# =============================================================================
# NOTE IMPORTANTE SUR LA COUVERTURE TRS
# =============================================================================
TRS_COVERAGE_NOTE = """
📊 NOTE IMPORTANTE SUR LA COUVERTURE DES DONNÉES TRS

La couverture des données TRS officielles pour les ports africains est limitée (~15-20% des ports majeurs).
Cela reflète la réalité du secteur:
• Peu d'études TRS WCO ont été conduites et publiées pour l'Afrique
• Les autorités portuaires ne publient pas systématiquement leurs données de performance
• Les méthodologies de mesure varient selon les pays

Sources utilisées (par ordre de fiabilité):
1. Études TRS WCO officielles
2. Études TRS nationales (ex: Egypt Customs Authority)
3. Rapports des autorités portuaires (ex: KPA, Transnet, PAA)
4. World Bank CPPI (vessel time, non cargo dwell)
5. Rapports industriels vérifiés

Pour les ports marqués "NA": Aucune donnée fiable disponible.
Les estimations régionales (ex: AfDB 20 jours) sont des moyennes continentales à interpréter avec précaution.
"""


def get_trs_data(port_id: str) -> dict:
    """Récupère les données TRS pour un port."""
    return TRS_OFFICIAL_DATA.get(port_id, {
        "container_dwell_time_days": "NA",
        "source": "NA",
        "source_type": "NO_DATA",
        "data_year": "NA",
        "notes": "Aucune donnée TRS disponible pour ce port."
    })


def get_source_reliability(source_type: str) -> dict:
    """Récupère les informations de fiabilité d'une source."""
    return SOURCE_RELIABILITY.get(source_type, SOURCE_RELIABILITY["NO_DATA"])


def get_lpi_data(country_iso: str) -> dict:
    """Récupère les données LPI 2023 pour un pays."""
    return LPI_2023_DATA.get(country_iso, {})
