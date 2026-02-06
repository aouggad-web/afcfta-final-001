"""
Tests for background job tasks
"""
import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from backend.jobs.tasks import (
    crawl_country_customs_data,
    validate_country_data,
    schedule_daily_crawls,
    get_job_status,
    get_all_jobs,
    clear_old_jobs,
)


pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_scraper():
    """Mock scraper fixture"""
    scraper = MagicMock()
    scraper.scrape_tariffs = AsyncMock(return_value={
        "tariffs": {
            "tariff_lines": [
                {"hs_code": "0101.21", "description": "Test", "customs_duty": "25%"}
            ]
        }
    })
    return scraper


@pytest.fixture
def mock_db():
    """Mock database fixture"""
    db = MagicMock()
    collection = MagicMock()
    collection.insert_one = AsyncMock()
    collection.find_one = AsyncMock(return_value=None)
    db.__getitem__ = MagicMock(return_value=collection)
    return db


class TestCrawlCountryCustomsData:
    """Test crawl_country_customs_data function"""
    
    @patch('backend.jobs.tasks.ScraperFactory.get_scraper')
    @patch('backend.jobs.tasks.get_db')
    @patch('backend.jobs.tasks.notification_manager')
    async def test_crawl_success(self, mock_notif, mock_get_db, mock_factory, mock_scraper, mock_db):
        """Test successful crawl"""
        mock_factory.return_value = mock_scraper
        mock_get_db.return_value = mock_db
        mock_notif.notify_crawl_start = AsyncMock()
        mock_notif.notify_crawl_success = AsyncMock()
        
        result = await crawl_country_customs_data("KEN", notify=True)
        
        assert result["status"] == "success"
        assert result["country_code"] == "KEN"
        assert "job_id" in result
        assert "duration_seconds" in result
        assert result["stats"]["items_scraped"] == 1
        
        # Verify notifications were sent
        mock_notif.notify_crawl_start.assert_called_once()
        mock_notif.notify_crawl_success.assert_called_once()
    
    @patch('backend.jobs.tasks.ScraperFactory.get_scraper')
    @patch('backend.jobs.tasks.notification_manager')
    async def test_crawl_no_scraper(self, mock_notif, mock_factory):
        """Test crawl when scraper not found"""
        mock_factory.return_value = None
        mock_notif.notify_crawl_start = AsyncMock()
        mock_notif.notify_crawl_failed = AsyncMock()
        
        result = await crawl_country_customs_data("XXX", notify=True)
        
        assert result["status"] == "failed"
        assert "No scraper available" in result["errors"][0]
        mock_notif.notify_crawl_failed.assert_called_once()
    
    @patch('backend.jobs.tasks.ScraperFactory.get_scraper')
    @patch('backend.jobs.tasks.get_db')
    @patch('backend.jobs.tasks.notification_manager')
    async def test_crawl_without_notifications(self, mock_notif, mock_get_db, mock_factory, mock_scraper, mock_db):
        """Test crawl with notifications disabled"""
        mock_factory.return_value = mock_scraper
        mock_get_db.return_value = mock_db
        
        result = await crawl_country_customs_data("KEN", notify=False)
        
        assert result["status"] == "success"
        # Verify no notifications were sent
        mock_notif.notify_crawl_start.assert_not_called()
        mock_notif.notify_crawl_success.assert_not_called()
    
    @patch('backend.jobs.tasks.ScraperFactory.get_scraper')
    @patch('backend.jobs.tasks.get_db')
    async def test_crawl_without_db_save(self, mock_get_db, mock_factory, mock_scraper, mock_db):
        """Test crawl without saving to database"""
        mock_factory.return_value = mock_scraper
        mock_get_db.return_value = mock_db
        
        result = await crawl_country_customs_data("KEN", save_to_db=False, notify=False)
        
        assert result["status"] == "success"
        # Verify database insert was not called
        mock_db["customs_data"].insert_one.assert_not_called()
    
    @patch('backend.jobs.tasks.ScraperFactory.get_scraper')
    @patch('backend.jobs.tasks.notification_manager')
    async def test_crawl_validation_low_score(self, mock_notif, mock_factory, mock_scraper):
        """Test crawl with low validation score triggers warning"""
        # Mock scraper to return problematic data
        mock_scraper.scrape_tariffs = AsyncMock(return_value={
            "tariffs": {
                "tariff_lines": []  # Empty data triggers validation issues
            }
        })
        mock_factory.return_value = mock_scraper
        mock_notif.notify_crawl_start = AsyncMock()
        mock_notif.notify_validation_issues = AsyncMock()
        
        with patch('os.environ.get') as mock_env:
            mock_env.side_effect = lambda k, default: {
                "MIN_VALIDATION_SCORE": "70",
                "VALIDATION_ALERT_THRESHOLD": "80",
                "MONGO_URL": "mongodb://localhost:27017/",
                "DB_NAME": "test",
            }.get(k, default)
            
            result = await crawl_country_customs_data("KEN", save_to_db=False, notify=True)
        
        # Should still succeed but with low score
        assert result["status"] == "success"


class TestValidateCountryData:
    """Test validate_country_data function"""
    
    @patch('backend.jobs.tasks.get_db')
    async def test_validate_existing_data(self, mock_get_db, mock_db):
        """Test validation of existing data"""
        mock_db["customs_data"].find_one = AsyncMock(return_value={
            "country_code": "KEN",
            "data": {
                "tariffs": {
                    "tariff_lines": [
                        {"hs_code": "0101.21", "description": "Test"}
                    ]
                }
            },
            "imported_at": "2024-01-01T00:00:00"
        })
        mock_get_db.return_value = mock_db
        
        result = await validate_country_data("KEN")
        
        assert result["status"] == "completed"
        assert result["country_code"] == "KEN"
        assert "validation_score" in result
    
    @patch('backend.jobs.tasks.get_db')
    async def test_validate_no_data(self, mock_get_db, mock_db):
        """Test validation when no data exists"""
        mock_db["customs_data"].find_one = AsyncMock(return_value=None)
        mock_get_db.return_value = mock_db
        
        result = await validate_country_data("XXX")
        
        assert result["status"] == "no_data"
        assert "No data found" in result["message"]


class TestScheduleDailyCrawls:
    """Test schedule_daily_crawls function"""
    
    @patch('backend.jobs.tasks.crawl_country_customs_data')
    async def test_schedule_specific_countries(self, mock_crawl):
        """Test scheduling crawls for specific countries"""
        mock_crawl.return_value = {"status": "success"}
        
        result = await schedule_daily_crawls(countries=["KEN", "GHA"])
        
        assert result["total_countries"] == 2
        assert mock_crawl.call_count == 2
    
    @patch('backend.jobs.tasks.crawl_country_customs_data')
    async def test_schedule_by_priority(self, mock_crawl):
        """Test scheduling crawls by priority"""
        mock_crawl.return_value = {"status": "success"}
        
        result = await schedule_daily_crawls(priority=1)
        
        # High priority countries should be scheduled
        assert result["total_countries"] > 0
        assert mock_crawl.call_count > 0


class TestJobRegistry:
    """Test job registry functions"""
    
    def test_get_job_status(self):
        """Test getting job status"""
        # Jobs are stored in module-level registry during execution
        status = get_job_status("nonexistent_job")
        assert status is None
    
    def test_get_all_jobs(self):
        """Test getting all jobs"""
        jobs = get_all_jobs()
        assert isinstance(jobs, dict)
    
    def test_clear_old_jobs(self):
        """Test clearing old jobs"""
        # This should not raise an error
        clear_old_jobs(max_age_hours=1)
