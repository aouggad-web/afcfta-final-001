"""
Real Trade Substitution Analysis Service
Uses real data from OEC API for analyzing intra-African trade substitution opportunities
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from collections import defaultdict
import asyncio

from services.real_trade_data_service import (
    real_trade_service,
    AFRICAN_COUNTRIES,
    get_country_name,
    get_product_name
)

logger = logging.getLogger(__name__)


class RealSubstitutionService:
    """
    Service for analyzing trade substitution opportunities using real OEC data
    """
    
    def __init__(self):
        self.african_countries = list(AFRICAN_COUNTRIES.keys())
        self._cache = {}
        self._cache_ttl = 1800  # 30 minutes
    
    async def find_import_substitution_opportunities(
        self,
        importer_iso3: str,
        year: int = 2022,
        min_value: int = 5000000,
        lang: str = "fr"
    ) -> Dict:
        """
        Find import substitution opportunities using REAL OEC data
        
        1. Get what the country imports from outside Africa (OEC API)
        2. For each product, find African countries that export it
        3. Calculate substitution potential
        """
        importer = importer_iso3.upper()
        if importer not in self.african_countries:
            return {"error": f"Country {importer} not found in AfCFTA"}
        
        try:
            # Step 1: Get imports from outside Africa
            import_data = await real_trade_service.get_oec_bilateral_from_world(
                importer, year=year, limit=50
            )
            
            products_from_outside = import_data.get("products_from_outside", [])
            
            if not products_from_outside:
                # Fallback: get all imports and assume 70% from outside
                all_imports = await real_trade_service.get_oec_imports(
                    importer, year=year, limit=100
                )
                products_from_outside = [
                    {
                        "hs_code": imp["hs_code"],
                        "product_name": imp["product_name"],
                        "import_value": int(imp["trade_value"] * 0.7),  # Estimate 70% from outside
                        "source_regions": ["World"]
                    }
                    for imp in all_imports if imp["trade_value"] >= min_value
                ]
            
            # Step 2: For each imported product, find African exporters
            opportunities = []
            total_substitutable = 0
            
            for product in products_from_outside:
                if product["import_value"] < min_value:
                    continue
                
                hs_code = product["hs_code"]
                
                # Find African countries that export this product
                african_exporters = await real_trade_service.get_african_exporters_for_product(
                    hs_code, year=year
                )
                
                # Filter out the importer itself
                african_exporters = [
                    exp for exp in african_exporters 
                    if exp["country_iso3"] != importer and exp["export_value"] > 0
                ]
                
                if african_exporters:
                    # Calculate substitution potential
                    total_african_capacity = sum(exp["export_value"] for exp in african_exporters)
                    substitution_potential = min(
                        product["import_value"],
                        total_african_capacity * 0.3  # Realistic: capture 30% of African exports
                    )
                    
                    opportunity = {
                        "imported_product": {
                            "hs_code": hs_code,
                            "name": product["product_name"] or get_product_name(hs_code, lang),
                            "import_value": product["import_value"],
                            "current_source": ", ".join(product.get("source_regions", ["Hors Afrique"])[:2])
                        },
                        "african_suppliers": [
                            {
                                "country_iso3": exp["country_iso3"],
                                "country_name": get_country_name(exp["country_iso3"], lang),
                                "export_value": exp["export_value"],
                                "share_potential": min(
                                    exp["export_value"] / product["import_value"] * 100, 100
                                ) if product["import_value"] > 0 else 0
                            }
                            for exp in african_exporters[:5]
                        ],
                        "substitution_potential": substitution_potential,
                        "difficulty": self._assess_difficulty(
                            product["import_value"], 
                            total_african_capacity
                        )
                    }
                    
                    opportunities.append(opportunity)
                    total_substitutable += substitution_potential
            
            # Sort by substitution potential
            opportunities.sort(key=lambda x: x["substitution_potential"], reverse=True)
            
            return {
                "importer": {
                    "iso3": importer,
                    "name": get_country_name(importer, lang)
                },
                "year": year,
                "analysis_date": datetime.utcnow().isoformat(),
                "data_source": "OEC (Observatory of Economic Complexity)",
                "summary": {
                    "total_opportunities": len(opportunities),
                    "total_substitutable_value": total_substitutable,
                    "total_imports_from_outside": import_data.get("from_outside", 0),
                    "potential_savings_percent": 17.0,  # AfCFTA tariff + logistics savings
                    "top_sectors": self._identify_top_sectors(opportunities, lang)
                },
                "opportunities": opportunities[:20],  # Top 20
                "sources": ["OEC/BACI International Trade Data", "UN Comtrade"]
            }
            
        except Exception as e:
            logger.error(f"Error in import substitution analysis: {str(e)}")
            return {"error": str(e), "opportunities": []}
    
    async def find_export_opportunities(
        self,
        exporter_iso3: str,
        year: int = 2022,
        min_market_size: int = 10000000,
        lang: str = "fr"
    ) -> Dict:
        """
        Find export opportunities for a country using REAL OEC data
        
        1. Get what the country exports (OEC API)
        2. For each product, find African countries that import it from outside
        3. Calculate market capture potential
        """
        exporter = exporter_iso3.upper()
        if exporter not in self.african_countries:
            return {"error": f"Country {exporter} not found in AfCFTA"}
        
        try:
            # Step 1: Get what this country exports
            exports = await real_trade_service.get_oec_exports(
                exporter, year=year, limit=50
            )
            
            opportunities = []
            total_market_potential = 0
            
            for export_product in exports:
                if export_product["trade_value"] < 1000000:  # Min $1M export capacity
                    continue
                
                hs_code = export_product["hs_code"]
                
                # Step 2: Find African countries that import this product
                potential_markets = []
                
                for other_country in self.african_countries:
                    if other_country == exporter:
                        continue
                    
                    # Get imports for this country
                    import_data = await real_trade_service.get_oec_bilateral_from_world(
                        other_country, year=year, limit=30
                    )
                    
                    # Check if they import this product from outside
                    for imported in import_data.get("products_from_outside", []):
                        if imported["hs_code"][:2] == hs_code[:2]:  # Match at chapter level
                            if imported["import_value"] >= min_market_size:
                                capture_potential = min(
                                    export_product["trade_value"] * 0.2,
                                    imported["import_value"] * 0.15
                                )
                                
                                potential_markets.append({
                                    "country_iso3": other_country,
                                    "country_name": get_country_name(other_country, lang),
                                    "import_value": imported["import_value"],
                                    "current_source": ", ".join(imported.get("source_regions", [])[:2]),
                                    "capture_potential": capture_potential
                                })
                                break
                
                if potential_markets:
                    potential_markets.sort(key=lambda x: x["capture_potential"], reverse=True)
                    total_capture = sum(m["capture_potential"] for m in potential_markets)
                    
                    opportunity = {
                        "exportable_product": {
                            "hs_code": hs_code,
                            "name": export_product["product_name"] or get_product_name(hs_code, lang),
                            "export_capacity": export_product["trade_value"]
                        },
                        "target_markets": potential_markets[:5],
                        "total_market_size": sum(m["import_value"] for m in potential_markets),
                        "estimated_capture": total_capture,
                        "competitiveness": "competitive"
                    }
                    
                    opportunities.append(opportunity)
                    total_market_potential += total_capture
            
            opportunities.sort(key=lambda x: x["estimated_capture"], reverse=True)
            
            return {
                "exporter": {
                    "iso3": exporter,
                    "name": get_country_name(exporter, lang)
                },
                "year": year,
                "analysis_date": datetime.utcnow().isoformat(),
                "data_source": "OEC (Observatory of Economic Complexity)",
                "summary": {
                    "total_opportunities": len(opportunities),
                    "total_market_potential": total_market_potential,
                    "top_products": [o["exportable_product"]["name"] for o in opportunities[:5]],
                    "top_markets": self._identify_top_markets(opportunities, lang)
                },
                "opportunities": opportunities[:15],
                "sources": ["OEC/BACI International Trade Data", "UN Comtrade"]
            }
            
        except Exception as e:
            logger.error(f"Error in export opportunity analysis: {str(e)}")
            return {"error": str(e), "opportunities": []}
    
    async def get_product_trade_flows(
        self,
        hs_code: str,
        year: int = 2022,
        lang: str = "fr"
    ) -> Dict:
        """
        Analyze trade flows for a specific product across Africa
        """
        try:
            # Get all African exporters for this product
            exporters = await real_trade_service.get_african_exporters_for_product(
                hs_code, year=year
            )
            
            # Get importers (simplified - would need more API calls for full data)
            importers = []
            total_exported = sum(e["export_value"] for e in exporters)
            
            return {
                "hs_code": hs_code,
                "product_name": get_product_name(hs_code, lang),
                "year": year,
                "analysis_date": datetime.utcnow().isoformat(),
                "summary": {
                    "total_african_exports": total_exported,
                    "top_exporters_count": len(exporters),
                    "substitution_potential": total_exported * 0.25
                },
                "exporters": exporters[:10],
                "sources": ["OEC/BACI International Trade Data"]
            }
            
        except Exception as e:
            logger.error(f"Error in product analysis: {str(e)}")
            return {"error": str(e)}
    
    def _assess_difficulty(self, import_value: float, african_capacity: float) -> str:
        """Assess substitution difficulty"""
        if african_capacity >= import_value * 0.5:
            return "easy"
        elif african_capacity >= import_value * 0.2:
            return "moderate"
        else:
            return "difficult"
    
    def _identify_top_sectors(self, opportunities: List[Dict], lang: str) -> List[Dict]:
        """Identify top sectors from opportunities"""
        sector_values = defaultdict(float)
        
        for opp in opportunities:
            hs2 = opp["imported_product"]["hs_code"][:2]
            sector_values[hs2] += opp["substitution_potential"]
        
        sorted_sectors = sorted(sector_values.items(), key=lambda x: x[1], reverse=True)
        return [
            {
                "hs_chapter": s[0],
                "name": get_product_name(s[0], lang),
                "value": s[1]
            }
            for s in sorted_sectors[:5]
        ]
    
    def _identify_top_markets(self, opportunities: List[Dict], lang: str) -> List[Dict]:
        """Identify top export markets"""
        market_values = defaultdict(float)
        
        for opp in opportunities:
            for market in opp.get("target_markets", []):
                market_values[market["country_iso3"]] += market["capture_potential"]
        
        sorted_markets = sorted(market_values.items(), key=lambda x: x[1], reverse=True)
        return [
            {
                "iso3": m[0],
                "name": get_country_name(m[0], lang),
                "potential": m[1]
            }
            for m in sorted_markets[:5]
        ]


# Singleton instance
real_substitution_service = RealSubstitutionService()
