"""
UN Comtrade Trade Data Service
Fetches real trade data from UN Comtrade API for African countries
Supports import/export analysis at HS6 level

API Documentation: https://comtradedeveloper.un.org
"""
import httpx
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# UN Comtrade API Configuration
COMTRADE_BASE_URL = "https://comtradeapi.un.org/data/v1/get/C/A"
COMTRADE_BULK_URL = "https://comtradeapi.un.org/bulk/v1/get/C/A"

# African Countries ISO3 codes for filtering
AFRICAN_COUNTRIES_ISO3 = [
    "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CPV", "CMR", "CAF", "TCD",
    "COM", "COG", "COD", "CIV", "DJI", "EGY", "GNQ", "ERI", "SWZ", "ETH",
    "GAB", "GMB", "GHA", "GIN", "GNB", "KEN", "LSO", "LBR", "LBY", "MDG",
    "MWI", "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA", "RWA",
    "STP", "SEN", "SYC", "SLE", "SOM", "ZAF", "SSD", "SDN", "TZA", "TGO",
    "TUN", "UGA", "ZMB", "ZWE"
]

# M49 codes for African countries (UN numeric codes)
AFRICAN_COUNTRIES_M49 = {
    "DZA": "012", "AGO": "024", "BEN": "204", "BWA": "072", "BFA": "854",
    "BDI": "108", "CPV": "132", "CMR": "120", "CAF": "140", "TCD": "148",
    "COM": "174", "COG": "178", "COD": "180", "CIV": "384", "DJI": "262",
    "EGY": "818", "GNQ": "226", "ERI": "232", "SWZ": "748", "ETH": "231",
    "GAB": "266", "GMB": "270", "GHA": "288", "GIN": "324", "GNB": "624",
    "KEN": "404", "LSO": "426", "LBR": "430", "LBY": "434", "MDG": "450",
    "MWI": "454", "MLI": "466", "MRT": "478", "MUS": "480", "MAR": "504",
    "MOZ": "508", "NAM": "516", "NER": "562", "NGA": "566", "RWA": "646",
    "STP": "678", "SEN": "686", "SYC": "690", "SLE": "694", "SOM": "706",
    "ZAF": "710", "SSD": "728", "SDN": "736", "TZA": "834", "TGO": "768",
    "TUN": "788", "UGA": "800", "ZMB": "894", "ZWE": "716"
}

# Reverse mapping
M49_TO_ISO3 = {v: k for k, v in AFRICAN_COUNTRIES_M49.items()}

# Country names
COUNTRY_NAMES = {
    "DZA": {"fr": "Algérie", "en": "Algeria"},
    "AGO": {"fr": "Angola", "en": "Angola"},
    "BEN": {"fr": "Bénin", "en": "Benin"},
    "BWA": {"fr": "Botswana", "en": "Botswana"},
    "BFA": {"fr": "Burkina Faso", "en": "Burkina Faso"},
    "BDI": {"fr": "Burundi", "en": "Burundi"},
    "CPV": {"fr": "Cap-Vert", "en": "Cape Verde"},
    "CMR": {"fr": "Cameroun", "en": "Cameroon"},
    "CAF": {"fr": "Centrafrique", "en": "Central African Republic"},
    "TCD": {"fr": "Tchad", "en": "Chad"},
    "COM": {"fr": "Comores", "en": "Comoros"},
    "COG": {"fr": "Congo", "en": "Republic of the Congo"},
    "COD": {"fr": "RD Congo", "en": "DR Congo"},
    "CIV": {"fr": "Côte d'Ivoire", "en": "Ivory Coast"},
    "DJI": {"fr": "Djibouti", "en": "Djibouti"},
    "EGY": {"fr": "Égypte", "en": "Egypt"},
    "GNQ": {"fr": "Guinée Équatoriale", "en": "Equatorial Guinea"},
    "ERI": {"fr": "Érythrée", "en": "Eritrea"},
    "SWZ": {"fr": "Eswatini", "en": "Eswatini"},
    "ETH": {"fr": "Éthiopie", "en": "Ethiopia"},
    "GAB": {"fr": "Gabon", "en": "Gabon"},
    "GMB": {"fr": "Gambie", "en": "Gambia"},
    "GHA": {"fr": "Ghana", "en": "Ghana"},
    "GIN": {"fr": "Guinée", "en": "Guinea"},
    "GNB": {"fr": "Guinée-Bissau", "en": "Guinea-Bissau"},
    "KEN": {"fr": "Kenya", "en": "Kenya"},
    "LSO": {"fr": "Lesotho", "en": "Lesotho"},
    "LBR": {"fr": "Libéria", "en": "Liberia"},
    "LBY": {"fr": "Libye", "en": "Libya"},
    "MDG": {"fr": "Madagascar", "en": "Madagascar"},
    "MWI": {"fr": "Malawi", "en": "Malawi"},
    "MLI": {"fr": "Mali", "en": "Mali"},
    "MRT": {"fr": "Mauritanie", "en": "Mauritania"},
    "MUS": {"fr": "Maurice", "en": "Mauritius"},
    "MAR": {"fr": "Maroc", "en": "Morocco"},
    "MOZ": {"fr": "Mozambique", "en": "Mozambique"},
    "NAM": {"fr": "Namibie", "en": "Namibia"},
    "NER": {"fr": "Niger", "en": "Niger"},
    "NGA": {"fr": "Nigeria", "en": "Nigeria"},
    "RWA": {"fr": "Rwanda", "en": "Rwanda"},
    "STP": {"fr": "São Tomé-et-Príncipe", "en": "São Tomé and Príncipe"},
    "SEN": {"fr": "Sénégal", "en": "Senegal"},
    "SYC": {"fr": "Seychelles", "en": "Seychelles"},
    "SLE": {"fr": "Sierra Leone", "en": "Sierra Leone"},
    "SOM": {"fr": "Somalie", "en": "Somalia"},
    "ZAF": {"fr": "Afrique du Sud", "en": "South Africa"},
    "SSD": {"fr": "Soudan du Sud", "en": "South Sudan"},
    "SDN": {"fr": "Soudan", "en": "Sudan"},
    "TZA": {"fr": "Tanzanie", "en": "Tanzania"},
    "TGO": {"fr": "Togo", "en": "Togo"},
    "TUN": {"fr": "Tunisie", "en": "Tunisia"},
    "UGA": {"fr": "Ouganda", "en": "Uganda"},
    "ZMB": {"fr": "Zambie", "en": "Zambia"},
    "ZWE": {"fr": "Zimbabwe", "en": "Zimbabwe"}
}


class ComtradeService:
    """
    Service for fetching trade data from UN Comtrade API
    """
    
    def __init__(self, subscription_key: Optional[str] = None):
        """
        Initialize the Comtrade service
        
        Args:
            subscription_key: Optional API key for premium access
        """
        self.subscription_key = subscription_key
        self.base_url = COMTRADE_BASE_URL
        self.timeout = 60.0
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour cache
    
    def _get_cache_key(self, **params) -> str:
        """Generate cache key from parameters"""
        return f"comtrade_{hash(frozenset(params.items()))}"
    
    async def _make_request(self, params: Dict) -> Dict:
        """
        Make request to Comtrade API
        
        Note: Without subscription key, we use the preview endpoint
        which is limited but free
        """
        try:
            headers = {}
            if self.subscription_key:
                headers["Ocp-Apim-Subscription-Key"] = self.subscription_key
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 403:
                    logger.warning("Comtrade API access denied - using fallback data")
                    return {"error": "API access denied", "data": []}
                else:
                    logger.error(f"Comtrade API error: {response.status_code}")
                    return {"error": f"API error {response.status_code}", "data": []}
                    
        except Exception as e:
            logger.error(f"Comtrade request failed: {str(e)}")
            return {"error": str(e), "data": []}
    
    async def get_country_imports(
        self,
        reporter_iso3: str,
        year: int = 2022,
        hs_code: Optional[str] = None,
        partner: str = "0"  # 0 = World
    ) -> Dict:
        """
        Get imports for a specific African country
        
        Args:
            reporter_iso3: ISO3 code of the importing country
            year: Year of trade data
            hs_code: Optional HS code filter (2, 4, or 6 digits)
            partner: Partner country M49 code (0 = World)
        
        Returns:
            Dict with import data
        """
        reporter_m49 = AFRICAN_COUNTRIES_M49.get(reporter_iso3.upper())
        if not reporter_m49:
            return {"error": f"Country {reporter_iso3} not found", "data": []}
        
        params = {
            "reporterCode": reporter_m49,
            "period": str(year),
            "flowCode": "M",  # M = Imports
            "partnerCode": partner,
            "cmdCode": hs_code or "TOTAL",
            "partner2Code": "0",
            "customsCode": "C00",
            "motCode": "0"
        }
        
        return await self._make_request(params)
    
    async def get_country_exports(
        self,
        reporter_iso3: str,
        year: int = 2022,
        hs_code: Optional[str] = None,
        partner: str = "0"
    ) -> Dict:
        """
        Get exports for a specific African country
        """
        reporter_m49 = AFRICAN_COUNTRIES_M49.get(reporter_iso3.upper())
        if not reporter_m49:
            return {"error": f"Country {reporter_iso3} not found", "data": []}
        
        params = {
            "reporterCode": reporter_m49,
            "period": str(year),
            "flowCode": "X",  # X = Exports
            "partnerCode": partner,
            "cmdCode": hs_code or "TOTAL",
            "partner2Code": "0",
            "customsCode": "C00",
            "motCode": "0"
        }
        
        return await self._make_request(params)
    
    async def get_imports_from_outside_africa(
        self,
        reporter_iso3: str,
        year: int = 2022,
        hs_chapter: Optional[str] = None
    ) -> Dict:
        """
        Get imports that come from outside Africa
        This is key for identifying substitution opportunities
        """
        # First get total imports
        total_imports = await self.get_country_imports(
            reporter_iso3, year, hs_chapter
        )
        
        # Then get imports from African countries
        african_m49_codes = ",".join(AFRICAN_COUNTRIES_M49.values())
        african_imports = await self.get_country_imports(
            reporter_iso3, year, hs_chapter, african_m49_codes
        )
        
        # Calculate non-African imports
        # This would need proper data processing in production
        return {
            "reporter": reporter_iso3,
            "year": year,
            "total_imports": total_imports,
            "african_imports": african_imports,
            "non_african_imports": []  # Calculated difference
        }


# Simulated trade data for development (based on real patterns)
# This will be replaced with real API data when subscription is available
SIMULATED_TRADE_DATA = {
    # Top imports from outside Africa for key African countries
    "imports_from_outside": {
        "NGA": [  # Nigeria
            {"hs_code": "271019", "product": "Huiles de pétrole raffinées", "value": 12500000000, "source_region": "Europe/Asia"},
            {"hs_code": "100199", "product": "Blé et méteil", "value": 3200000000, "source_region": "North America/Europe"},
            {"hs_code": "870323", "product": "Véhicules automobiles", "value": 2800000000, "source_region": "Asia/Europe"},
            {"hs_code": "300490", "product": "Médicaments", "value": 1900000000, "source_region": "Europe/India"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "value": 1200000000, "source_region": "China"},
            {"hs_code": "730890", "product": "Constructions en fer/acier", "value": 980000000, "source_region": "China"},
            {"hs_code": "848180", "product": "Robinetterie", "value": 750000000, "source_region": "China/Europe"},
            {"hs_code": "392190", "product": "Plaques en plastique", "value": 620000000, "source_region": "China"},
        ],
        "EGY": [  # Egypt
            {"hs_code": "100199", "product": "Blé et méteil", "value": 4500000000, "source_region": "Russia/Ukraine"},
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "value": 3800000000, "source_region": "Middle East"},
            {"hs_code": "120190", "product": "Fèves de soja", "value": 1800000000, "source_region": "Americas"},
            {"hs_code": "720839", "product": "Produits laminés plats en fer", "value": 1500000000, "source_region": "Europe/Asia"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "value": 890000000, "source_region": "China"},
        ],
        "ZAF": [  # South Africa
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "value": 15000000000, "source_region": "Middle East/Nigeria"},
            {"hs_code": "870323", "product": "Véhicules automobiles", "value": 3200000000, "source_region": "Europe/Asia"},
            {"hs_code": "854230", "product": "Circuits intégrés", "value": 2100000000, "source_region": "Asia"},
            {"hs_code": "300490", "product": "Médicaments", "value": 1800000000, "source_region": "Europe/India"},
            {"hs_code": "848180", "product": "Robinetterie", "value": 950000000, "source_region": "China/Europe"},
        ],
        "KEN": [  # Kenya
            {"hs_code": "271019", "product": "Huiles de pétrole raffinées", "value": 3500000000, "source_region": "Middle East"},
            {"hs_code": "100630", "product": "Riz", "value": 450000000, "source_region": "Asia"},
            {"hs_code": "151190", "product": "Huile de palme", "value": 380000000, "source_region": "Malaysia/Indonesia"},
            {"hs_code": "720839", "product": "Produits laminés plats en fer", "value": 320000000, "source_region": "China"},
            {"hs_code": "300490", "product": "Médicaments", "value": 280000000, "source_region": "India"},
        ],
        "MAR": [  # Morocco
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "value": 4200000000, "source_region": "Middle East"},
            {"hs_code": "100199", "product": "Blé et méteil", "value": 1800000000, "source_region": "Europe"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "value": 1200000000, "source_region": "Europe"},
            {"hs_code": "870323", "product": "Véhicules automobiles", "value": 980000000, "source_region": "Europe"},
        ],
        "CIV": [  # Côte d'Ivoire
            {"hs_code": "100630", "product": "Riz", "value": 850000000, "source_region": "Asia"},
            {"hs_code": "271019", "product": "Huiles de pétrole raffinées", "value": 720000000, "source_region": "Europe"},
            {"hs_code": "300490", "product": "Médicaments", "value": 450000000, "source_region": "Europe/India"},
            {"hs_code": "730890", "product": "Constructions en fer/acier", "value": 380000000, "source_region": "China"},
        ],
        "TUN": [  # Tunisia
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "value": 2100000000, "source_region": "Algeria/Libya"},
            {"hs_code": "100199", "product": "Blé et méteil", "value": 680000000, "source_region": "Europe"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "value": 420000000, "source_region": "Europe"},
        ],
        "GHA": [  # Ghana
            {"hs_code": "271019", "product": "Huiles de pétrole raffinées", "value": 1800000000, "source_region": "Europe"},
            {"hs_code": "100630", "product": "Riz", "value": 520000000, "source_region": "Asia"},
            {"hs_code": "870323", "product": "Véhicules automobiles", "value": 480000000, "source_region": "Europe/Asia"},
            {"hs_code": "300490", "product": "Médicaments", "value": 350000000, "source_region": "India"},
        ],
    },
    
    # African production/export capabilities
    "african_production": {
        "NGA": [
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "capacity": 85000000000, "quality": "high"},
            {"hs_code": "271121", "product": "Gaz naturel", "capacity": 8500000000, "quality": "high"},
            {"hs_code": "180100", "product": "Cacao en fèves", "capacity": 350000000, "quality": "medium"},
            {"hs_code": "400122", "product": "Caoutchouc naturel", "capacity": 180000000, "quality": "medium"},
        ],
        "ZAF": [
            {"hs_code": "710812", "product": "Or", "capacity": 12000000000, "quality": "high"},
            {"hs_code": "711011", "product": "Platine", "capacity": 8500000000, "quality": "high"},
            {"hs_code": "870323", "product": "Véhicules automobiles", "capacity": 6200000000, "quality": "high"},
            {"hs_code": "720839", "product": "Produits laminés plats en fer", "capacity": 4500000000, "quality": "high"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "capacity": 1800000000, "quality": "high"},
            {"hs_code": "300490", "product": "Médicaments", "capacity": 1200000000, "quality": "medium"},
        ],
        "EGY": [
            {"hs_code": "271019", "product": "Huiles de pétrole raffinées", "capacity": 4200000000, "quality": "high"},
            {"hs_code": "310210", "product": "Engrais azotés", "capacity": 2800000000, "quality": "high"},
            {"hs_code": "720839", "product": "Produits laminés plats en fer", "capacity": 2200000000, "quality": "high"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "capacity": 1500000000, "quality": "high"},
            {"hs_code": "690890", "product": "Carreaux céramiques", "capacity": 980000000, "quality": "high"},
        ],
        "MAR": [
            {"hs_code": "310390", "product": "Engrais phosphatés", "capacity": 5500000000, "quality": "high"},
            {"hs_code": "870323", "product": "Véhicules automobiles", "capacity": 4800000000, "quality": "high"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "capacity": 3200000000, "quality": "high"},
            {"hs_code": "620342", "product": "Pantalons en coton", "capacity": 1800000000, "quality": "high"},
        ],
        "ETH": [
            {"hs_code": "090111", "product": "Café non torréfié", "capacity": 1200000000, "quality": "high"},
            {"hs_code": "060311", "product": "Fleurs coupées", "capacity": 850000000, "quality": "high"},
            {"hs_code": "410120", "product": "Cuirs et peaux", "capacity": 450000000, "quality": "medium"},
            {"hs_code": "620520", "product": "Chemises en coton", "capacity": 380000000, "quality": "medium"},
        ],
        "CIV": [
            {"hs_code": "180100", "product": "Cacao en fèves", "capacity": 5500000000, "quality": "high"},
            {"hs_code": "180400", "product": "Beurre de cacao", "capacity": 1200000000, "quality": "high"},
            {"hs_code": "080130", "product": "Noix de cajou", "capacity": 850000000, "quality": "high"},
            {"hs_code": "400122", "product": "Caoutchouc naturel", "capacity": 620000000, "quality": "high"},
        ],
        "KEN": [
            {"hs_code": "090240", "product": "Thé noir", "capacity": 1400000000, "quality": "high"},
            {"hs_code": "060311", "product": "Fleurs coupées", "capacity": 950000000, "quality": "high"},
            {"hs_code": "090111", "product": "Café non torréfié", "capacity": 280000000, "quality": "high"},
            {"hs_code": "070820", "product": "Haricots", "capacity": 180000000, "quality": "medium"},
        ],
        "TUN": [
            {"hs_code": "150910", "product": "Huile d'olive vierge", "capacity": 850000000, "quality": "high"},
            {"hs_code": "854430", "product": "Fils et câbles électriques", "capacity": 1200000000, "quality": "high"},
            {"hs_code": "620342", "product": "Pantalons en coton", "capacity": 680000000, "quality": "high"},
            {"hs_code": "080520", "product": "Dattes", "capacity": 420000000, "quality": "high"},
        ],
        "GHA": [
            {"hs_code": "180100", "product": "Cacao en fèves", "capacity": 2200000000, "quality": "high"},
            {"hs_code": "710812", "product": "Or", "capacity": 6500000000, "quality": "high"},
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "capacity": 3800000000, "quality": "high"},
            {"hs_code": "080130", "product": "Noix de cajou", "capacity": 350000000, "quality": "medium"},
        ],
        "DZA": [
            {"hs_code": "271121", "product": "Gaz naturel", "capacity": 35000000000, "quality": "high"},
            {"hs_code": "270900", "product": "Huiles brutes de pétrole", "capacity": 28000000000, "quality": "high"},
            {"hs_code": "310210", "product": "Engrais azotés", "capacity": 1800000000, "quality": "high"},
            {"hs_code": "080520", "product": "Dattes", "capacity": 950000000, "quality": "high"},
        ],
    }
}


def get_simulated_imports_from_outside(country_iso3: str) -> List[Dict]:
    """
    Get simulated import data for a country
    In production, this would call the Comtrade API
    """
    return SIMULATED_TRADE_DATA["imports_from_outside"].get(
        country_iso3.upper(), []
    )


def get_simulated_african_production(country_iso3: str) -> List[Dict]:
    """
    Get simulated production/export capabilities
    In production, this would aggregate from multiple sources
    """
    return SIMULATED_TRADE_DATA["african_production"].get(
        country_iso3.upper(), []
    )


def get_all_african_production() -> Dict[str, List[Dict]]:
    """Get all African production capabilities"""
    return SIMULATED_TRADE_DATA["african_production"]


def get_country_name(iso3: str, lang: str = "fr") -> str:
    """Get country name in specified language"""
    country = COUNTRY_NAMES.get(iso3.upper(), {})
    return country.get(lang, country.get("en", iso3))


# Create singleton instance
comtrade_service = ComtradeService()
