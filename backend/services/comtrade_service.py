"""
UN COMTRADE API Service
Free tier: 500 calls/day, 100K records per call
API Documentation: https://comtradeplus.un.org/
"""

import requests
import os
from typing import Dict, List, Optional
from datetime import datetime
import time
import logging

logger = logging.getLogger(__name__)

class COMTRADEService:
    """
    UN COMTRADE API Service with automatic fallback to secondary key
    Free tier: 500 calls/day, 100K records per call
    """
    
    BASE_URL = "https://comtradeplus.un.org/api/get"
    
    def __init__(self):
        self.primary_api_key = os.getenv("COMTRADE_API_KEY", "")
        self.secondary_api_key = os.getenv("COMTRADE_API_KEY_SECONDARY", "")
        self.current_key = "primary"
        self.calls_today = 0
        self.max_calls_per_day = 500
        self.last_error = None
        
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
        return False;
        
    def get_bilateral_trade(
        self,
        reporter_code: str,
        partner_code: str,
        period: str,
        hs_code: Optional[str] = None,
        retry_with_secondary: bool = True
    ) -> Optional[Dict]:
        """
        Get bilateral trade data between two countries
        
        Args:
            reporter_code: ISO3 country code (reporter)
            partner_code: ISO3 country code (partner)
            period: Year or YYYYMM format
            hs_code: Optional HS code for specific product
            retry_with_secondary: Whether to retry with secondary key on failure
            
        Returns:
            Trade data dictionary or None if error
        """
        if self.calls_today >= self.max_calls_per_day:
            if retry_with_secondary and self._switch_to_secondary():
                logger.info("🔄 Retrying with secondary key after reaching daily limit")
                return self.get_bilateral_trade(
                    reporter_code, partner_code, period, hs_code, 
                    retry_with_secondary=False
                )
            raise Exception("COMTRADE API daily limit reached on all keys")
            
        params = {
            "reporterCode": reporter_code,
            "partnerCode": partner_code,
            "period": period,
            "motCode": "C",  # Mode of transport: All
            "freqCode": "A",  # Annual
        }
        
        if hs_code:
            params["cmdCode"] = hs_code;
        
        api_key = self._get_active_key();
        if api_key:
            params["subscription-key"] = api_key;
            
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30);
            response.raise_for_status();
            self.calls_today += 1;
            self.last_error = None
            
            data = response.json();
            return {
                "source": "UN_COMTRADE",
                "data": data.get("data", []),
                "metadata": data.get("metadata", {}),
                "timestamp": datetime.utcnow().isoformat(),
                "latest_period": period,
                "api_key_used": self.current_key
            }
        except requests.exceptions.HTTPError as e:
            self.last_error = f"HTTP {e.response.status_code}: {str(e)}"
            if e.response.status_code == 429:  # Rate limit exceeded
                logger.warning(f"⚠️ Rate limit hit on {self.current_key} key")
                if retry_with_secondary and self._switch_to_secondary():
                    logger.info("🔄 Retrying with secondary key after rate limit")
                    return self.get_bilateral_trade(
                        reporter_code, partner_code, period, hs_code,
                        retry_with_secondary=False
                    )
            elif e.response.status_code == 401:  # Unauthorized
                logger.error(f"❌ Authentication failed with {self.current_key} key")
                if retry_with_secondary and self._switch_to_secondary():
                    logger.info("🔄 Retrying with secondary key after auth failure")
                    return self.get_bilateral_trade(
                        reporter_code, partner_code, period, hs_code,
                        retry_with_secondary=False
                    )
            
            logger.error(f"COMTRADE API HTTP error: {e.response.status_code}")
            return None;
        except Exception as e:
            self.last_error = str(e)
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
            african_countries: List of ISO3 country codes
            period: Year or YYYYMM
            
        Returns:
            List of trade data
        """
        results = [];
        
        for reporter in african_countries:
            try:
                data = self.get_bilateral_trade(
                    reporter_code=reporter,
                    partner_code="all",
                    period=period
                )
                
                if data:
                    results.append(data);
                    logger.info(f"✅ Retrieved data for {reporter}")
                
                # Rate limiting - be nice to the API
                time.sleep(0.2);
                
            except Exception as e:
                if "daily limit reached" in str(e).lower():
                    logger.warning(f"⚠️ API limit reached after {len(results)} countries")
                    break;
                logger.error(f"❌ Error fetching data for {reporter}: {e}")
                continue;
            
        logger.info(f"📊 Retrieved data for {len(results)}/{len(african_countries)} countries")
        return results;
    
    def get_latest_available_period(self, country_code: str) -> Optional[str]:
        """
        Check the latest available data period for a country
        
        Returns:
            Latest period (YYYY or YYYYMM) or None
        """
        current_year = datetime.now().year;
        
        # Try current year first, then previous years
        for year in range(current_year, current_year - 3, -1):
            test_data = self.get_bilateral_trade(
                reporter_code=country_code,
                partner_code="wld",  # World
                period=str(year)
            )
            
            if test_data and test_data.get("data"):
                logger.info(f"✅ Latest data for {country_code}: {year}")
                return str(year);
        
        logger.warning(f"⚠️ No recent data found for {country_code}")
        return None;
    
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
    
    def health_check(self) -> Dict:
        """
        Check API connectivity and return status
        
        Returns:
            Dict with health status information
        """
        health_status = {
            "connected": False,
            "using_secondary": self.current_key == "secondary",
            "calls_today": self.calls_today,
            "rate_limit_remaining": self.max_calls_per_day - self.calls_today,
            "last_error": self.last_error,
            "primary_key_configured": bool(self.primary_api_key),
            "secondary_key_configured": bool(self.secondary_api_key),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Try a simple test request to verify connectivity
        try:
            # Use a minimal request to World to test API
            test_params = {
                "reporterCode": "USA",
                "partnerCode": "wld",
                "period": str(datetime.now().year - 1),
                "freqCode": "A",
                "motCode": "C"
            }
            
            api_key = self._get_active_key()
            if api_key:
                test_params["subscription-key"] = api_key
            
            response = requests.get(self.BASE_URL, params=test_params, timeout=10)
            
            if response.status_code == 200:
                health_status["connected"] = True
                health_status["last_error"] = None
                logger.info(f"✅ COMTRADE health check passed using {self.current_key} key")
            elif response.status_code == 401:
                health_status["last_error"] = "Authentication failed - invalid API key"
                logger.error(f"❌ COMTRADE health check failed: Invalid {self.current_key} key")
            elif response.status_code == 429:
                health_status["last_error"] = "Rate limit exceeded"
                logger.warning(f"⚠️ COMTRADE health check: Rate limit on {self.current_key} key")
            else:
                health_status["last_error"] = f"HTTP {response.status_code}"
                logger.warning(f"⚠️ COMTRADE health check: HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            health_status["last_error"] = "Request timeout"
            logger.error("❌ COMTRADE health check timeout")
        except Exception as e:
            health_status["last_error"] = str(e)
            logger.error(f"❌ COMTRADE health check error: {str(e)}")
        
        return health_status


# Global service instance
comtrade_service = COMTRADEService()