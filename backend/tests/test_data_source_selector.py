"""
Test suite for Data Source Selector Service
Tests the smart data source selector that orchestrates multiple data sources
with fallback logic and error handling.

Test Coverage:
- Source selection priority (UN COMTRADE > OEC > WTO)
- Fallback behavior when primary sources fail
- Error handling across different sources
- Source status tracking and availability
- Data quality metrics and freshness
- Edge cases and invalid inputs
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from backend.services.data_source_selector import DataSourceSelector, data_source_selector

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)
Data Source Selector Tests
Tests for the data_source_selector service that orchestrates multiple data sources
with fallback logic. Tests cover source selection, fallback behavior, error handling,
and status tracking across COMTRADE, OEC, and WTO sources.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime

# Import the service and its dependencies
import sys
import os

# Add backend to path to enable proper imports
backend_path = os.path.join(os.path.dirname(__file__), "..")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from services.data_source_selector import DataSourceSelector, data_source_selector


class TestDataSourceSelectorInit:
    """Tests for DataSourceSelector initialization"""
    
    def test_selector_initializes_with_services(self):
        """Selector should initialize with COMTRADE, OEC, and WTO services"""
        selector = DataSourceSelector()
        
        assert selector.comtrade is not None
        assert selector.wto is not None
        # OEC may be None if not available
        assert selector._source_status is not None
        
    def test_selector_initializes_source_status(self):
        """Selector should initialize source status for all sources"""
        selector = DataSourceSelector()
        
        assert "UN_COMTRADE" in selector._source_status
        assert "OEC" in selector._source_status
        assert "WTO" in selector._source_status
        
        # UN_COMTRADE and WTO should be available by default
        assert selector._source_status["UN_COMTRADE"]["available"] == True
        assert selector._source_status["WTO"]["available"] == True
        
    def test_global_selector_instance_exists(self):
        """Global data_source_selector instance should be available"""
        assert data_source_selector is not None
        assert isinstance(data_source_selector, DataSourceSelector)


class TestGetLatestTradeData:
    """Tests for get_latest_trade_data method"""
    
    @pytest.mark.asyncio
    async def test_returns_comtrade_data_when_available(self):
        """Should return COMTRADE data when available (highest priority)"""
        selector = DataSourceSelector()
        
        # Mock COMTRADE to return data
        mock_comtrade_data = {
            "data": [{"value": 1000000, "year": 2023}],
            "latest_period": "2023"
        }
        
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = mock_comtrade_data
            
            result = await selector.get_latest_trade_data(
                reporter="USA",
                partner="CAN",
                hs_code="0901"
            )
            
            assert result["source_used"] == "UN_COMTRADE"
            assert result["data"] is not None
            assert result["data_period"] == "2023"
            assert len(result["sources_checked"]) >= 1
            
    @pytest.mark.asyncio
    async def test_falls_back_to_oec_when_comtrade_fails(self):
        """Should fall back to OEC when COMTRADE fails"""
        selector = DataSourceSelector()
        
        # Mock COMTRADE to fail
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.side_effect = Exception("COMTRADE API error")
            
            # Mock OEC to return data
            mock_oec_data = {
                "type": "exports",
                "data": [{"value": 500000}],
                "source": "OEC"
            }
            
            with patch.object(selector, '_get_oec_data', new_callable=AsyncMock) as mock_oec:
                mock_oec.return_value = mock_oec_data
                
                result = await selector.get_latest_trade_data(
                    reporter="USA",
                    partner="CAN"
                )
                
                # Should fall back to OEC
                assert result["source_used"] == "OEC"
                assert result["data"] is not None
                assert len(result["sources_checked"]) >= 2
                
    @pytest.mark.asyncio
    async def test_falls_back_to_wto_when_comtrade_and_oec_fail(self):
        """Should fall back to WTO when both COMTRADE and OEC fail"""
        selector = DataSourceSelector()
        
        # Mock COMTRADE to fail
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.side_effect = Exception("COMTRADE API error")
            
            # Mock OEC to fail
            with patch.object(selector, '_get_oec_data', new_callable=AsyncMock) as mock_oec:
                mock_oec.side_effect = Exception("OEC API error")
                
                # Mock WTO to return data
                mock_wto_data = {
                    "data": [{"tariff": 5.0}],
                    "latest_period": "2022"
                }
                
                with patch.object(selector.wto, 'get_tariff_data', new_callable=AsyncMock) as mock_wto:
                    mock_wto.return_value = mock_wto_data
                    
                    result = await selector.get_latest_trade_data(
                        reporter="USA",
                        partner="CAN"
                    )
                    
                    # Should fall back to WTO
                    assert result["source_used"] == "WTO"
                    assert result["data"] is not None
                    assert result["data_period"] == "2022"
                    assert len(result["sources_checked"]) == 3
                    
    @pytest.mark.asyncio
    async def test_returns_no_data_when_all_sources_fail(self):
        """Should return empty result when all sources fail"""
        selector = DataSourceSelector()
        
        # Mock all sources to fail
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.side_effect = Exception("COMTRADE error")
            
            with patch.object(selector, '_get_oec_data', new_callable=AsyncMock) as mock_oec:
                mock_oec.side_effect = Exception("OEC error")
                
                with patch.object(selector.wto, 'get_tariff_data', new_callable=AsyncMock) as mock_wto:
                    mock_wto.side_effect = Exception("WTO error")
                    
                    result = await selector.get_latest_trade_data(
                        reporter="USA",
                        partner="CAN"
                    )
                    
                    assert result["source_used"] is None
                    assert result["data"] is None
                    assert len(result["sources_checked"]) == 3
                    # All should show error status
                    for source in result["sources_checked"]:
                        assert source["status"] == "error"


class TestSourceStatusTracking:
    """Tests for source status tracking and availability"""
    
    def test_update_source_status_on_success(self):
        """Should update source status on successful call"""
        selector = DataSourceSelector()
        initial_error_count = selector._source_status["UN_COMTRADE"]["error_count"]
        
        selector._update_source_status("UN_COMTRADE", success=True)
        
        assert selector._source_status["UN_COMTRADE"]["error_count"] == 0
        assert selector._source_status["UN_COMTRADE"]["last_check"] is not None
        
    def test_update_source_status_on_failure(self):
        """Should increment error count on failed call"""
        selector = DataSourceSelector()
        initial_error_count = selector._source_status["UN_COMTRADE"]["error_count"]
        
        selector._update_source_status("UN_COMTRADE", success=False)
        
        assert selector._source_status["UN_COMTRADE"]["error_count"] == initial_error_count + 1
        assert selector._source_status["UN_COMTRADE"]["last_check"] is not None
        
    def test_disables_source_after_5_consecutive_failures(self):
        """Should disable source after 5 consecutive failures"""
        selector = DataSourceSelector()
        
        # Simulate 5 consecutive failures
        for _ in range(5):
            selector._update_source_status("UN_COMTRADE", success=False)
        
        assert selector._source_status["UN_COMTRADE"]["available"] == False
        assert selector._source_status["UN_COMTRADE"]["error_count"] == 5
        
    def test_resets_error_count_on_success(self):
        """Should reset error count on successful call after failures"""
        selector = DataSourceSelector()
        
        # Simulate 3 failures
        for _ in range(3):
            selector._update_source_status("WTO", success=False)
        
        assert selector._source_status["WTO"]["error_count"] == 3
        
        # Successful call should reset
        selector._update_source_status("WTO", success=True)
        
        assert selector._source_status["WTO"]["error_count"] == 0
        assert selector._source_status["WTO"]["available"] == True


class TestGetSourceStatus:
    """Tests for get_source_status method"""
    
    def test_get_source_status_returns_all_sources(self):
        """Should return status for all data sources"""
        selector = DataSourceSelector()
        
        status = selector.get_source_status()
        
        assert "sources" in status
        assert "UN_COMTRADE" in status["sources"]
        assert "OEC" in status["sources"]
        assert "WTO" in status["sources"]
        
    def test_get_source_status_includes_recommended(self):
        """Should include recommended source"""
        selector = DataSourceSelector()
        
        status = selector.get_source_status()
        
        assert "recommended" in status
        assert status["recommended"] in ["UN_COMTRADE", "OEC", "WTO"]
        
    def test_get_source_status_includes_timestamp(self):
        """Should include timestamp"""
        selector = DataSourceSelector()
        
        status = selector.get_source_status()
        
        assert "timestamp" in status
        assert status["timestamp"] is not None


class TestDataQualityMetrics:
    """Tests for data quality and freshness metrics"""
    
    def test_get_freshness_label_recent(self):
        """Should return 'recent' for data from last year"""
        selector = DataSourceSelector()
        current_year = datetime.now().year
        
        label = selector._get_freshness_label(str(current_year - 1))
        
        assert label == "recent"
        
    def test_get_freshness_label_moderate(self):
        """Should return 'moderate' for data from 2 years ago"""
        selector = DataSourceSelector()
        current_year = datetime.now().year
        
        label = selector._get_freshness_label(str(current_year - 2))
        
        assert label == "moderate"
        
    def test_get_freshness_label_outdated(self):
        """Should return 'outdated' for data older than 2 years"""
        selector = DataSourceSelector()
        current_year = datetime.now().year
        
        label = selector._get_freshness_label(str(current_year - 5))
        
        assert label == "outdated"
        
    def test_get_freshness_label_unknown_for_invalid(self):
        """Should return 'unknown' for invalid period"""
        selector = DataSourceSelector()
        
        label = selector._get_freshness_label("invalid")
        
        assert label == "unknown"
        
    def test_get_source_reliability(self):
        """Should return reliability rating for sources"""
        selector = DataSourceSelector()
        

    def test_initialization(self):
        """Test that selector initializes with all sources"""
        selector = DataSourceSelector()

        assert selector.comtrade is not None
        assert selector.wto is not None
        assert selector._source_status is not None
        assert "UN_COMTRADE" in selector._source_status
        assert "OEC" in selector._source_status
        assert "WTO" in selector._source_status

    def test_initial_source_status(self):
        """Test that all sources start as available"""
        selector = DataSourceSelector()

        assert selector._source_status["UN_COMTRADE"]["available"] is True
        assert selector._source_status["WTO"]["available"] is True
        assert selector._source_status["UN_COMTRADE"]["error_count"] == 0
        assert selector._source_status["WTO"]["error_count"] == 0


class TestSourceSelection:
    """Tests for source selection logic"""

    @pytest.mark.asyncio
    async def test_comtrade_selected_first(self):
        """Test that COMTRADE is tried first when available"""
        selector = DataSourceSelector()

        # Mock COMTRADE to return data
        mock_data = {"data": [{"trade_value": 1000000}], "latest_period": "2023"}
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        result = await selector.get_latest_trade_data("NGA", "GHA")

        assert result["source_used"] == "UN_COMTRADE"
        assert result["data"] == mock_data["data"]
        assert result["data_period"] == "2023"
        selector.comtrade.get_bilateral_trade.assert_called_once()

    @pytest.mark.asyncio
    async def test_fallback_to_oec_when_comtrade_fails(self):
        """Test fallback to OEC when COMTRADE fails"""
        selector = DataSourceSelector()

        # Mock COMTRADE to fail
        selector.comtrade.get_bilateral_trade = AsyncMock(
            side_effect=Exception("API Error")
        )

        # Mock OEC to succeed
        if selector.oec:
            mock_oec_data = {
                "type": "exports",
                "data": [{"value": 500000}],
                "source": "OEC",
            }
            selector._get_oec_data = AsyncMock(return_value=mock_oec_data)

            result = await selector.get_latest_trade_data("KEN", "TZA")

            assert result["source_used"] == "OEC"
            assert len(result["sources_checked"]) >= 2
            assert result["sources_checked"][0]["source"] == "UN_COMTRADE"
            assert result["sources_checked"][0]["status"] == "error"

    @pytest.mark.asyncio
    async def test_fallback_to_wto_when_comtrade_and_oec_fail(self):
        """Test fallback to WTO when both COMTRADE and OEC fail"""
        selector = DataSourceSelector()

        # Mock COMTRADE to fail
        selector.comtrade.get_bilateral_trade = AsyncMock(
            side_effect=Exception("API Error")
        )

        # Mock OEC to fail (if available)
        if selector.oec:
            selector._get_oec_data = AsyncMock(return_value=None)

        # Mock WTO to succeed
        mock_wto_data = {"data": [{"tariff_rate": 5.5}], "latest_period": "2022"}
        selector.wto.get_tariff_data = AsyncMock(return_value=mock_wto_data)

        result = await selector.get_latest_trade_data("ZAF", "EGY")

        assert result["source_used"] == "WTO"
        assert result["data"] == mock_wto_data["data"]
        assert len(result["sources_checked"]) >= 2

    @pytest.mark.asyncio
    async def test_no_data_from_any_source(self):
        """Test when no source returns data"""
        selector = DataSourceSelector()

        # Mock all sources to fail
        selector.comtrade.get_bilateral_trade = AsyncMock(
            side_effect=Exception("Error")
        )
        if selector.oec:
            selector._get_oec_data = AsyncMock(return_value=None)
        selector.wto.get_tariff_data = AsyncMock(return_value=None)

        result = await selector.get_latest_trade_data("XXX", "YYY")

        assert result["data"] is None
        assert result["source_used"] is None
        assert len(result["sources_checked"]) >= 2


class TestErrorHandling:
    """Tests for error handling across different sources"""

    @pytest.mark.asyncio
    async def test_comtrade_api_error_handling(self):
        """Test handling of COMTRADE API errors"""
        selector = DataSourceSelector()

        # Mock COMTRADE to raise an error
        selector.comtrade.get_bilateral_trade = AsyncMock(
            side_effect=Exception("Rate limit exceeded")
        )
        selector.wto.get_tariff_data = AsyncMock(return_value=None)
        if selector.oec:
            selector._get_oec_data = AsyncMock(return_value=None)

        result = await selector.get_latest_trade_data("NGA", "GHA")

        # Check that error was recorded
        assert any(
            check["source"] == "UN_COMTRADE" and check["status"] == "error"
            for check in result["sources_checked"]
        )

        # Verify error count increased
        assert selector._source_status["UN_COMTRADE"]["error_count"] > 0

    @pytest.mark.asyncio
    async def test_wto_api_error_handling(self):
        """Test handling of WTO API errors"""
        selector = DataSourceSelector()

        # Mock COMTRADE to return no data
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=None)

        # Mock WTO to raise an error
        selector.wto.get_tariff_data = AsyncMock(
            side_effect=Exception("Service unavailable")
        )

        if selector.oec:
            selector._get_oec_data = AsyncMock(return_value=None)

        result = await selector.get_latest_trade_data("ZAF", "KEN")

        # Check that error was recorded
        wto_check = next(
            (c for c in result["sources_checked"] if c["source"] == "WTO"), None
        )
        if wto_check:
            assert wto_check["status"] == "error"

    @pytest.mark.asyncio
    async def test_source_disabled_after_multiple_errors(self):
        """Test that source is disabled after 5 consecutive errors"""
        selector = DataSourceSelector()

        # Mock to always fail
        selector.comtrade.get_bilateral_trade = AsyncMock(
            side_effect=Exception("Error")
        )
        selector.wto.get_tariff_data = AsyncMock(return_value=None)
        if selector.oec:
            selector._get_oec_data = AsyncMock(return_value=None)

        # Call 5 times to trigger disable
        for _ in range(5):
            await selector.get_latest_trade_data("TEST", "TEST")

        # Check that COMTRADE is now disabled
        assert selector._source_status["UN_COMTRADE"]["available"] is False
        assert selector._source_status["UN_COMTRADE"]["error_count"] >= 5

    @pytest.mark.asyncio
    async def test_error_count_resets_on_success(self):
        """Test that error count resets when source succeeds"""
        selector = DataSourceSelector()

        # Set initial error count
        selector._source_status["UN_COMTRADE"]["error_count"] = 3

        # Mock COMTRADE to succeed
        mock_data = {"data": [{"value": 1000}], "latest_period": "2023"}
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        await selector.get_latest_trade_data("NGA", "GHA")

        # Error count should be reset
        assert selector._source_status["UN_COMTRADE"]["error_count"] == 0


class TestSourceStatusTracking:
    """Tests for source status tracking and availability"""

    def test_get_source_status(self):
        """Test getting current source status"""
        selector = DataSourceSelector()

        status = selector.get_source_status()

        assert "sources" in status
        assert "recommended" in status
        assert "timestamp" in status
        assert "UN_COMTRADE" in status["sources"]
        assert "WTO" in status["sources"]

    def test_update_source_status_on_success(self):
        """Test status update on successful call"""
        selector = DataSourceSelector()

        initial_count = selector._source_status["UN_COMTRADE"]["error_count"]

        selector._update_source_status("UN_COMTRADE", success=True)

        assert selector._source_status["UN_COMTRADE"]["error_count"] == 0
        assert selector._source_status["UN_COMTRADE"]["last_check"] is not None

    def test_update_source_status_on_failure(self):
        """Test status update on failed call"""
        selector = DataSourceSelector()

        initial_count = selector._source_status["WTO"]["error_count"]

        selector._update_source_status("WTO", success=False)

        assert selector._source_status["WTO"]["error_count"] == initial_count + 1
        assert selector._source_status["WTO"]["last_check"] is not None

    def test_recommended_source_selection(self):
        """Test recommended source selection logic"""
        selector = DataSourceSelector()

        # Initially, COMTRADE should be recommended
        recommended = selector._get_recommended_source()
        assert recommended in ["UN_COMTRADE", "OEC", "WTO"]

        # Disable COMTRADE
        selector._source_status["UN_COMTRADE"]["available"] = False

        # Now should recommend next available
        recommended = selector._get_recommended_source()
        assert recommended in ["OEC", "WTO"]


class TestDataQualityAssessment:
    """Tests for data quality and freshness assessment"""

    @pytest.mark.asyncio
    async def test_get_trade_with_source_info(self):
        """Test getting trade data with detailed source information"""
        selector = DataSourceSelector()

        # Mock COMTRADE to return data
        mock_data = {"data": [{"value": 1000000}], "latest_period": "2023"}
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        result = await selector.get_trade_with_source_info("NGA", "GHA")

        assert "data_quality" in result
        assert result["data_quality"]["source"] == "UN_COMTRADE"
        assert "freshness" in result["data_quality"]
        assert "reliability" in result["data_quality"]
        assert "coverage" in result["data_quality"]

    def test_freshness_label_recent(self):
        """Test freshness label for recent data"""
        selector = DataSourceSelector()

        current_year = datetime.now().year
        label = selector._get_freshness_label(str(current_year - 1))

        assert label == "recent"

    def test_freshness_label_moderate(self):
        """Test freshness label for moderately old data"""
        selector = DataSourceSelector()

        current_year = datetime.now().year
        label = selector._get_freshness_label(str(current_year - 2))

        assert label == "moderate"

    def test_freshness_label_outdated(self):
        """Test freshness label for outdated data"""
        selector = DataSourceSelector()

        current_year = datetime.now().year
        label = selector._get_freshness_label(str(current_year - 5))

        assert label == "outdated"

    def test_source_reliability_ratings(self):
        """Test reliability ratings for different sources"""
        selector = DataSourceSelector()

        assert selector._get_source_reliability("UN_COMTRADE") == "high"
        assert selector._get_source_reliability("OEC") == "high"
        assert selector._get_source_reliability("WTO") == "high"
        assert selector._get_source_reliability("UNKNOWN") == "unknown"


class TestGetTradeWithSourceInfo:
    """Tests for get_trade_with_source_info method"""
    
    @pytest.mark.asyncio
    async def test_includes_data_quality_information(self):
        """Should include data quality information in response"""
        selector = DataSourceSelector()
        
        # Mock COMTRADE to return data
        mock_data = {
            "data": [{"value": 1000000}],
            "latest_period": "2023"
        }
        
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = mock_data
            
            result = await selector.get_trade_with_source_info(
                reporter="USA",
                partner="CAN"
            )
            
            assert "data_quality" in result
            assert "source" in result["data_quality"]
            assert "freshness" in result["data_quality"]
            assert "reliability" in result["data_quality"]
            assert "coverage" in result["data_quality"]


class TestGetBestSourceForCountry:
    """Tests for get_best_source_for_country method"""
    
    @pytest.mark.asyncio
    async def test_returns_source_with_most_recent_data(self):
        """Should return source with most recent data"""
        selector = DataSourceSelector()
        
        # Mock COMTRADE to have 2023 data
        with patch.object(selector.comtrade, 'get_latest_available_period', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = "2023"
            
            # Mock WTO to have 2022 data
            with patch.object(selector.wto, 'get_latest_available_year', new_callable=AsyncMock) as mock_wto:
                mock_wto.return_value = "2022"
                
                best_source = await selector.get_best_source_for_country("USA")
                
                # Should prefer COMTRADE with more recent data
                assert best_source == "UN_COMTRADE"
                
    @pytest.mark.asyncio
    async def test_returns_default_when_no_sources_available(self):
        """Should return default source when no data available"""
        selector = DataSourceSelector()
        
        # Mock all sources to fail
        with patch.object(selector.comtrade, 'get_latest_available_period', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.side_effect = Exception("Error")
            
            with patch.object(selector.wto, 'get_latest_available_year', new_callable=AsyncMock) as mock_wto:
                mock_wto.side_effect = Exception("Error")
                
                best_source = await selector.get_best_source_for_country("USA")
                
                # Should return default
                assert best_source == "UN_COMTRADE"


class TestCompareDataSources:
    """Tests for compare_data_sources method"""
    
    @pytest.mark.asyncio
    async def test_compares_multiple_sources(self):
        """Should compare data from multiple sources"""
        selector = DataSourceSelector()
        
        countries = ["USA", "CAN", "MEX"]
        
        # Mock COMTRADE
        with patch.object(selector.comtrade, 'get_latest_available_period', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = "2023"
            
            # Mock WTO
            with patch.object(selector.wto, 'get_latest_available_year', new_callable=AsyncMock) as mock_wto:
                mock_wto.return_value = "2022"
                
                comparison = await selector.compare_data_sources(countries)
                
                assert "timestamp" in comparison
                assert "countries_checked" in comparison
                assert "sources" in comparison
                assert len(comparison["countries_checked"]) <= 5  # Limits to 5 countries
                
    @pytest.mark.asyncio
    async def test_comparison_includes_recommended_source(self):
        """Should include recommended source in comparison"""
        selector = DataSourceSelector()
        
        countries = ["USA", "CAN"]
        
        # Mock sources
        with patch.object(selector.comtrade, 'get_latest_available_period', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = "2023"
            
            with patch.object(selector.wto, 'get_latest_available_year', new_callable=AsyncMock) as mock_wto:
                mock_wto.return_value = "2022"
                
                comparison = await selector.compare_data_sources(countries)
                
                if "recommended_source" in comparison:
                    assert comparison["recommended_source"] in ["UN_COMTRADE", "WTO"]


class TestEdgeCases:
    """Tests for edge cases and error handling"""
    
    @pytest.mark.asyncio
    async def test_handles_none_partner(self):
        """Should handle None partner gracefully"""
        selector = DataSourceSelector()
        
        mock_data = {
            "data": [{"value": 1000000}],
            "latest_period": "2023"
        }
        
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = mock_data
            
            result = await selector.get_latest_trade_data(
                reporter="USA",
                partner=None
            )
            
            assert result["partner"] is None
            # Should have called comtrade with partner="0" (World)
            mock_comtrade.assert_called_once()
            
    @pytest.mark.asyncio
    async def test_handles_none_hs_code(self):
        """Should handle None HS code gracefully"""
        selector = DataSourceSelector()
        
        mock_data = {
            "data": [{"value": 1000000}],
            "latest_period": "2023"
        }
        
        with patch.object(selector.comtrade, 'get_bilateral_trade', new_callable=AsyncMock) as mock_comtrade:
            mock_comtrade.return_value = mock_data
            
            result = await selector.get_latest_trade_data(
                reporter="USA",
                hs_code=None
            )
            
            assert result["hs_code"] is None
            
    @pytest.mark.asyncio
    async def test_skips_disabled_sources(self):
        """Should skip sources that are marked as unavailable"""
        selector = DataSourceSelector()
        
        # Disable COMTRADE
        selector._source_status["UN_COMTRADE"]["available"] = False
        
        # Mock OEC to return data
        mock_oec_data = {
            "type": "exports",
            "data": [{"value": 500000}],
            "source": "OEC"
        }
        
        with patch.object(selector, '_get_oec_data', new_callable=AsyncMock) as mock_oec:
            mock_oec.return_value = mock_oec_data
            
            result = await selector.get_latest_trade_data(
                reporter="USA",
                partner="CAN"
            )
            
            # Should skip COMTRADE and use OEC
            assert result["source_used"] == "OEC"
            # COMTRADE should not be in sources_checked
            source_names = [s["source"] for s in result["sources_checked"]]
            assert "UN_COMTRADE" not in source_names


class TestGetRecommendedSource:
    """Tests for _get_recommended_source method"""
    
    def test_recommends_first_available_source(self):
        """Should recommend first available source in priority order"""
        selector = DataSourceSelector()
        
        # All sources available - should recommend UN_COMTRADE
        recommended = selector._get_recommended_source()
        assert recommended == "UN_COMTRADE"
        
    def test_recommends_next_when_first_unavailable(self):
        """Should recommend next source when first is unavailable"""
        selector = DataSourceSelector()
        
        # Disable UN_COMTRADE
        selector._source_status["UN_COMTRADE"]["available"] = False
        
        recommended = selector._get_recommended_source()
        # Should recommend OEC or WTO (next available)
        assert recommended in ["OEC", "WTO"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
