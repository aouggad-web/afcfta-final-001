"""
WTO (World Trade Organization) API Service
Provides tariff data and trade policy information
API Documentation: https://apiportal.wto.org/
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class WTOService:
    """
    WTO API Service for tariff and trade policy data
    Free public access available
    """
    
    BASE_URL = "https://api.wto.org/timeseries/v1"
    
    def __init__(self):
        self.api_key = os.getenv("WTO_API_KEY", "")
        self._cache = {}
        self._cache_ttl = 7200  # 2 hours cache (tariffs don't change often)
        
    def _get_cache_key(self, *args) -> str:
        return "-".join(str(a) for a in args)
    
    def _is_cache_valid(self, key: str) -> bool:
        if key not in self._cache:
            return False
        entry = self._cache[key]
        return (datetime.utcnow() - entry["timestamp"]).seconds < self._cache_ttl
    
    async def get_tariff_data(
        self,
        reporter: str,
        partner: str = None,
        hs_code: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get tariff data for a country
        
        Args:
            reporter: ISO3 country code
            partner: Optional ISO3 partner country code
            hs_code: Optional HS product code
            
        Returns:
            Tariff data dictionary
        """
        cache_key = self._get_cache_key("tariff", reporter, partner or "all", hs_code or "all")
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]["data"]
        
        # Build indicator code for MFN tariffs
        indicator = "HS_M_0010"  # MFN Applied Duties
        
        params = {
            "i": indicator,
            "r": reporter,
            "ps": "last",  # Latest available
            "max": 500
        }
        
        if partner:
            params["p"] = partner
        if hs_code:
            params["pc"] = hs_code
        
        headers = {}
        if self.api_key:
            headers["Ocp-Apim-Subscription-Key"] = self.api_key
            
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/data",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    result = {
                        "source": "WTO",
                        "data": data.get("Dataset", []),
                        "metadata": {
                            "reporter": reporter,
                            "partner": partner,
                            "hs_code": hs_code,
                            "indicator": indicator
                        },
                        "timestamp": datetime.utcnow().isoformat(),
                        "latest_period": self._extract_latest_period(data.get("Dataset", []))
                    }
                    
                    self._cache[cache_key] = {
                        "data": result,
                        "timestamp": datetime.utcnow()
                    }
                    
                    return result
                    
                elif response.status_code == 401:
                    logger.warning("WTO API: Unauthorized - API key may be required")
                    return None
                else:
                    logger.error(f"WTO API error: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.error(f"WTO API error: {str(e)}")
            return None
    
    async def get_mfn_average(
        self,
        country_code: str,
        product_group: str = None
    ) -> Optional[Dict]:
        """
        Get MFN (Most Favored Nation) average tariff for a country
        
        Args:
            country_code: ISO3 country code
            product_group: Optional product group (AG=Agriculture, NAMA=Non-Agricultural)
            
        Returns:
            Average tariff information
        """
        cache_key = self._get_cache_key("mfn_avg", country_code, product_group or "all")
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]["data"]
        
        # Use simple average indicator
        indicator = "HS_M_0020"  # Simple Average MFN
        
        params = {
            "i": indicator,
            "r": country_code,
            "ps": "last",
            "max": 100
        }
        
        if product_group:
            params["pc"] = product_group
            
        headers = {}
        if self.api_key:
            headers["Ocp-Apim-Subscription-Key"] = self.api_key
            
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.BASE_URL}/data",
                    params=params,
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    dataset = data.get("Dataset", [])
                    
                    # Extract average from dataset
                    avg_tariff = None
                    year = None
                    
                    for record in dataset:
                        if record.get("Value"):
                            avg_tariff = float(record["Value"])
                            year = record.get("Year")
                            break
                    
                    result = {
                        "source": "WTO",
                        "country": country_code,
                        "mfn_average_percent": avg_tariff,
                        "product_group": product_group or "all",
                        "year": year,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    
                    self._cache[cache_key] = {
                        "data": result,
                        "timestamp": datetime.utcnow()
                    }
                    
                    return result
                    
        except Exception as e:
            logger.error(f"WTO MFN average error: {str(e)}")
            return None
    
    async def get_afcfta_tariff_comparison(
        self,
        country_code: str,
        hs_code: str
    ) -> Optional[Dict]:
        """
        Compare MFN tariff vs AfCFTA tariff (typically 0%)
        
        Args:
            country_code: ISO3 country code
            hs_code: HS product code
            
        Returns:
            Comparison showing tariff reduction potential
        """
        mfn_data = await self.get_tariff_data(country_code, hs_code=hs_code)
        
        if not mfn_data or not mfn_data.get("data"):
            return None
            
        # Extract MFN rate
        mfn_rate = None
        for record in mfn_data["data"]:
            if record.get("Value"):
                mfn_rate = float(record["Value"])
                break
        
        if mfn_rate is None:
            return None
            
        # AfCFTA rate is typically 0% for most products (after full implementation)
        afcfta_rate = 0.0
        
        return {
            "country": country_code,
            "hs_code": hs_code,
            "mfn_rate_percent": mfn_rate,
            "afcfta_rate_percent": afcfta_rate,
            "tariff_reduction_percent": mfn_rate - afcfta_rate,
            "savings_description": f"Économie de {mfn_rate:.1f}% sous la ZLECAf",
            "source": "WTO + AfCFTA TRS",
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_latest_available_year(self, country_code: str) -> Optional[str]:
        """
        Get the latest year with available tariff data
        
        Args:
            country_code: ISO3 country code
            
        Returns:
            Latest year as string (e.g., "2023")
        """
        data = await self.get_tariff_data(country_code)
        
        if data and data.get("latest_period"):
            return data["latest_period"]
            
        return None
    
    def _extract_latest_period(self, dataset: List[Dict]) -> Optional[str]:
        """Extract the latest year from dataset records"""
        years = [r.get("Year") for r in dataset if r.get("Year")]
        if years:
            return str(max(int(y) for y in years if y.isdigit()))
        return None


# Global service instance
wto_service = WTOService()
