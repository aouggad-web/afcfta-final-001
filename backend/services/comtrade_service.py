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
    UN COMTRADE API Service
    Free tier: 500 calls/day, 100K records per call
    """
    
    BASE_URL = "https://comtradeplus.un.org/api/get"
    
    def __init__(self):
        self.api_key = os.getenv("COMTRADE_API_KEY", "")
        self.calls_today = 0
        self.max_calls_per_day = 500
        
    def get_bilateral_trade(
        self,
        reporter_code: str,
        partner_code: str,
        period: str,
        hs_code: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get bilateral trade data between two countries
        
        Args:
            reporter_code: ISO3 country code (reporter)
            partner_code: ISO3 country code (partner)
            period: Year or YYYYMM format
            hs_code: Optional HS code for specific product
            
        Returns:
            Trade data dictionary or None if error
        """
        if self.calls_today >= self.max_calls_per_day:
            raise Exception("COMTRADE API daily limit reached")
            
        params = {
            "reporterCode": reporter_code,
            "partnerCode": partner_code,
            "period": period,
            "motCode": "C",  # Mode of transport: All
            "freqCode": "A",  # Annual
        }
        
        if hs_code:
            params["cmdCode"] = hs_code
            
        if self.api_key:
            params["subscription-key"] = self.api_key
            
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            self.calls_today += 1
            
            data = response.json()
            return {
                "source": "UN_COMTRADE",
                "data": data.get("data", []),
                "metadata": data.get("metadata", {}),
                "timestamp": datetime.utcnow().isoformat(),
                "latest_period": period
            }
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
            african_countries: List of ISO3 country codes
            period: Year or YYYYMM
            
        Returns:
            List of trade data
        """
        results = []
        
        for reporter in african_countries:
            if self.calls_today >= self.max_calls_per_day:
                logger.warning(f"API limit reached after {len(results)} countries")
                break
                
            data = self.get_bilateral_trade(
                reporter_code=reporter,
                partner_code="all",
                period=period
            )
            
            if data:
                results.append(data)
                
            # Rate limiting
            time.sleep(0.2)
            
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
                partner_code="wld",  # World
                period=str(year)
            )
            
            if test_data and test_data.get("data"):
                return str(year)
                
        return None


# Global service instance
comtrade_service = COMTRADEService()
