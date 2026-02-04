"""
UN COMTRADE API Service (v1 API)
API Documentation: https://uncomtrade.org/docs/
OpenAPI Spec: https://comtradeapi.un.org/data/v1/openapi.json
Subscription required - Learn more at https://uncomtrade.org/docs/subscriptions/
"""

import requests
import os
from typing import Dict, List, Optional
from datetime import datetime, timezone
import time
import logging

logger = logging.getLogger(__name__)

class COMTRADEService:
    """
    UN COMTRADE v1 API Service with automatic fallback to secondary key
    Requires subscription - see https://uncomtrade.org/docs/subscriptions/
    """
    
    BASE_URL = "https://comtradeapi.un.org/data/v1"
    
    def __init__(self):
        self.primary_api_key = os.getenv("COMTRADE_API_KEY", "")
        self.secondary_api_key = os.getenv("COMTRADE_API_KEY_SECONDARY", "")
        self.current_key = "primary"
        self.calls_today = 0
        self.max_calls_per_day = 500
        
        if not self.primary_api_key and not self.secondary_api_key:
            logger.warning("⚠️ No COMTRADE API keys configured")
        elif self.primary_api_key and self.secondary_api_key:
            logger.info("✅ COMTRADE: Primary and secondary keys loaded")
        elif self.primary_api_key:
            logger.info("✅ COMTRADE: Primary key loaded (no secondary)")
        else:
            logger.info("✅ COMTRADE: Secondary key loaded (no primary)")
    
    def _get_active_key(self) -> str:
        """Get the currently active API key"""
        if self.current_key == "primary" and self.primary_api_key:
            return self.primary_api_key
        elif self.secondary_api_key:
            return self.secondary_api_key
        return ""
    
    def _switch_to_secondary(self):
        """Switch to secondary API key when primary fails or reaches limit"""
        if self.secondary_api_key and self.current_key == "primary":
            logger.info("🔄 Switching from primary to secondary COMTRADE API key")
            self.current_key = "secondary"
            self.calls_today = 0  # Reset counter for new key
            return True
        return False
        
    def get_bilateral_trade(
        self,
        reporter_code: str,
        partner_code: str,
        period: str,
        hs_code: Optional[str] = None,
        type_code: str = "C",
        freq_code: str = "A",
        cl_code: str = "HS",
        retry_with_secondary: bool = True
    ) -> Optional[Dict]:
        """
        Get bilateral trade data between two countries using v1 API
        
        Args:
            reporter_code: M49 country code (reporter)
            partner_code: M49 country code (partner) or 'all' for all partners
            period: Year (YYYY) or Month (YYYYMM) format
            hs_code: Optional HS commodity code
            type_code: Type of trade - 'C' for commodities, 'S' for services (default: 'C')
            freq_code: Frequency - 'A' for annual, 'M' for monthly (default: 'A')
            cl_code: Classification - 'HS', 'SITC', etc. (default: 'HS')
            retry_with_secondary: Whether to retry with secondary key on failure
            
        Returns:
            Trade data dictionary or None if error
        """
        if self.calls_today >= self.max_calls_per_day:
            if retry_with_secondary and self._switch_to_secondary():
                logger.info("🔄 Retrying with secondary key after reaching daily limit")
                return self.get_bilateral_trade(
                    reporter_code, partner_code, period, hs_code, 
                    type_code, freq_code, cl_code,
                    retry_with_secondary=False
                )
            raise Exception("COMTRADE API daily limit reached on all keys")
        
        # Build v1 API URL: /get/{typeCode}/{freqCode}/{clCode}
        url = f"{self.BASE_URL}/get/{type_code}/{freq_code}/{cl_code}"
        
        params = {
            "reporterCode": reporter_code,
            "partnerCode": partner_code,
            "period": period,
        }
        
        if hs_code:
            params["cmdCode"] = hs_code
        
        # Add API key using header (v1 API uses header-based auth)
        api_key = self._get_active_key()
        headers = {}
        if api_key:
            headers["Ocp-Apim-Subscription-Key"] = api_key
            
        # Retry logic with exponential backoff for rate limiting
        max_retries = 3
        backoff_factor = 2
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, headers=headers, timeout=30)
                response.raise_for_status()
                self.calls_today += 1
                
                data = response.json()
                return {
                    "source": "UN_COMTRADE",
                    "data": data.get("data", []),
                    "metadata": data.get("metadata", {}),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "latest_period": period,
                    "api_key_used": self.current_key
                }
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit exceeded
                    logger.warning(f"⚠️ Rate limit hit on {self.current_key} key (attempt {attempt + 1}/{max_retries})")
                    
                    # First try switching to secondary key
                    if retry_with_secondary and self._switch_to_secondary():
                        logger.info("🔄 Retrying with secondary key after rate limit")
                        return self.get_bilateral_trade(
                            reporter_code, partner_code, period, hs_code,
                            type_code, freq_code, cl_code,
                            retry_with_secondary=False
                        )
                    
                    # If no secondary key or already using it, apply exponential backoff
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor ** (attempt + 1)  # 2s, 4s, 8s
                        logger.info(f"⏳ Waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"❌ Rate limit exceeded after {max_retries} attempts")
                        return None
                        
                elif e.response.status_code == 401:  # Unauthorized
                    logger.error(f"❌ Authentication failed with {self.current_key} key. Check API credentials.")
                    if retry_with_secondary and self._switch_to_secondary():
                        logger.info("🔄 Retrying with secondary key after auth failure")
                        return self.get_bilateral_trade(
                            reporter_code, partner_code, period, hs_code,
                            type_code, freq_code, cl_code,
                            retry_with_secondary=False
                        )
                    return None
                    
                elif e.response.status_code == 400:  # Bad request
                    logger.error(f"❌ Bad request: {url} with params {params}")
                    return None
                
                logger.error(f"COMTRADE API HTTP error: {e.response.status_code}")
                return None
            except Exception as e:
                logger.error(f"COMTRADE API error: {str(e)}")
                return None
    
    def get_african_trade_data(
        self,
        african_countries: List[str],
        period: str
    ) -> List[Dict]:
        """
        Get trade data for all African countries
        
        Args:
            african_countries: List of M49 country codes
            period: Year (YYYY) or Month (YYYYMM)
            
        Returns:
            List of trade data
        """
        results = []
        
        for reporter in african_countries:
            try:
                data = self.get_bilateral_trade(
                    reporter_code=reporter,
                    partner_code="all",
                    period=period
                )
                
                if data:
                    results.append(data)
                    logger.info(f"✅ Retrieved data for {reporter}")
                
                # Rate limiting - be nice to the API
                time.sleep(0.2)
                
            except Exception as e:
                if "daily limit reached" in str(e).lower():
                    logger.warning(f"⚠️ API limit reached after {len(results)} countries")
                    break
                logger.error(f"❌ Error fetching data for {reporter}: {e}")
                continue
            
        logger.info(f"📊 Retrieved data for {len(results)}/{len(african_countries)} countries")
        return results
    
    def get_latest_available_period(self, country_code: str) -> Optional[str]:
        """
        Check the latest available data period for a country
        
        Returns:
            Latest period (YYYY or YYYYMM) or None
        """
        current_year = datetime.now().year
        
        # Try current year first, then previous years
        for year in range(current_year, current_year - 3, -1):
            test_data = self.get_bilateral_trade(
                reporter_code=country_code,
                partner_code="0",  # World (v1 API uses '0' for world)
                period=str(year)
            )
            
            if test_data and test_data.get("data"):
                logger.info(f"✅ Latest data for {country_code}: {year}")
                return str(year)
        
        logger.warning(f"⚠️ No recent data found for {country_code}")
        return None
    
    def get_service_status(self) -> Dict:
        """
        Get current service status
        
        Returns:
            Dict with service configuration and status
        """
        return {
            "primary_key_configured": bool(self.primary_api_key),
            "secondary_key_configured": bool(self.secondary_api_key),
            "current_key": self.current_key,
            "calls_today": self.calls_today,
            "calls_remaining": self.max_calls_per_day - self.calls_today,
            "can_switch_to_secondary": bool(self.secondary_api_key) and self.current_key == "primary"
        }
    
    def get_metadata(
        self,
        type_code: str = "C",
        freq_code: str = "A",
        cl_code: str = "HS"
    ) -> Optional[Dict]:
        """
        Get metadata for specified trade classification
        
        Args:
            type_code: Type of trade - 'C' for commodities, 'S' for services
            freq_code: Frequency - 'A' for annual, 'M' for monthly
            cl_code: Classification - 'HS', 'SITC', 'BEC', 'EBOPS'
            
        Returns:
            Metadata dictionary or None if error
        """
        url = f"{self.BASE_URL}/getMetadata/{type_code}/{freq_code}/{cl_code}"
        
        api_key = self._get_active_key()
        headers = {}
        if api_key:
            headers["Ocp-Apim-Subscription-Key"] = api_key
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            self.calls_today += 1
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching metadata: {str(e)}")
            return None
    
    def get_live_update(self) -> Optional[Dict]:
        """
        Get live update information from the API
        
        Returns:
            Live update info or None if error
        """
        url = f"{self.BASE_URL}/getLiveUpdate"
        
        api_key = self._get_active_key()
        headers = {}
        if api_key:
            headers["Ocp-Apim-Subscription-Key"] = api_key
        
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            self.calls_today += 1
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching live update: {str(e)}")
            return None


# Global service instance
comtrade_service = COMTRADEService()