"""
Service d'intégration avec l'API OEC (Observatory of Economic Complexity)
=========================================================================
Permet de récupérer les statistiques commerciales par:
- Code HS (HS4, HS6)
- Pays exportateur/importateur
- Année

API Documentation: https://oec.world/en/resources/documentation
"""

import httpx
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Configuration de l'API OEC
OEC_BASE_URL = "https://api-v2.oec.world/tesseract/data.jsonrecords"

# Cubes disponibles (datasets)
OEC_CUBES = {
    "hs92": "trade_i_baci_a_92",      # HS Rev. 1992 (1995-2023)
    "hs96": "trade_i_baci_a_96",      # HS Rev. 1996 (1998-2023)
    "hs02": "trade_i_baci_a_02",      # HS Rev. 2002 (2003-2023)
    "hs07": "trade_i_baci_a_07",      # HS Rev. 2007 (2008-2023)
    "hs12": "trade_i_baci_a_12",      # HS Rev. 2012 (2013-2023)
    "hs17": "trade_i_baci_a_17",      # HS Rev. 2017 (2018-2023)
}

# Codes ISO des pays africains pour l'OEC
AFRICAN_COUNTRIES_OEC = {
    "DZA": {"oec_id": "afdza", "name_fr": "Algérie", "name_en": "Algeria"},
    "AGO": {"oec_id": "afago", "name_fr": "Angola", "name_en": "Angola"},
    "BEN": {"oec_id": "afben", "name_fr": "Bénin", "name_en": "Benin"},
    "BWA": {"oec_id": "afbwa", "name_fr": "Botswana", "name_en": "Botswana"},
    "BFA": {"oec_id": "afbfa", "name_fr": "Burkina Faso", "name_en": "Burkina Faso"},
    "BDI": {"oec_id": "afbdi", "name_fr": "Burundi", "name_en": "Burundi"},
    "CPV": {"oec_id": "afcpv", "name_fr": "Cap-Vert", "name_en": "Cape Verde"},
    "CMR": {"oec_id": "afcmr", "name_fr": "Cameroun", "name_en": "Cameroon"},
    "CAF": {"oec_id": "afcaf", "name_fr": "République centrafricaine", "name_en": "Central African Republic"},
    "TCD": {"oec_id": "aftcd", "name_fr": "Tchad", "name_en": "Chad"},
    "COM": {"oec_id": "afcom", "name_fr": "Comores", "name_en": "Comoros"},
    "COG": {"oec_id": "afcog", "name_fr": "Congo", "name_en": "Congo"},
    "COD": {"oec_id": "afcod", "name_fr": "RD Congo", "name_en": "DR Congo"},
    "CIV": {"oec_id": "afciv", "name_fr": "Côte d'Ivoire", "name_en": "Ivory Coast"},
    "DJI": {"oec_id": "afdji", "name_fr": "Djibouti", "name_en": "Djibouti"},
    "EGY": {"oec_id": "afegy", "name_fr": "Égypte", "name_en": "Egypt"},
    "GNQ": {"oec_id": "afgnq", "name_fr": "Guinée équatoriale", "name_en": "Equatorial Guinea"},
    "ERI": {"oec_id": "aferi", "name_fr": "Érythrée", "name_en": "Eritrea"},
    "SWZ": {"oec_id": "afswz", "name_fr": "Eswatini", "name_en": "Eswatini"},
    "ETH": {"oec_id": "afeth", "name_fr": "Éthiopie", "name_en": "Ethiopia"},
    "GAB": {"oec_id": "afgab", "name_fr": "Gabon", "name_en": "Gabon"},
    "GMB": {"oec_id": "afgmb", "name_fr": "Gambie", "name_en": "Gambia"},
    "GHA": {"oec_id": "afgha", "name_fr": "Ghana", "name_en": "Ghana"},
    "GIN": {"oec_id": "afgin", "name_fr": "Guinée", "name_en": "Guinea"},
    "GNB": {"oec_id": "afgnb", "name_fr": "Guinée-Bissau", "name_en": "Guinea-Bissau"},
    "KEN": {"oec_id": "afken", "name_fr": "Kenya", "name_en": "Kenya"},
    "LSO": {"oec_id": "aflso", "name_fr": "Lesotho", "name_en": "Lesotho"},
    "LBR": {"oec_id": "aflbr", "name_fr": "Liberia", "name_en": "Liberia"},
    "LBY": {"oec_id": "aflby", "name_fr": "Libye", "name_en": "Libya"},
    "MDG": {"oec_id": "afmdg", "name_fr": "Madagascar", "name_en": "Madagascar"},
    "MWI": {"oec_id": "afmwi", "name_fr": "Malawi", "name_en": "Malawi"},
    "MLI": {"oec_id": "afmli", "name_fr": "Mali", "name_en": "Mali"},
    "MRT": {"oec_id": "afmrt", "name_fr": "Mauritanie", "name_en": "Mauritania"},
    "MUS": {"oec_id": "afmus", "name_fr": "Maurice", "name_en": "Mauritius"},
    "MAR": {"oec_id": "afmar", "name_fr": "Maroc", "name_en": "Morocco"},
    "MOZ": {"oec_id": "afmoz", "name_fr": "Mozambique", "name_en": "Mozambique"},
    "NAM": {"oec_id": "afnam", "name_fr": "Namibie", "name_en": "Namibia"},
    "NER": {"oec_id": "afner", "name_fr": "Niger", "name_en": "Niger"},
    "NGA": {"oec_id": "afnga", "name_fr": "Nigeria", "name_en": "Nigeria"},
    "RWA": {"oec_id": "afrwa", "name_fr": "Rwanda", "name_en": "Rwanda"},
    "STP": {"oec_id": "afstp", "name_fr": "São Tomé-et-Príncipe", "name_en": "São Tomé and Príncipe"},
    "SEN": {"oec_id": "afsen", "name_fr": "Sénégal", "name_en": "Senegal"},
    "SYC": {"oec_id": "afsyc", "name_fr": "Seychelles", "name_en": "Seychelles"},
    "SLE": {"oec_id": "afsle", "name_fr": "Sierra Leone", "name_en": "Sierra Leone"},
    "SOM": {"oec_id": "afsom", "name_fr": "Somalie", "name_en": "Somalia"},
    "ZAF": {"oec_id": "afzaf", "name_fr": "Afrique du Sud", "name_en": "South Africa"},
    "SSD": {"oec_id": "afssd", "name_fr": "Soudan du Sud", "name_en": "South Sudan"},
    "SDN": {"oec_id": "afsdn", "name_fr": "Soudan", "name_en": "Sudan"},
    "TZA": {"oec_id": "aftza", "name_fr": "Tanzanie", "name_en": "Tanzania"},
    "TGO": {"oec_id": "aftgo", "name_fr": "Togo", "name_en": "Togo"},
    "TUN": {"oec_id": "aftun", "name_fr": "Tunisie", "name_en": "Tunisia"},
    "UGA": {"oec_id": "afuga", "name_fr": "Ouganda", "name_en": "Uganda"},
    "ZMB": {"oec_id": "afzmb", "name_fr": "Zambie", "name_en": "Zambia"},
    "ZWE": {"oec_id": "afzwe", "name_fr": "Zimbabwe", "name_en": "Zimbabwe"},
}


class OECTradeService:
    """Service pour interroger l'API OEC"""
    
    def __init__(self, api_token: Optional[str] = None):
        self.api_token = api_token
        self.timeout = 30.0
    
    async def _make_request(self, params: Dict) -> Dict:
        """Effectue une requête à l'API OEC"""
        if self.api_token:
            params["token"] = self.api_token
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.get(OEC_BASE_URL, params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"OEC API error: {e.response.status_code}")
                return {"error": str(e), "data": []}
            except Exception as e:
                logger.error(f"OEC request failed: {e}")
                return {"error": str(e), "data": []}
    
    def _build_params(
        self,
        cube: str,
        drilldowns: List[str],
        measures: List[str],
        cuts: Optional[Dict] = None,
        limit: int = 100
    ) -> Dict:
        """Construit les paramètres de requête"""
        params = {
            "cube": cube,
            "drilldowns": ",".join(drilldowns),
            "measures": ",".join(measures),
            "limit": limit
        }
        if cuts:
            for key, value in cuts.items():
                params[key] = value
        return params
    
    async def get_exports_by_product(
        self,
        country_iso3: str,
        year: int,
        hs_level: str = "HS4",
        limit: int = 50
    ) -> Dict:
        """
        Récupère les exportations d'un pays par produit
        
        Args:
            country_iso3: Code ISO3 du pays (ex: "NGA" pour Nigeria)
            year: Année (ex: 2022)
            hs_level: Niveau HS (HS2, HS4, HS6)
            limit: Nombre max de résultats
        """
        country_info = AFRICAN_COUNTRIES_OEC.get(country_iso3.upper())
        if not country_info:
            return {"error": f"Country {country_iso3} not found", "data": []}
        
        params = self._build_params(
            cube=OEC_CUBES["hs92"],
            drilldowns=["Year", "Exporter Country", hs_level],
            measures=["Trade Value"],
            cuts={
                "Year": str(year),
                "Exporter Country": country_info["oec_id"]
            },
            limit=limit
        )
        
        result = await self._make_request(params)
        return self._format_product_response(result, "exports", country_info)
    
    async def get_imports_by_product(
        self,
        country_iso3: str,
        year: int,
        hs_level: str = "HS4",
        limit: int = 50
    ) -> Dict:
        """
        Récupère les importations d'un pays par produit
        """
        country_info = AFRICAN_COUNTRIES_OEC.get(country_iso3.upper())
        if not country_info:
            return {"error": f"Country {country_iso3} not found", "data": []}
        
        params = self._build_params(
            cube=OEC_CUBES["hs92"],
            drilldowns=["Year", "Importer Country", hs_level],
            measures=["Trade Value"],
            cuts={
                "Year": str(year),
                "Importer Country": country_info["oec_id"]
            },
            limit=limit
        )
        
        result = await self._make_request(params)
        return self._format_product_response(result, "imports", country_info)
    
    def _format_oec_hs_id(self, hs_code: str) -> str:
        """
        Formate un code HS pour l'API OEC.
        L'OEC utilise un format spécifique: préfixe 2 + code HS pour HS4, préfixe 2 + code pour HS6
        Ex: HS4 0901 (café) -> 20901
            HS6 090111 -> 2090111
        """
        # Nettoyer le code
        clean_code = hs_code.lstrip('0').zfill(len(hs_code))
        # Ajouter le préfixe 2 pour l'API OEC
        return f"2{hs_code.zfill(4)}" if len(hs_code) <= 4 else f"2{hs_code}"
    
    async def get_trade_by_hs_code(
        self,
        hs_code: str,
        year: int,
        trade_flow: str = "exports",
        limit: int = 50
    ) -> Dict:
        """
        Récupère les statistiques commerciales pour un code HS spécifique
        
        Args:
            hs_code: Code HS (4 ou 6 chiffres)
            year: Année
            trade_flow: "exports" ou "imports"
            limit: Nombre max de résultats
        """
        # Déterminer le niveau HS et formater l'ID
        hs_code_clean = hs_code.zfill(4)
        hs_level = "HS4" if len(hs_code_clean) <= 4 else "HS6"
        oec_hs_id = self._format_oec_hs_id(hs_code_clean)
        
        if trade_flow == "exports":
            drilldowns = ["Year", "Exporter Country"]
            country_field = "Exporter Country"
        else:
            drilldowns = ["Year", "Importer Country"]
            country_field = "Importer Country"
        
        # L'API OEC utilise le nom du niveau directement comme filtre (pas "ID")
        params = self._build_params(
            cube=OEC_CUBES["hs92"],
            drilldowns=drilldowns,
            measures=["Trade Value"],
            cuts={
                "Year": str(year),
                hs_level: oec_hs_id
            },
            limit=limit
        )
        
        result = await self._make_request(params)
        return self._format_hs_response(result, hs_code, year, trade_flow)
    
    async def get_bilateral_trade(
        self,
        exporter_iso3: str,
        importer_iso3: str,
        year: int,
        hs_level: str = "HS4",
        limit: int = 50
    ) -> Dict:
        """
        Récupère le commerce bilatéral entre deux pays
        """
        exporter_info = AFRICAN_COUNTRIES_OEC.get(exporter_iso3.upper())
        importer_info = AFRICAN_COUNTRIES_OEC.get(importer_iso3.upper())
        
        if not exporter_info:
            return {"error": f"Exporter country {exporter_iso3} not found", "data": []}
        if not importer_info:
            return {"error": f"Importer country {importer_iso3} not found", "data": []}
        
        params = self._build_params(
            cube=OEC_CUBES["hs92"],
            drilldowns=["Year", "Exporter Country", "Importer Country", hs_level],
            measures=["Trade Value"],
            cuts={
                "Year": str(year),
                "Exporter Country": exporter_info["oec_id"],
                "Importer Country": importer_info["oec_id"]
            },
            limit=limit
        )
        
        result = await self._make_request(params)
        return self._format_bilateral_response(result, exporter_info, importer_info, year)
    
    async def get_available_years(self) -> List[int]:
        """Retourne les années disponibles dans l'API"""
        # Les données BACI couvrent généralement 1995-2023
        return list(range(1995, 2024))
    
    async def get_top_african_exporters(
        self,
        hs_code: str,
        year: int,
        limit: int = 20
    ) -> Dict:
        """
        Récupère les principaux exportateurs africains pour un produit
        """
        hs_code_clean = hs_code.zfill(4)
        hs_level = "HS4" if len(hs_code_clean) <= 4 else "HS6"
        oec_hs_id = self._format_oec_hs_id(hs_code_clean)
        
        params = self._build_params(
            cube=OEC_CUBES["hs92"],
            drilldowns=["Year", "Exporter Country"],
            measures=["Trade Value"],
            cuts={
                "Year": str(year),
                hs_level: oec_hs_id
            },
            limit=200  # Get more to filter African countries
        )
        
        result = await self._make_request(params)
        
        # Filter only African countries
        african_oec_ids = {v["oec_id"] for v in AFRICAN_COUNTRIES_OEC.values()}
        african_data = []
        
        for row in result.get("data", []):
            country_id = row.get("Exporter Country ID", "")
            if country_id in african_oec_ids:
                african_data.append(row)
        
        # Sort by trade value
        african_data.sort(key=lambda x: x.get("Trade Value", 0), reverse=True)
        
        return {
            "hs_code": hs_code,
            "year": year,
            "total_countries": len(african_data),
            "data": african_data[:limit],
            "source": "OEC/BACI"
        }
    
    def _format_product_response(self, result: Dict, flow: str, country_info: Dict) -> Dict:
        """Formate la réponse pour les produits"""
        data = result.get("data", [])
        return {
            "country": country_info,
            "trade_flow": flow,
            "total_products": len(data),
            "total_value": sum(row.get("Trade Value", 0) for row in data),
            "currency": "USD",
            "data": data,
            "source": "OEC/BACI",
            "retrieved_at": datetime.utcnow().isoformat()
        }
    
    def _format_hs_response(self, result: Dict, hs_code: str, year: int, flow: str) -> Dict:
        """Formate la réponse pour un code HS"""
        data = result.get("data", [])
        return {
            "hs_code": hs_code,
            "year": year,
            "trade_flow": flow,
            "total_countries": len(data),
            "total_value": sum(row.get("Trade Value", 0) for row in data),
            "currency": "USD",
            "data": data,
            "source": "OEC/BACI",
            "retrieved_at": datetime.utcnow().isoformat()
        }
    
    def _format_bilateral_response(
        self, result: Dict, exporter: Dict, importer: Dict, year: int
    ) -> Dict:
        """Formate la réponse pour le commerce bilatéral"""
        data = result.get("data", [])
        return {
            "exporter": exporter,
            "importer": importer,
            "year": year,
            "total_products": len(data),
            "total_value": sum(row.get("Trade Value", 0) for row in data),
            "currency": "USD",
            "data": data,
            "source": "OEC/BACI",
            "retrieved_at": datetime.utcnow().isoformat()
        }


# Instance globale du service
oec_service = OECTradeService()


# Fonctions utilitaires pour l'API
async def get_country_exports(country_iso3: str, year: int, limit: int = 50) -> Dict:
    """Raccourci pour obtenir les exports d'un pays"""
    return await oec_service.get_exports_by_product(country_iso3, year, limit=limit)


async def get_country_imports(country_iso3: str, year: int, limit: int = 50) -> Dict:
    """Raccourci pour obtenir les imports d'un pays"""
    return await oec_service.get_imports_by_product(country_iso3, year, limit=limit)


async def get_product_trade_stats(hs_code: str, year: int, flow: str = "exports") -> Dict:
    """Raccourci pour obtenir les stats d'un produit"""
    return await oec_service.get_trade_by_hs_code(hs_code, year, flow)


async def get_african_top_exporters(hs_code: str, year: int, limit: int = 10) -> Dict:
    """Raccourci pour obtenir les top exportateurs africains"""
    return await oec_service.get_top_african_exporters(hs_code, year, limit)


def get_african_countries_list(language: str = "fr") -> List[Dict]:
    """Retourne la liste des pays africains avec leurs codes"""
    name_key = f"name_{language}"
    return [
        {
            "iso3": iso3,
            "oec_id": info["oec_id"],
            "name": info.get(name_key, info["name_en"])
        }
        for iso3, info in sorted(AFRICAN_COUNTRIES_OEC.items(), key=lambda x: x[1].get(name_key, ""))
    ]
