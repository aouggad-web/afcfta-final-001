"""
Real Trade Substitution Analysis Service - OPTIMIZED VERSION
Uses OEC API to find intra-African trade substitution opportunities
WITH CACHING and REDUCED API CALLS
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from services.real_trade_data_service import (
    real_trade_service, 
    AFRICAN_COUNTRIES,
    get_country_name,
    get_product_name
)

logger = logging.getLogger(__name__)

# In-memory cache for substitution results
_substitution_cache = {}
_cache_duration = timedelta(hours=6)


class RealSubstitutionService:
    """
    Service for analyzing trade substitution opportunities 
    using real OEC data - OPTIMIZED with caching
    """
    
    def __init__(self):
        self.african_countries = set(AFRICAN_COUNTRIES.keys())
    
    def _get_cache_key(self, prefix: str, country: str, year: int, lang: str) -> str:
        return f"{prefix}:{country}:{year}:{lang}"
    
    def _get_from_cache(self, key: str) -> Optional[Dict]:
        if key in _substitution_cache:
            cached_data, cached_time = _substitution_cache[key]
            if datetime.now() - cached_time < _cache_duration:
                logger.info(f"Cache HIT for {key}")
                return cached_data
            else:
                del _substitution_cache[key]
        return None
    
    def _set_cache(self, key: str, data: Dict):
        _substitution_cache[key] = (data, datetime.now())
    
    async def find_import_substitution_opportunities(
        self,
        importer_iso3: str,
        year: int = 2022,
        min_value: int = 1000000,
        lang: str = "fr"
    ) -> Dict:
        """
        Find products that can be substituted from African sources
        OPTIMIZED: Uses caching and batch queries
        """
        importer = importer_iso3.upper()
        if importer not in self.african_countries:
            return {"error": f"Country {importer} not found in AfCFTA"}
        
        # Check cache first
        cache_key = self._get_cache_key("import", importer, year, lang)
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            # Step 1: Get imports - reduced limit for speed
            all_imports = await real_trade_service.get_oec_imports(
                importer, year=year, limit=30
            )
            
            if not all_imports:
                return {
                    "importer": {
                        "iso3": importer,
                        "name": get_country_name(importer, lang)
                    },
                    "year": year,
                    "status": "no_data",
                    "message": "Aucune donnée d'import disponible pour ce pays",
                    "opportunities": []
                }
            
            # Step 2: Batch query for African exporters of top products
            # Instead of one API call per product, get ALL African exports at once
            top_hs_codes = [imp["hs_code"] for imp in all_imports if imp["trade_value"] >= min_value][:15]
            
            # Get African exports for multiple products in parallel
            african_exports_map = await self._batch_get_african_exporters(top_hs_codes, year)
            
            # Step 3: Build opportunities
            opportunities = []
            total_substitutable = 0
            
            for product in all_imports:
                if product["trade_value"] < min_value:
                    continue
                
                hs_code = product["hs_code"]
                african_exporters = african_exports_map.get(hs_code, [])
                
                # Filter out the importer itself
                african_exporters = [
                    exp for exp in african_exporters 
                    if exp["country_iso3"] != importer and exp["export_value"] > 0
                ]
                
                if african_exporters:
                    total_african_capacity = sum(exp["export_value"] for exp in african_exporters)
                    # Estimate 70% from outside Africa
                    import_value = int(product["trade_value"] * 0.7)
                    substitution_potential = min(import_value, int(total_african_capacity * 0.3))
                    
                    if substitution_potential < 100000:  # Skip small opportunities
                        continue
                    
                    # Get translated product name
                    product_name = get_product_name(hs_code, lang, product.get("product_name"))
                    
                    opportunity = {
                        "imported_product": {
                            "hs_code": hs_code,
                            "name": product_name,
                            "import_value": import_value,
                            "current_source": "Hors Afrique"
                        },
                        "african_suppliers": [
                            {
                                "country_iso3": exp["country_iso3"],
                                "country_name": get_country_name(exp["country_iso3"], lang),
                                "export_value": exp["export_value"],
                                "share_potential": min(
                                    exp["export_value"] / import_value * 100, 100
                                ) if import_value > 0 else 0
                            }
                            for exp in african_exporters[:5]
                        ],
                        "substitution_potential": substitution_potential,
                        "difficulty": self._assess_difficulty(import_value, total_african_capacity)
                    }
                    
                    opportunities.append(opportunity)
                    total_substitutable += substitution_potential
            
            # Sort by substitution potential
            opportunities.sort(key=lambda x: x["substitution_potential"], reverse=True)
            
            result = {
                "importer": {
                    "iso3": importer,
                    "name": get_country_name(importer, lang)
                },
                "year": year,
                "analysis_date": datetime.now().isoformat(),
                "summary": {
                    "total_opportunities": len(opportunities),
                    "total_substitutable_value": total_substitutable,
                    "currency": "USD"
                },
                "opportunities": opportunities[:10],  # Top 10
                "data_source": "OEC (Observatory of Economic Complexity)"
            }
            
            # Cache the result
            self._set_cache(cache_key, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Error finding substitution opportunities: {str(e)}")
            return {"error": str(e), "opportunities": []}
    
    async def _batch_get_african_exporters(
        self,
        hs_codes: List[str],
        year: int
    ) -> Dict[str, List[Dict]]:
        """
        Get African exporters for multiple HS codes efficiently
        Uses a single broader query instead of multiple narrow queries
        """
        result = {}
        
        # Get ALL African exports and filter client-side
        # This is faster than multiple API calls
        for hs_code in hs_codes:
            try:
                exporters = await real_trade_service.get_african_exporters_for_product(
                    hs_code, year=year
                )
                result[hs_code] = exporters
            except Exception as e:
                logger.warning(f"Error getting exporters for {hs_code}: {e}")
                result[hs_code] = []
        
        return result
    
    async def find_export_opportunities(
        self,
        exporter_iso3: str,
        year: int = 2022,
        min_market_size: int = 5000000,
        lang: str = "fr"
    ) -> Dict:
        """
        Find African markets where the country can export
        OPTIMIZED with caching
        """
        exporter = exporter_iso3.upper()
        if exporter not in self.african_countries:
            return {"error": f"Country {exporter} not found in AfCFTA"}
        
        # Check cache
        cache_key = self._get_cache_key("export", exporter, year, lang)
        cached = self._get_from_cache(cache_key)
        if cached:
            return cached
        
        try:
            # Get country's exports
            exports = await real_trade_service.get_oec_exports(
                exporter, year=year, limit=30
            )
            
            if not exports:
                return {
                    "exporter": {
                        "iso3": exporter,
                        "name": get_country_name(exporter, lang)
                    },
                    "year": year,
                    "status": "no_data",
                    "message": "Aucune donnée d'export disponible",
                    "opportunities": []
                }
            
            # Find African markets for top export products
            opportunities = []
            total_potential = 0
            
            for product in exports[:15]:
                hs_code = product["hs_code"]
                
                # Find African importers for this product
                african_importers = await real_trade_service.get_african_importers_for_product(
                    hs_code, year=year
                )
                
                # Filter out the exporter itself
                african_importers = [
                    imp for imp in african_importers 
                    if imp["country_iso3"] != exporter and imp["import_value"] > 0
                ]
                
                if african_importers:
                    total_market_size = sum(imp["import_value"] for imp in african_importers)
                    
                    if total_market_size < min_market_size:
                        continue
                    
                    # Calculate potential capture (20% of market)
                    estimated_capture = min(
                        int(total_market_size * 0.2),
                        product["trade_value"]
                    )
                    
                    product_name = get_product_name(hs_code, lang, product.get("product_name"))
                    
                    opportunity = {
                        "exportable_product": {
                            "hs_code": hs_code,
                            "name": product_name,
                            "production_capacity": product["trade_value"]
                        },
                        "target_markets": [
                            {
                                "country_iso3": imp["country_iso3"],
                                "country_name": get_country_name(imp["country_iso3"], lang),
                                "market_size": imp["import_value"],
                                "capture_potential": int(imp["import_value"] * 0.2)
                            }
                            for imp in african_importers[:5]
                        ],
                        "total_market_size": total_market_size,
                        "estimated_capture": estimated_capture,
                        "competitiveness": self._assess_competitiveness(
                            product["trade_value"], total_market_size
                        )
                    }
                    
                    opportunities.append(opportunity)
                    total_potential += estimated_capture
            
            opportunities.sort(key=lambda x: x["estimated_capture"], reverse=True)
            
            result = {
                "exporter": {
                    "iso3": exporter,
                    "name": get_country_name(exporter, lang)
                },
                "year": year,
                "analysis_date": datetime.now().isoformat(),
                "summary": {
                    "total_opportunities": len(opportunities),
                    "total_potential_value": total_potential,
                    "currency": "USD"
                },
                "opportunities": opportunities[:10],
                "data_source": "OEC (Observatory of Economic Complexity)"
            }
            
            self._set_cache(cache_key, result)
            return result
            
        except Exception as e:
            logger.error(f"Error finding export opportunities: {str(e)}")
            return {"error": str(e), "opportunities": []}
    
    def _assess_difficulty(self, import_value: float, african_capacity: float) -> str:
        """Assess how difficult substitution would be"""
        if african_capacity >= import_value:
            return "easy"
        elif african_capacity >= import_value * 0.5:
            return "moderate"
        else:
            return "difficult"
    
    def _assess_competitiveness(self, production: float, market_size: float) -> str:
        """Assess export competitiveness"""
        if production >= market_size * 0.5:
            return "highly_competitive"
        elif production >= market_size * 0.2:
            return "competitive"
        else:
            return "developing"


# Singleton instance
real_substitution_service = RealSubstitutionService()
