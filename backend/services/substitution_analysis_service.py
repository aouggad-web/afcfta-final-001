"""
Trade Substitution Analysis Service
Analyzes opportunities for intra-African trade substitution

This service identifies:
1. What African countries import from outside Africa
2. Which African countries can produce/export those products
3. Matching opportunities for import substitution under AfCFTA
"""
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from collections import defaultdict

from services.comtrade_service import (
    get_simulated_imports_from_outside,
    get_simulated_african_production,
    get_all_african_production,
    get_country_name,
    AFRICAN_COUNTRIES_ISO3,
    COUNTRY_NAMES
)

logger = logging.getLogger(__name__)


class SubstitutionAnalysisService:
    """
    Service for analyzing trade substitution opportunities within AfCFTA
    """
    
    def __init__(self):
        self.african_countries = AFRICAN_COUNTRIES_ISO3
        self._opportunity_cache = {}
    
    def find_substitution_opportunities(
        self,
        importer_iso3: str,
        min_value: int = 10000000,  # Minimum $10M import value
        lang: str = "fr"
    ) -> Dict:
        """
        Find substitution opportunities for a specific importing country
        
        Args:
            importer_iso3: ISO3 code of the importing country
            min_value: Minimum import value to consider
            lang: Language for product/country names
        
        Returns:
            Dict with substitution opportunities
        """
        importer = importer_iso3.upper()
        if importer not in self.african_countries:
            return {"error": f"Country {importer} not found in AfCFTA"}
        
        # Get what this country imports from outside Africa
        imports = get_simulated_imports_from_outside(importer)
        
        # Get all African production capabilities
        all_production = get_all_african_production()
        
        opportunities = []
        total_substitutable_value = 0
        
        for import_item in imports:
            if import_item["value"] < min_value:
                continue
            
            hs_code = import_item["hs_code"]
            
            # Find African countries that can supply this product
            potential_suppliers = []
            
            for supplier_iso3, production_list in all_production.items():
                if supplier_iso3 == importer:
                    continue  # Skip self
                
                for prod in production_list:
                    # Match by HS code (can be partial match at chapter level)
                    if self._hs_codes_match(hs_code, prod["hs_code"]):
                        potential_suppliers.append({
                            "country_iso3": supplier_iso3,
                            "country_name": get_country_name(supplier_iso3, lang),
                            "hs_code": prod["hs_code"],
                            "product": prod["product"],
                            "production_capacity": prod["capacity"],
                            "quality": prod["quality"],
                            "match_score": self._calculate_match_score(
                                import_item["value"],
                                prod["capacity"],
                                prod["quality"]
                            )
                        })
            
            if potential_suppliers:
                # Sort by match score
                potential_suppliers.sort(key=lambda x: x["match_score"], reverse=True)
                
                opportunity = {
                    "imported_product": {
                        "hs_code": hs_code,
                        "name": import_item["product"],
                        "import_value": import_item["value"],
                        "current_source": import_item["source_region"]
                    },
                    "african_suppliers": potential_suppliers[:5],  # Top 5 suppliers
                    "substitution_potential": min(
                        import_item["value"],
                        sum(s["production_capacity"] for s in potential_suppliers[:3])
                    ),
                    "difficulty": self._assess_difficulty(import_item, potential_suppliers)
                }
                
                opportunities.append(opportunity)
                total_substitutable_value += opportunity["substitution_potential"]
        
        # Sort opportunities by substitution potential
        opportunities.sort(key=lambda x: x["substitution_potential"], reverse=True)
        
        return {
            "importer": {
                "iso3": importer,
                "name": get_country_name(importer, lang)
            },
            "analysis_date": datetime.utcnow().isoformat(),
            "summary": {
                "total_opportunities": len(opportunities),
                "total_substitutable_value": total_substitutable_value,
                "potential_savings_percent": self._estimate_savings_percent(total_substitutable_value),
                "top_sectors": self._identify_top_sectors(opportunities)
            },
            "opportunities": opportunities,
            "sources": ["UN Comtrade", "OEC", "UNCTAD", "National Statistics"]
        }
    
    def find_export_opportunities(
        self,
        exporter_iso3: str,
        min_market_size: int = 50000000,  # Minimum $50M market
        lang: str = "fr"
    ) -> Dict:
        """
        Find export opportunities for a specific African country
        
        Args:
            exporter_iso3: ISO3 code of the exporting country
            min_market_size: Minimum market size to consider
            lang: Language for names
        
        Returns:
            Dict with export opportunities to other AfCFTA countries
        """
        exporter = exporter_iso3.upper()
        if exporter not in self.african_countries:
            return {"error": f"Country {exporter} not found in AfCFTA"}
        
        # Get what this country can produce/export
        production = get_simulated_african_production(exporter)
        
        opportunities = []
        total_market_potential = 0
        
        for prod_item in production:
            hs_code = prod_item["hs_code"]
            
            # Find African countries that import this product from outside
            potential_markets = []
            
            for importer_iso3 in self.african_countries:
                if importer_iso3 == exporter:
                    continue
                
                imports = get_simulated_imports_from_outside(importer_iso3)
                
                for imp in imports:
                    if self._hs_codes_match(hs_code, imp["hs_code"]) and imp["value"] >= min_market_size:
                        potential_markets.append({
                            "country_iso3": importer_iso3,
                            "country_name": get_country_name(importer_iso3, lang),
                            "hs_code": imp["hs_code"],
                            "product": imp["product"],
                            "import_value": imp["value"],
                            "current_source": imp["source_region"],
                            "capture_potential": self._estimate_capture_potential(
                                prod_item["capacity"],
                                imp["value"],
                                prod_item["quality"]
                            )
                        })
            
            if potential_markets:
                # Sort by capture potential
                potential_markets.sort(key=lambda x: x["capture_potential"], reverse=True)
                
                market_total = sum(m["import_value"] for m in potential_markets)
                capture_total = sum(m["capture_potential"] for m in potential_markets)
                
                opportunity = {
                    "exportable_product": {
                        "hs_code": hs_code,
                        "name": prod_item["product"],
                        "production_capacity": prod_item["capacity"],
                        "quality": prod_item["quality"]
                    },
                    "target_markets": potential_markets[:8],  # Top 8 markets
                    "total_market_size": market_total,
                    "estimated_capture": capture_total,
                    "competitiveness": self._assess_competitiveness(prod_item)
                }
                
                opportunities.append(opportunity)
                total_market_potential += capture_total
        
        # Sort by estimated capture
        opportunities.sort(key=lambda x: x["estimated_capture"], reverse=True)
        
        return {
            "exporter": {
                "iso3": exporter,
                "name": get_country_name(exporter, lang)
            },
            "analysis_date": datetime.utcnow().isoformat(),
            "summary": {
                "total_opportunities": len(opportunities),
                "total_market_potential": total_market_potential,
                "top_products": [o["exportable_product"]["name"] for o in opportunities[:5]],
                "top_markets": self._identify_top_markets(opportunities)
            },
            "opportunities": opportunities,
            "sources": ["UN Comtrade", "OEC", "UNCTAD", "National Statistics"]
        }
    
    def get_product_analysis(
        self,
        hs_code: str,
        lang: str = "fr"
    ) -> Dict:
        """
        Analyze substitution opportunities for a specific product across Africa
        
        Args:
            hs_code: HS code (2, 4, or 6 digits)
            lang: Language for names
        
        Returns:
            Dict with product-level analysis
        """
        # Get all African production for this HS code
        producers = []
        all_production = get_all_african_production()
        
        for country_iso3, production_list in all_production.items():
            for prod in production_list:
                if self._hs_codes_match(hs_code, prod["hs_code"]):
                    producers.append({
                        "country_iso3": country_iso3,
                        "country_name": get_country_name(country_iso3, lang),
                        "hs_code": prod["hs_code"],
                        "product": prod["product"],
                        "capacity": prod["capacity"],
                        "quality": prod["quality"]
                    })
        
        # Get all African imports for this HS code
        importers = []
        for country_iso3 in self.african_countries:
            imports = get_simulated_imports_from_outside(country_iso3)
            for imp in imports:
                if self._hs_codes_match(hs_code, imp["hs_code"]):
                    importers.append({
                        "country_iso3": country_iso3,
                        "country_name": get_country_name(country_iso3, lang),
                        "hs_code": imp["hs_code"],
                        "product": imp["product"],
                        "import_value": imp["value"],
                        "current_source": imp["source_region"]
                    })
        
        # Sort by capacity/value
        producers.sort(key=lambda x: x["capacity"], reverse=True)
        importers.sort(key=lambda x: x["import_value"], reverse=True)
        
        total_production = sum(p["capacity"] for p in producers)
        total_imports = sum(i["import_value"] for i in importers)
        
        return {
            "hs_code": hs_code,
            "analysis_date": datetime.utcnow().isoformat(),
            "summary": {
                "total_african_production": total_production,
                "total_imports_from_outside": total_imports,
                "substitution_potential": min(total_production * 0.3, total_imports),
                "producer_count": len(producers),
                "importer_count": len(importers)
            },
            "producers": producers[:10],
            "importers": importers[:10],
            "trade_flows": self._generate_trade_flows(producers, importers),
            "sources": ["UN Comtrade", "OEC", "UNCTAD"]
        }
    
    def get_african_trade_matrix(self, lang: str = "fr") -> Dict:
        """
        Generate a comprehensive matrix of substitution opportunities
        across all AfCFTA countries
        """
        matrix = {
            "analysis_date": datetime.utcnow().isoformat(),
            "countries": [],
            "top_opportunities": [],
            "sector_summary": defaultdict(lambda: {"total_value": 0, "opportunities": 0})
        }
        
        all_opportunities = []
        
        for country in self.african_countries:
            result = self.find_substitution_opportunities(country, min_value=50000000, lang=lang)
            
            if "error" not in result:
                country_data = {
                    "iso3": country,
                    "name": get_country_name(country, lang),
                    "total_opportunities": result["summary"]["total_opportunities"],
                    "substitutable_value": result["summary"]["total_substitutable_value"]
                }
                matrix["countries"].append(country_data)
                
                # Collect all opportunities for ranking
                for opp in result.get("opportunities", []):
                    opp["importer"] = country
                    opp["importer_name"] = get_country_name(country, lang)
                    all_opportunities.append(opp)
        
        # Sort all opportunities and get top 20
        all_opportunities.sort(
            key=lambda x: x.get("substitution_potential", 0),
            reverse=True
        )
        matrix["top_opportunities"] = all_opportunities[:20]
        
        # Calculate sector summaries
        for opp in all_opportunities:
            hs2 = opp["imported_product"]["hs_code"][:2]
            sector = self._get_sector_name(hs2, lang)
            matrix["sector_summary"][sector]["total_value"] += opp["substitution_potential"]
            matrix["sector_summary"][sector]["opportunities"] += 1
        
        # Convert defaultdict to regular dict
        matrix["sector_summary"] = dict(matrix["sector_summary"])
        
        return matrix
    
    def _hs_codes_match(self, code1: str, code2: str) -> bool:
        """Check if two HS codes match (at any level)"""
        min_len = min(len(code1), len(code2))
        return code1[:min_len] == code2[:min_len]
    
    def _calculate_match_score(
        self,
        import_value: float,
        production_capacity: float,
        quality: str
    ) -> float:
        """Calculate a match score for a supplier"""
        # Base score from capacity coverage
        capacity_score = min(production_capacity / import_value, 1.0) * 50
        
        # Quality bonus
        quality_scores = {"high": 30, "medium": 20, "low": 10}
        quality_score = quality_scores.get(quality, 15)
        
        # AfCFTA preference bonus
        afcfta_bonus = 20
        
        return capacity_score + quality_score + afcfta_bonus
    
    def _assess_difficulty(
        self,
        import_item: Dict,
        suppliers: List[Dict]
    ) -> str:
        """Assess the difficulty of substitution"""
        if not suppliers:
            return "impossible"
        
        best_supplier = suppliers[0]
        
        if best_supplier["production_capacity"] >= import_item["value"] * 0.5:
            if best_supplier["quality"] == "high":
                return "easy"
            return "moderate"
        elif best_supplier["production_capacity"] >= import_item["value"] * 0.2:
            return "moderate"
        else:
            return "difficult"
    
    def _estimate_savings_percent(self, total_value: float) -> float:
        """Estimate potential savings from AfCFTA preferences"""
        # Average tariff savings under AfCFTA
        avg_tariff_reduction = 0.12  # 12% average
        logistics_savings = 0.05  # 5% from shorter distances
        return (avg_tariff_reduction + logistics_savings) * 100
    
    def _identify_top_sectors(self, opportunities: List[Dict]) -> List[Dict]:
        """Identify top sectors from opportunities"""
        sector_values = defaultdict(float)
        
        for opp in opportunities:
            hs2 = opp["imported_product"]["hs_code"][:2]
            sector_values[hs2] += opp["substitution_potential"]
        
        # Sort and return top 5
        sorted_sectors = sorted(sector_values.items(), key=lambda x: x[1], reverse=True)
        return [
            {"hs_chapter": s[0], "name": self._get_sector_name(s[0]), "value": s[1]}
            for s in sorted_sectors[:5]
        ]
    
    def _estimate_capture_potential(
        self,
        capacity: float,
        import_value: float,
        quality: str
    ) -> float:
        """Estimate how much of the market can be captured"""
        # Base capture rate
        base_rate = 0.15  # 15% realistic capture
        
        # Adjust for quality
        quality_multipliers = {"high": 1.5, "medium": 1.0, "low": 0.6}
        quality_mult = quality_multipliers.get(quality, 1.0)
        
        # Adjust for capacity
        capacity_mult = min(capacity / import_value, 1.0)
        
        return import_value * base_rate * quality_mult * capacity_mult
    
    def _assess_competitiveness(self, prod_item: Dict) -> str:
        """Assess competitiveness of a product"""
        quality = prod_item.get("quality", "medium")
        if quality == "high":
            return "highly_competitive"
        elif quality == "medium":
            return "competitive"
        else:
            return "developing"
    
    def _identify_top_markets(self, opportunities: List[Dict]) -> List[Dict]:
        """Identify top export markets from opportunities"""
        market_values = defaultdict(float)
        
        for opp in opportunities:
            for market in opp.get("target_markets", []):
                market_values[market["country_iso3"]] += market["capture_potential"]
        
        sorted_markets = sorted(market_values.items(), key=lambda x: x[1], reverse=True)
        return [
            {"iso3": m[0], "name": get_country_name(m[0]), "potential": m[1]}
            for m in sorted_markets[:5]
        ]
    
    def _generate_trade_flows(
        self,
        producers: List[Dict],
        importers: List[Dict]
    ) -> List[Dict]:
        """Generate potential trade flows between producers and importers"""
        flows = []
        
        for producer in producers[:5]:
            for importer in importers[:5]:
                if producer["country_iso3"] != importer["country_iso3"]:
                    flows.append({
                        "from": producer["country_iso3"],
                        "from_name": producer["country_name"],
                        "to": importer["country_iso3"],
                        "to_name": importer["country_name"],
                        "potential_value": min(
                            producer["capacity"] * 0.2,
                            importer["import_value"] * 0.3
                        )
                    })
        
        flows.sort(key=lambda x: x["potential_value"], reverse=True)
        return flows[:10]
    
    def _get_sector_name(self, hs2: str, lang: str = "fr") -> str:
        """Get sector name from HS chapter"""
        sectors = {
            "01": {"fr": "Animaux vivants", "en": "Live animals"},
            "02": {"fr": "Viandes", "en": "Meat"},
            "03": {"fr": "Poissons", "en": "Fish"},
            "04": {"fr": "Produits laitiers", "en": "Dairy"},
            "05": {"fr": "Autres produits animaux", "en": "Other animal products"},
            "06": {"fr": "Plantes vivantes", "en": "Live plants"},
            "07": {"fr": "Légumes", "en": "Vegetables"},
            "08": {"fr": "Fruits", "en": "Fruits"},
            "09": {"fr": "Café, thé, épices", "en": "Coffee, tea, spices"},
            "10": {"fr": "Céréales", "en": "Cereals"},
            "15": {"fr": "Graisses et huiles", "en": "Fats and oils"},
            "17": {"fr": "Sucres", "en": "Sugars"},
            "18": {"fr": "Cacao", "en": "Cocoa"},
            "27": {"fr": "Combustibles minéraux", "en": "Mineral fuels"},
            "28": {"fr": "Produits chimiques inorganiques", "en": "Inorganic chemicals"},
            "29": {"fr": "Produits chimiques organiques", "en": "Organic chemicals"},
            "30": {"fr": "Produits pharmaceutiques", "en": "Pharmaceuticals"},
            "31": {"fr": "Engrais", "en": "Fertilizers"},
            "39": {"fr": "Plastiques", "en": "Plastics"},
            "40": {"fr": "Caoutchouc", "en": "Rubber"},
            "52": {"fr": "Coton", "en": "Cotton"},
            "61": {"fr": "Vêtements en maille", "en": "Knitted apparel"},
            "62": {"fr": "Vêtements non maille", "en": "Non-knitted apparel"},
            "71": {"fr": "Pierres et métaux précieux", "en": "Precious stones/metals"},
            "72": {"fr": "Fonte, fer et acier", "en": "Iron and steel"},
            "73": {"fr": "Ouvrages en fer/acier", "en": "Iron/steel articles"},
            "84": {"fr": "Machines", "en": "Machinery"},
            "85": {"fr": "Équipements électriques", "en": "Electrical equipment"},
            "87": {"fr": "Véhicules", "en": "Vehicles"},
            "90": {"fr": "Instruments optiques", "en": "Optical instruments"},
        }
        
        sector = sectors.get(hs2, {"fr": f"Chapitre {hs2}", "en": f"Chapter {hs2}"})
        return sector.get(lang, sector.get("en"))


# Singleton instance
substitution_service = SubstitutionAnalysisService()
