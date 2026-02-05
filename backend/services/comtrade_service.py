"""
UN COMTRADE API Service
Free tier: 500 calls/day, 100K records per call
API Documentation: https://comtradeplus.un.org/
Provides more recent trade data than OEC (monthly updates vs annual)
"""

import os
import logging
from typing import Dict, List, Optional
from datetime import datetime
import time
import httpx
import asyncio

logger = logging.getLogger(__name__)


class COMTRADEService:
    """
    UN COMTRADE API Service
    Free tier: 500 calls/day, 100K records per call
    More recent data than OEC (monthly updates)
    """
    
    BASE_URL = "https://comtradeapi.un.org/public/v1/preview"
    
    def __init__(self):
        self.api_key = os.getenv("COMTRADE_API_KEY", "")
        self.calls_today = 0
        self.max_calls_per_day = 500
        self._cache = {}
        self._cache_ttl = 3600  # 1 hour cache
        
    def _get_cache_key(self, *args) -> str:
        """Generate cache key from arguments"""
        return "-".join(str(a) for a in args)
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache entry is still valid"""
        if key not in self._cache:
            return False
        entry = self._cache[key]
        return (datetime.utcnow() - entry["timestamp"]).seconds < self._cache_ttl
    
    async def get_bilateral_trade(
        self,
        reporter_code: str,
        partner_code: str = "0",  # 0 = World
        period: str = None,
        hs_code: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get bilateral trade data between two countries
        
        Args:
            reporter_code: ISO3 country code or M49 numeric code (reporter)
            partner_code: ISO3 country code or M49 numeric code (partner), "0" for World
            period: Year (YYYY) format
            hs_code: Optional HS code for specific product (AG2, AG4, AG6)
            
        Returns:
            Trade data dictionary or None if error
        """
        if self.calls_today >= self.max_calls_per_day:
            logger.warning("COMTRADE API daily limit reached")
            return None
        
        # Default to current year if not specified
        if not period:
            period = str(datetime.now().year - 1)  # Use previous year for complete data
        
        # Build cache key
        cache_key = self._get_cache_key("bilateral", reporter_code, partner_code, period, hs_code or "all")
        if self._is_cache_valid(cache_key):
            logger.debug(f"Cache hit for {cache_key}")
            return self._cache[cache_key]["data"]
        
        # Build API URL - using preview endpoint (no auth needed)
        url = f"{self.BASE_URL}/tariffline/C/A/{reporter_code}/{period}"
        
        params = {
            "partnerCode": partner_code,
            "motCode": "0",  # All modes of transport
        }
        
        if hs_code:
            params["cmdCode"] = hs_code
            
        headers = {}
        if self.api_key:
            headers["Ocp-Apim-Subscription-Key"] = self.api_key
            
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params, headers=headers)
                self.calls_today += 1
                
                if response.status_code == 200:
                    data = response.json()
                    
                    result = {
                        "source": "UN_COMTRADE",
                        "data": data.get("data", []),
                        "count": data.get("count", 0),
                        "metadata": {
                            "reporter": reporter_code,
                            "partner": partner_code,
                            "period": period,
                            "hs_code": hs_code
                        },
                        "timestamp": datetime.utcnow().isoformat(),
                        "latest_period": period
                    }
                    
                    # Cache the result
                    self._cache[cache_key] = {
                        "data": result,
                        "timestamp": datetime.utcnow()
                    }
                    
                    return result
                    
                elif response.status_code == 404:
                    logger.info(f"No COMTRADE data for {reporter_code}/{period}")
                    return None
                else:
                    logger.error(f"COMTRADE API error: {response.status_code} - {response.text[:200]}")
                    return None
                    
        except Exception as e:
            logger.error(f"COMTRADE API error: {str(e)}")
            return None
    
    async def get_trade_summary(
        self,
        reporter_code: str,
        period: str = None
    ) -> Optional[Dict]:
        """
        Get trade summary (total exports/imports) for a country
        
        Args:
            reporter_code: ISO3 or M49 country code
            period: Year (YYYY)
            
        Returns:
            Summary with total exports and imports
        """
        if not period:
            period = str(datetime.now().year - 1)
            
        cache_key = self._get_cache_key("summary", reporter_code, period)
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]["data"]
        
        # Get exports (flowCode=X)
        exports_url = f"{self.BASE_URL}/tariffline/C/A/{reporter_code}/{period}"
        # Get imports (flowCode=M)
        imports_url = f"{self.BASE_URL}/tariffline/C/A/{reporter_code}/{period}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # Fetch both in parallel
                exports_task = client.get(exports_url, params={"flowCode": "X", "partnerCode": "0"})
                imports_task = client.get(imports_url, params={"flowCode": "M", "partnerCode": "0"})
                
                # Note: We can't truly parallelize with httpx in this simple way
                # Just fetch sequentially for now
                exports_resp = await client.get(exports_url, params={"flowCode": "X", "partnerCode": "0"})
                self.calls_today += 1
                
                imports_resp = await client.get(imports_url, params={"flowCode": "M", "partnerCode": "0"})
                self.calls_today += 1
                
                exports_total = 0
                imports_total = 0
                
                if exports_resp.status_code == 200:
                    exports_data = exports_resp.json().get("data", [])
                    exports_total = sum(r.get("primaryValue", 0) for r in exports_data)
                
                if imports_resp.status_code == 200:
                    imports_data = imports_resp.json().get("data", [])
                    imports_total = sum(r.get("primaryValue", 0) for r in imports_data)
                
                result = {
                    "source": "UN_COMTRADE",
                    "reporter": reporter_code,
                    "period": period,
                    "total_exports_usd": exports_total,
                    "total_imports_usd": imports_total,
                    "trade_balance_usd": exports_total - imports_total,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                self._cache[cache_key] = {
                    "data": result,
                    "timestamp": datetime.utcnow()
                }
                
                return result
                
        except Exception as e:
            logger.error(f"COMTRADE summary error: {str(e)}")
            return None
    
    async def get_african_trade_data(
        self,
        african_country_codes: List[str],
        period: str = None
    ) -> List[Dict]:
        """
        Get trade data for multiple African countries
        
        Args:
            african_country_codes: List of ISO3 country codes
            period: Year (YYYY)
            
        Returns:
            List of trade data per country
        """
        if not period:
            period = str(datetime.now().year - 1)
            
        results = []
        
        for country_code in african_country_codes:
            if self.calls_today >= self.max_calls_per_day:
                logger.warning(f"API limit reached after {len(results)} countries")
                break
                
            data = await self.get_bilateral_trade(
                reporter_code=country_code,
                partner_code="0",  # World
                period=period
            )
            
            if data:
                results.append({
                    "country": country_code,
                    **data
                })
                
            # Rate limiting
            await self._rate_limit_delay()
            
        return results
    
    async def get_product_trade(
        self,
        hs_code: str,
        period: str = None,
        flow: str = "X"  # X=exports, M=imports
    ) -> List[Dict]:
        """
        Get trade data for a specific product across African countries
        
        Args:
            hs_code: HS code (2, 4, or 6 digits)
            period: Year (YYYY)
            flow: "X" for exports, "M" for imports
            
        Returns:
            List of country trade data for the product
        """
        if not period:
            period = str(datetime.now().year - 1)
        
        # Major African trading countries to sample
        major_traders = ["ZAF", "EGY", "NGA", "MAR", "DZA", "KEN", "ETH", "GHA", "TUN", "CIV"]
        
        results = []
        
        for country in major_traders:
            if self.calls_today >= self.max_calls_per_day:
                break
                
            data = await self.get_bilateral_trade(
                reporter_code=country,
                partner_code="0",
                period=period,
                hs_code=hs_code
            )
            
            if data and data.get("data"):
                # Calculate total for this product
                trade_value = sum(r.get("primaryValue", 0) for r in data["data"] if r.get("flowCode") == flow)
                
                if trade_value > 0:
                    results.append({
                        "country_iso3": country,
                        "hs_code": hs_code,
                        "trade_value_usd": trade_value,
                        "flow": "export" if flow == "X" else "import",
                        "period": period,
                        "source": "UN_COMTRADE"
                    })
            
            await self._rate_limit_delay()
        
        # Sort by trade value
        results.sort(key=lambda x: x["trade_value_usd"], reverse=True)
        
        return results
    
    async def get_latest_available_period(self, country_code: str) -> Optional[str]:
        """
        Check the latest available data period for a country
        
        Returns:
            Latest period (YYYY) or None
        """
        current_year = datetime.now().year
        
        # Try current year first, then previous years
        for year in range(current_year, current_year - 3, -1):
            data = await self.get_bilateral_trade(
                reporter_code=country_code,
                partner_code="0",
                period=str(year)
            )
            
            if data and data.get("data"):
                return str(year)
                
            await self._rate_limit_delay()
                
        return None
    
    async def _rate_limit_delay(self):
        """Add delay between requests to respect rate limits"""
        await asyncio.sleep(0.2)  # 200ms between requests


# Global service instance
comtrade_service = COMTRADEService()
