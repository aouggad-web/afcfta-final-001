"""
Smart data source selector that chooses the best available source
based on data freshness, availability, and API limits
"""

from typing import Dict, Optional, List
from datetime import datetime
import logging

from .comtrade_service import comtrade_service
from .wto_service import wto_service

logger = logging.getLogger(__name__)

# Try to import OEC service if available
try:
    from .oec_trade_service import oec_service
    HAS_OEC = True
except ImportError:
    HAS_OEC = False
    logger.warning("OEC service not available")


class DataSourceSelector:
    """
    Smart data source selector that chooses the best available source
    based on data freshness, availability, and API limits
    """
    
    def __init__(self):
        self.comtrade = comtrade_service
        self.wto = wto_service
        self.oec = oec_service if HAS_OEC else None
        
    def get_latest_trade_data(
        self,
        reporter: str,
        partner: str,
        hs_code: Optional[str] = None
    ) -> Dict:
        """
        Get the latest available trade data from the best source
        
        Priority order:
        1. UN COMTRADE (most recent, monthly updates, free tier)
        2. OEC (good coverage, needs Pro for latest)
        3. WTO (tariff-focused, annual)
        
        Args:
            reporter: ISO3 reporter country code
            partner: ISO3 partner country code
            hs_code: Optional HS product code
            
        Returns:
            Dictionary with trade data and source information
        """
        results = {
            "reporter": reporter,
            "partner": partner,
            "hs_code": hs_code,
            "sources_checked": [],
            "data": None,
            "source_used": None,
            "data_period": None,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Try UN COMTRADE first (best for latest data)
        try:
            current_year = datetime.now().year
            comtrade_data = self.comtrade.get_bilateral_trade(
                reporter_code=reporter,
                partner_code=partner,
                period=str(current_year),
                hs_code=hs_code
            )
            
            results["sources_checked"].append({
                "source": "UN_COMTRADE",
                "status": "success" if comtrade_data else "no_data",
                "period": comtrade_data.get("latest_period") if comtrade_data else None
            })
            
            if comtrade_data and comtrade_data.get("data"):
                results["data"] = comtrade_data["data"]
                results["source_used"] = "UN_COMTRADE"
                results["data_period"] = comtrade_data.get("latest_period")
                return results
                
        except Exception as e:
            logger.error(f"COMTRADE error: {str(e)}")
            results["sources_checked"].append({
                "source": "UN_COMTRADE",
                "status": "error",
                "error": str(e)
            })
        
        # Fallback to OEC if available
        if self.oec:
            try:
                # OEC uses different method signature, adapt as needed
                oec_data = None  # Placeholder - would need proper implementation
                results["sources_checked"].append({
                    "source": "OEC",
                    "status": "success" if oec_data else "no_data"
                })
                
                if oec_data:
                    results["data"] = oec_data
                    results["source_used"] = "OEC"
                    return results
                    
            except Exception as e:
                logger.error(f"OEC error: {str(e)}")
                results["sources_checked"].append({
                    "source": "OEC",
                    "status": "error",
                    "error": str(e)
                })
        
        # Fallback to WTO (mainly for tariff data)
        try:
            wto_data = self.wto.get_tariff_data(reporter, partner, hs_code)
            results["sources_checked"].append({
                "source": "WTO",
                "status": "success" if wto_data else "no_data",
                "period": wto_data.get("latest_period") if wto_data else None
            })
            
            if wto_data:
                results["data"] = wto_data["data"]
                results["source_used"] = "WTO"
                results["data_period"] = wto_data.get("latest_period")
                return results
                
        except Exception as e:
            logger.error(f"WTO error: {str(e)}")
            results["sources_checked"].append({
                "source": "WTO",
                "status": "error",
                "error": str(e)
            })
        
        return results
    
    def compare_data_sources(
        self,
        country_codes: List[str]
    ) -> Dict:
        """
        Compare all data sources to determine which has the latest data
        
        Returns:
            Comparison report with latest available periods
        """
        comparison = {
            "timestamp": datetime.utcnow().isoformat(),
            "countries_checked": country_codes,
            "sources": {}
        }
        
        for country in country_codes[:5]:  # Check first 5 to avoid rate limits
            # Check COMTRADE
            try:
                comtrade_period = self.comtrade.get_latest_available_period(country)
                if "UN_COMTRADE" not in comparison["sources"]:
                    comparison["sources"]["UN_COMTRADE"] = []
                comparison["sources"]["UN_COMTRADE"].append({
                    "country": country,
                    "latest_period": comtrade_period
                })
            except Exception as e:
                logger.error(f"Error checking COMTRADE for {country}: {str(e)}")
            
            # Check WTO
            try:
                wto_period = self.wto.get_latest_available_year(country)
                if "WTO" not in comparison["sources"]:
                    comparison["sources"]["WTO"] = []
                comparison["sources"]["WTO"].append({
                    "country": country,
                    "latest_period": wto_period
                })
            except Exception as e:
                logger.error(f"Error checking WTO for {country}: {str(e)}")
        
        # Determine overall winner
        avg_periods = {}
        for source, data in comparison["sources"].items():
            periods = [int(d["latest_period"]) for d in data if d["latest_period"]]
            if periods:
                avg_periods[source] = sum(periods) / len(periods)
        
        if avg_periods:
            comparison["recommended_source"] = max(avg_periods, key=avg_periods.get)
            comparison["average_latest_year"] = avg_periods
        
        return comparison


# Global selector instance
data_source_selector = DataSourceSelector()
