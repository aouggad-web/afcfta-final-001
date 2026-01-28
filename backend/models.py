"""
Pydantic models for ZLECAf API
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid


class CountryInfo(BaseModel):
    """Country information model"""
    code: str  # ISO3 (code principal)
    iso2: str = ""  # ISO2 (pour les drapeaux)
    iso3: str  # ISO3 
    name: str
    region: str
    wb_code: str
    population: int


class TariffCalculationRequest(BaseModel):
    """Request model for tariff calculation"""
    origin_country: str
    destination_country: str
    hs_code: str
    value: float


class TariffCalculationResponse(BaseModel):
    """Response model for tariff calculation"""
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
    # WARNING: Taux variables selon sous-positions
    rate_warning: Optional[Dict[str, Any]] = None  # Warning si taux différents par sous-position
    sub_positions_details: Optional[List[Dict[str, Any]]] = None  # Liste des sous-positions avec leurs taux
    # Règles d'origine
    rules_of_origin: Dict[str, Any]
    # Top producteurs africains
    top_african_producers: List[Dict[str, Any]]
    # Données économiques des pays
    origin_country_data: Dict[str, Any]
    destination_country_data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CountryEconomicProfile(BaseModel):
    """Economic profile for a country"""
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
