"""
WTO Data Portal API Service
Free access to tariff and trade data
API Documentation: https://data.wto.org/
"""

import requests
import time
from typing import Dict, Optional
from datetime import datetime
from requests.exceptions import HTTPError
import logging

logger = logging.getLogger(__name__)


def make_wto_request_with_retry(url, params=None, max_retries=5):
    """
    Make WTO API request with exponential backoff for rate limits
    
    Args:
        url: API endpoint URL
        params: Optional query parameters
        max_retries: Maximum number of retry attempts (default: 5)
    
    Returns:
        Response object or None if all retries failed
    """
    def calculate_backoff(attempt):
        """
        Calculate exponential backoff wait time.
        Returns wait times: 2, 4, 8, 16, 32 seconds for attempts 0-4.
        These are the delays between retries, not including the final failed attempt.
        """
        return (2 ** attempt) * 2
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response
        except HTTPError as e:
            if e.response.status_code == 429:  # Rate limit
                if attempt < max_retries - 1:
                    wait_time = calculate_backoff(attempt)
                    logger.warning(f"⚠️ Rate limit hit (429), retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"❌ Rate limit exceeded after {max_retries} attempts")
                    return None
            elif e.response.status_code == 400:
                logger.warning(f"⚠️ Bad request (400) for URL: {url}. Skipping...")
                return None
            elif e.response.status_code == 401:
                logger.warning(f"⚠️ Unauthorized (401) for URL: {url}. Check API credentials. Skipping...")
                return None
            else:
                logger.error(f"❌ HTTP error {e.response.status_code}: {e}")
                return None
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = calculate_backoff(attempt)
                logger.warning(f"⚠️ Request timeout, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                logger.error(f"❌ Request timed out after {max_retries} attempts")
                return None
        except Exception as e:
            logger.error(f"❌ Error fetching data: {e}")
            return None
    
    # This line should never be reached as all paths in the loop return
    return None


class WTOService:
    """
    WTO Data Portal API Service
    Free access to tariff and trade data
    """
    
    BASE_URL = "https://api.wto.org/timeseries/v1"
    
    def __init__(self):
        pass
    
    def get_tariff_data(
        self,
        reporter_code: str,
        partner_code: str,
        product_code: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get tariff data from WTO
        
        Args:
            reporter_code: ISO3 country code
            partner_code: ISO3 partner code
            product_code: HS code
            
        Returns:
            Tariff data dictionary or None if error
        """
        endpoint = f"{self.BASE_URL}/data"
        
        params = {
            "i": "IDB_MFN_SMPL",  # Indicator: MFN Simple Average
            "r": reporter_code,
            "p": partner_code,
            "fmt": "json"
        }
        
        if product_code:
            params["pc"] = product_code
            
        try:
            response = make_wto_request_with_retry(endpoint, params=params, max_retries=5)
            
            if response is None:
                return None
            
            data = response.json()
            
            # Extract latest year
            dataset = data.get("Dataset", {})
            series = dataset.get("Series", [])
            
            latest_year = None
            if series:
                observations = series[0].get("Obs", [])
                if observations:
                    latest_year = observations[-1].get("Time")
            
            return {
                "source": "WTO",
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "latest_period": latest_year
            }
        except Exception as e:
            logger.error(f"WTO API error: {str(e)}")
            return None
    
    def get_trade_indicators(
        self,
        country_code: str,
        indicator: str = "TRADE_VALUE"
    ) -> Optional[Dict]:
        """
        Get trade indicators from WTO
        
        Args:
            country_code: ISO3 country code
            indicator: Trade indicator type
            
        Returns:
            Trade indicator data or None if error
        """
        endpoint = f"{self.BASE_URL}/data"
        
        params = {
            "i": indicator,
            "r": country_code,
            "fmt": "json"
        }
        
        try:
            response = make_wto_request_with_retry(endpoint, params=params, max_retries=5)
            
            if response is None:
                return None
            
            data = response.json()
            return {
                "source": "WTO",
                "indicator": indicator,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"WTO API error: {str(e)}")
            return None
    
    def get_latest_available_year(self, country_code: str) -> Optional[str]:
        """
        Get the latest available year for a country in WTO database
        
        Returns:
            Latest year as string or None
        """
        data = self.get_tariff_data(country_code, "wld")
        
        if data and data.get("latest_period"):
            return data["latest_period"]
            
        return None


# Global service instance
wto_service = WTOService()
