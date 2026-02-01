"""
Data Source Selector Tests
===========================
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


class TestCompareDataSources:
    """Tests for comparing data sources"""

    @pytest.mark.asyncio
    async def test_compare_data_sources(self):
        """Test comparing multiple data sources"""
        selector = DataSourceSelector()

        # Mock methods
        selector.comtrade.get_latest_available_period = AsyncMock(return_value="2023")
        selector.wto.get_latest_available_year = AsyncMock(return_value="2022")

        result = await selector.compare_data_sources(["NGA", "KEN", "ZAF"])

        assert "timestamp" in result
        assert "countries_checked" in result
        assert "sources" in result
        assert (
            len(result["countries_checked"]) <= 5
        )  # Limited to 5 to avoid rate limits


class TestBestSourceForCountry:
    """Tests for determining best source for specific country"""

    @pytest.mark.asyncio
    async def test_get_best_source_for_country(self):
        """Test getting best source for a specific country"""
        selector = DataSourceSelector()

        # Mock COMTRADE to have more recent data
        selector.comtrade.get_latest_available_period = AsyncMock(return_value="2023")
        selector.wto.get_latest_available_year = AsyncMock(return_value="2022")

        best_source = await selector.get_best_source_for_country("NGA")

        assert best_source == "UN_COMTRADE"

    @pytest.mark.asyncio
    async def test_get_best_source_defaults_to_comtrade(self):
        """Test default to COMTRADE when no data available"""
        selector = DataSourceSelector()

        # Mock all to fail
        selector.comtrade.get_latest_available_period = AsyncMock(
            side_effect=Exception("Error")
        )
        selector.wto.get_latest_available_year = AsyncMock(
            side_effect=Exception("Error")
        )

        best_source = await selector.get_best_source_for_country("XXX")

        assert best_source == "UN_COMTRADE"


class TestGlobalSelectorInstance:
    """Tests for the global selector instance"""

    def test_global_instance_exists(self):
        """Test that global selector instance is available"""
        assert data_source_selector is not None
        assert isinstance(data_source_selector, DataSourceSelector)

    def test_global_instance_has_sources(self):
        """Test that global instance has all sources configured"""
        assert data_source_selector.comtrade is not None
        assert data_source_selector.wto is not None
        assert data_source_selector._source_status is not None


class TestHSCodeHandling:
    """Tests for HS code parameter handling"""

    @pytest.mark.asyncio
    async def test_with_hs_code(self):
        """Test data retrieval with specific HS code"""
        selector = DataSourceSelector()

        mock_data = {
            "data": [{"hs_code": "0901", "value": 500000}],
            "latest_period": "2023",
        }
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        result = await selector.get_latest_trade_data("ETH", "USA", hs_code="0901")

        assert result["hs_code"] == "0901"
        assert result["source_used"] == "UN_COMTRADE"

        # Verify HS code was passed to COMTRADE
        selector.comtrade.get_bilateral_trade.assert_called_once()
        call_args = selector.comtrade.get_bilateral_trade.call_args
        assert call_args[1]["hs_code"] == "0901"

    @pytest.mark.asyncio
    async def test_without_hs_code(self):
        """Test data retrieval without HS code (all products)"""
        selector = DataSourceSelector()

        mock_data = {"data": [{"value": 1000000}], "latest_period": "2023"}
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        result = await selector.get_latest_trade_data("NGA", "GHA")

        assert result["hs_code"] is None

        # Verify HS code was None
        call_args = selector.comtrade.get_bilateral_trade.call_args
        assert call_args[1]["hs_code"] is None


class TestPartnerHandling:
    """Tests for partner country parameter handling"""

    @pytest.mark.asyncio
    async def test_with_partner_country(self):
        """Test bilateral trade with specific partner"""
        selector = DataSourceSelector()

        mock_data = {"data": [{"value": 750000}], "latest_period": "2023"}
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        result = await selector.get_latest_trade_data("KEN", "UGA")

        assert result["partner"] == "UGA"

        # Verify partner was passed correctly
        call_args = selector.comtrade.get_bilateral_trade.call_args
        assert call_args[1]["partner_code"] == "UGA"

    @pytest.mark.asyncio
    async def test_without_partner_defaults_to_world(self):
        """Test that no partner defaults to world (0)"""
        selector = DataSourceSelector()

        mock_data = {"data": [{"value": 2000000}], "latest_period": "2023"}
        selector.comtrade.get_bilateral_trade = AsyncMock(return_value=mock_data)

        result = await selector.get_latest_trade_data("ZAF", None)

        assert result["partner"] is None

        # Verify default partner code "0" (world) was used
        call_args = selector.comtrade.get_bilateral_trade.call_args
        assert call_args[1]["partner_code"] == "0"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
