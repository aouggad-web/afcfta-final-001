"""
WTO Data Portal API Service
Free access to tariff and trade data
API Documentation: https://data.wto.org/
"""

import requests
from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


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
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
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
            response = requests.get(endpoint, params=params, timeout=30)
            response.raise_for_status()
            
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
