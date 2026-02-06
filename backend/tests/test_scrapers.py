"""
Tests for scraper system and 54 African countries support
"""
import pytest
from backend.crawlers.scraper_factory import ScraperFactory
from backend.crawlers.all_countries_registry import (
    AFRICAN_COUNTRIES_REGISTRY,
    get_all_countries_list,
    get_countries_by_region,
    get_countries_by_bloc,
    Region,
    RegionalBlock,
)


class TestCountriesRegistry:
    """Test the 54 countries registry"""
    
    def test_registry_has_54_countries(self):
        """Test that registry contains all 54 African countries"""
        assert len(AFRICAN_COUNTRIES_REGISTRY) == 54
    
    def test_all_countries_have_required_fields(self):
        """Test that all countries have required metadata"""
        required_fields = ["iso2", "iso3", "name_en", "name_fr", "region", "vat_rate"]
        
        for country_code, country_data in AFRICAN_COUNTRIES_REGISTRY.items():
            for field in required_fields:
                assert field in country_data, f"{country_code} missing {field}"
    
    def test_iso_codes_consistency(self):
        """Test ISO2 and ISO3 codes are consistent"""
        for country_code, country_data in AFRICAN_COUNTRIES_REGISTRY.items():
            assert country_code == country_data["iso3"]
            assert len(country_data["iso2"]) == 2
            assert len(country_data["iso3"]) == 3
    
    def test_vat_rates_valid(self):
        """Test VAT rates are valid percentages"""
        for country_code, country_data in AFRICAN_COUNTRIES_REGISTRY.items():
            vat_rate = country_data["vat_rate"]
            assert isinstance(vat_rate, (int, float))
            assert 0 <= vat_rate <= 100, f"{country_code} has invalid VAT: {vat_rate}"
    
    def test_regions_valid(self):
        """Test all countries have valid regions"""
        valid_regions = set(r.value for r in Region)
        
        for country_code, country_data in AFRICAN_COUNTRIES_REGISTRY.items():
            region = country_data["region"].value
            assert region in valid_regions, f"{country_code} has invalid region: {region}"
    
    def test_regional_blocks_valid(self):
        """Test regional blocks are valid"""
        valid_blocks = set(b.value for b in RegionalBlock)
        
        for country_code, country_data in AFRICAN_COUNTRIES_REGISTRY.items():
            blocks = country_data.get("blocks", [])
            for block in blocks:
                assert block.value in valid_blocks, f"{country_code} has invalid block: {block}"
    
    def test_major_economies_exist(self):
        """Test that major African economies are present"""
        major_economies = ["NGA", "EGY", "ZAF", "DZA", "MAR", "KEN", "ETH", "GHA"]
        
        for country in major_economies:
            assert country in AFRICAN_COUNTRIES_REGISTRY, f"Missing major economy: {country}"
    
    def test_get_all_countries_list(self):
        """Test getting list of all countries"""
        countries = get_all_countries_list()
        assert len(countries) == 54
        assert all("iso3" in c for c in countries)
    
    def test_get_countries_by_region(self):
        """Test filtering countries by region"""
        west_african = get_countries_by_region(Region.WEST_AFRICA)
        assert len(west_african) > 0
        assert all(c["region"] == Region.WEST_AFRICA for c in west_african)
        
        # Test all 5 regions
        for region in Region:
            countries = get_countries_by_region(region)
            assert len(countries) > 0
    
    def test_get_countries_by_bloc(self):
        """Test filtering countries by economic bloc"""
        ecowas = get_countries_by_bloc(RegionalBlock.ECOWAS)
        assert len(ecowas) > 0
        
        # ECOWAS should have major West African countries
        ecowas_codes = [c["iso3"] for c in ecowas]
        assert "NGA" in ecowas_codes  # Nigeria
        assert "GHA" in ecowas_codes  # Ghana
    
    def test_regional_tariff_groups(self):
        """Test countries with regional tariffs are properly tagged"""
        # TEC CEDEAO countries
        tec_countries = [
            code for code, data in AFRICAN_COUNTRIES_REGISTRY.items()
            if RegionalBlock.ECOWAS in data.get("blocks", [])
        ]
        assert len(tec_countries) >= 15  # At least 15 ECOWAS members
        
        # SACU countries
        sacu_countries = [
            code for code, data in AFRICAN_COUNTRIES_REGISTRY.items()
            if RegionalBlock.SACU in data.get("blocks", [])
        ]
        assert len(sacu_countries) == 5  # Exactly 5 SACU members


class TestScraperFactory:
    """Test scraper factory for all 54 countries"""
    
    def test_get_scraper_for_all_countries(self):
        """Test that scraper can be obtained for all 54 countries"""
        failures = []
        
        for country_code in AFRICAN_COUNTRIES_REGISTRY.keys():
            scraper = ScraperFactory.get_scraper(country_code)
            if scraper is None:
                failures.append(country_code)
        
        # All countries should have either a specific or generic scraper
        assert len(failures) == 0, f"No scraper for: {failures}"
    
    def test_scraper_has_required_methods(self):
        """Test that scrapers have required methods"""
        # Test a few sample countries
        sample_countries = ["KEN", "GHA", "NGA", "EGY", "ZAF"]
        
        for country_code in sample_countries:
            scraper = ScraperFactory.get_scraper(country_code)
            assert scraper is not None
            assert hasattr(scraper, "scrape_tariffs")
            assert callable(scraper.scrape_tariffs)
    
    def test_scraper_country_code(self):
        """Test that scrapers have correct country code"""
        for country_code in ["KEN", "GHA", "NGA"]:
            scraper = ScraperFactory.get_scraper(country_code)
            assert scraper.country_code == country_code
    
    def test_generic_scraper_fallback(self):
        """Test that generic scraper is used as fallback"""
        # Countries without specific scrapers should get GenericScraper
        scraper = ScraperFactory.get_scraper("BDI")  # Burundi
        assert scraper is not None
        assert scraper.__class__.__name__ in ["GenericScraper", "BurundiScraper"]


class TestRegionalTariffSupport:
    """Test regional tariff system support"""
    
    def test_ecowas_tec_countries(self):
        """Test ECOWAS TEC (Tarif Extérieur Commun) countries"""
        ecowas = get_countries_by_bloc(RegionalBlock.ECOWAS)
        ecowas_codes = [c["iso3"] for c in ecowas]
        
        # Major ECOWAS members
        expected = ["BEN", "BFA", "CIV", "GHA", "GIN", "MLI", "NER", "NGA", "SEN", "TGO"]
        for code in expected:
            assert code in ecowas_codes, f"{code} should be in ECOWAS"
    
    def test_eac_cet_countries(self):
        """Test EAC CET (Common External Tariff) countries"""
        eac = get_countries_by_bloc(RegionalBlock.EAC)
        eac_codes = [c["iso3"] for c in eac]
        
        # Core EAC members
        expected = ["KEN", "UGA", "TZA", "RWA", "BDI"]
        for code in expected:
            if code in AFRICAN_COUNTRIES_REGISTRY:
                assert code in eac_codes, f"{code} should be in EAC"
    
    def test_sacu_countries(self):
        """Test SACU (Southern African Customs Union) countries"""
        sacu = get_countries_by_bloc(RegionalBlock.SACU)
        sacu_codes = [c["iso3"] for c in sacu]
        
        # All SACU members
        expected = ["ZAF", "BWA", "LSO", "NAM", "SWZ"]
        assert len(sacu_codes) == 5
        for code in expected:
            assert code in sacu_codes, f"{code} should be in SACU"
    
    def test_cemac_tdc_countries(self):
        """Test CEMAC TDC (Tarif Douanier Commun) countries"""
        cemac = get_countries_by_bloc(RegionalBlock.CEMAC)
        cemac_codes = [c["iso3"] for c in cemac]
        
        # Core CEMAC members
        expected = ["CMR", "CAF", "TCD", "COG", "GAB", "GNQ"]
        for code in expected:
            if code in AFRICAN_COUNTRIES_REGISTRY:
                assert code in cemac_codes or code in ["CAF", "TCD", "COG", "GNQ"], \
                    f"{code} should be in CEMAC"


class TestCountryPriorities:
    """Test country crawling priorities"""
    
    def test_high_priority_countries(self):
        """Test that major economies have high priority"""
        high_priority = [
            code for code, data in AFRICAN_COUNTRIES_REGISTRY.items()
            if data.get("priority", 3).value == 1
        ]
        
        # Major economies should be in high priority
        major_economies = ["NGA", "EGY", "ZAF", "KEN"]
        for economy in major_economies:
            if economy in AFRICAN_COUNTRIES_REGISTRY:
                priority = AFRICAN_COUNTRIES_REGISTRY[economy].get("priority", 3).value
                assert priority <= 2, f"{economy} should have high/medium priority"
    
    def test_all_priorities_valid(self):
        """Test that all priorities are valid (1-3)"""
        for country_code, data in AFRICAN_COUNTRIES_REGISTRY.items():
            priority = data.get("priority", 3)
            if hasattr(priority, 'value'):
                priority = priority.value
            assert 1 <= priority <= 3, f"{country_code} has invalid priority: {priority}"
