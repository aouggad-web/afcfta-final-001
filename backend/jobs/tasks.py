"""
Background tasks for AfCFTA customs data crawling system.

This module provides async tasks for:
- Crawling customs data from African countries
- Validating scraped data
- Scheduling periodic crawls
- Managing job lifecycle with notifications
"""

import logging
import asyncio
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import os

from backend.notifications.notification_manager import NotificationManager
from backend.crawlers.scraper_factory import ScraperFactory
from backend.crawlers.all_countries_registry import AFRICAN_COUNTRIES_REGISTRY
from backend.crawlers.validators.data_quality_validator import DataQualityValidator
from backend.crawlers.validators.tariff_validator import TariffValidator
from backend.crawlers.validators.consistency_validator import ConsistencyValidator

logger = logging.getLogger(__name__)

# Initialize notification manager (will be reinitialized with config in each task)
notification_manager = NotificationManager()

# Job status tracking (in-memory - in production, use Redis or database)
_job_registry: Dict[str, Dict[str, Any]] = {}


def get_db():
    """Get MongoDB database connection"""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
    client = AsyncIOMotorClient(mongo_url)
    return client[os.environ.get('DB_NAME', 'afcfta')]


async def crawl_country_customs_data(
    country_code: str,
    job_id: Optional[str] = None,
    save_to_db: bool = True,
    notify: bool = True,
) -> Dict[str, Any]:
    """
    Crawl customs data for a specific country with full notification integration.
    
    Args:
        country_code: ISO3 country code (e.g., 'KEN', 'GHA', 'NGA')
        job_id: Optional job identifier (auto-generated if not provided)
        save_to_db: Whether to save results to database
        notify: Whether to send notifications
        
    Returns:
        Dict containing job results with keys:
            - job_id: Unique job identifier
            - country_code: Country code
            - status: 'success', 'failed', or 'partial'
            - start_time: ISO timestamp
            - end_time: ISO timestamp
            - duration_seconds: Execution time
            - data: Scraped data (if successful)
            - stats: Statistics about scraped data
            - validation: Validation results
            - errors: List of errors (if any)
    """
    # Generate job ID if not provided
    if job_id is None:
        job_id = f"crawl_{country_code}_{uuid.uuid4().hex[:8]}"
    
    start_time = datetime.utcnow()
    country_info = AFRICAN_COUNTRIES_REGISTRY.get(country_code.upper())
    
    # Initialize result structure
    result = {
        "job_id": job_id,
        "country_code": country_code.upper(),
        "status": "started",
        "start_time": start_time.isoformat(),
        "country_name": country_info.get("name_en") if country_info else country_code,
        "errors": [],
    }
    
    # Register job
    _job_registry[job_id] = result
    
    logger.info(f"Starting crawl job {job_id} for {country_code}")
    
    try:
        # Get country name for better notifications
        country_name = result["country_name"]
        
        # Send start notification
        if notify:
            await notification_manager.notify_crawl_start(
                job_id=job_id,
                country_code=country_code.upper(),
                country_name=country_name,
            )
        
        # Get scraper for country
        scraper = ScraperFactory.get_scraper(country_code.upper())
        if not scraper:
            error_msg = f"No scraper available for country {country_code}"
            logger.error(error_msg)
            result["status"] = "failed"
            result["errors"].append(error_msg)
            
            if notify:
                await notification_manager.notify_crawl_failed(
                    job_id=job_id,
                    country_code=country_code.upper(),
                    country_name=country_name,
                    error=error_msg,
                    error_type="scraper_not_found",
                )
            
            return result
        
        # Perform scraping
        logger.info(f"Scraping tariffs for {country_code}...")
        scraped_data = await scraper.scrape_tariffs()
        
        if not scraped_data:
            error_msg = "No data returned from scraper"
            logger.warning(error_msg)
            result["status"] = "failed"
            result["errors"].append(error_msg)
            
            if notify:
                await notification_manager.notify_crawl_failed(
                    job_id=job_id,
                    country_code=country_code.upper(),
                    country_name=country_name,
                    error=error_msg,
                    error_type="no_data",
                )
            
            return result
        
        # Calculate statistics
        tariff_lines = scraped_data.get("tariffs", {}).get("tariff_lines", [])
        stats = {
            "items_scraped": len(tariff_lines),
            "has_tariffs": len(tariff_lines) > 0,
            "scraper_type": scraper.__class__.__name__,
        }
        
        # Perform data validation
        logger.info(f"Validating data for {country_code}...")
        validation_issues = []
        validation_score = 100.0
        
        try:
            # Data quality validation
            quality_validator = DataQualityValidator()
            quality_results = quality_validator.validate(scraped_data)
            if not quality_results["valid"]:
                validation_issues.extend(quality_results["issues"])
                validation_score -= len(quality_results["issues"]) * 5
            
            # Tariff validation
            tariff_validator = TariffValidator()
            tariff_results = tariff_validator.validate(scraped_data)
            if not tariff_results["valid"]:
                validation_issues.extend(tariff_results["issues"])
                validation_score -= len(tariff_results["issues"]) * 3
            
            # Consistency validation
            consistency_validator = ConsistencyValidator()
            consistency_results = consistency_validator.validate(scraped_data)
            if not consistency_results["valid"]:
                validation_issues.extend(consistency_results["issues"])
                validation_score -= len(consistency_results["issues"]) * 2
            
            # Ensure score doesn't go below 0
            validation_score = max(0, validation_score)
            
            stats["validation_score"] = validation_score
            result["validation"] = {
                "score": validation_score,
                "issues": validation_issues,
                "issue_count": len(validation_issues),
            }
            
            logger.info(f"Validation score for {country_code}: {validation_score}/100")
            
        except Exception as e:
            logger.error(f"Validation error for {country_code}: {e}")
            validation_issues.append(f"Validation process error: {str(e)}")
            stats["validation_score"] = 0
        
        # Save to database if requested
        if save_to_db:
            try:
                db = get_db()
                document = {
                    "country_code": country_code.upper(),
                    "country_name": country_name,
                    "imported_at": datetime.utcnow(),
                    "job_id": job_id,
                    "data": scraped_data,
                    "stats": stats,
                    "validation": result.get("validation"),
                }
                await db["customs_data"].insert_one(document)
                logger.info(f"Data saved to database for {country_code}")
            except Exception as e:
                logger.error(f"Database save error for {country_code}: {e}")
                result["errors"].append(f"Database error: {str(e)}")
        
        # Calculate duration
        end_time = datetime.utcnow()
        duration_seconds = (end_time - start_time).total_seconds()
        
        # Update result
        result.update({
            "status": "success",
            "end_time": end_time.isoformat(),
            "duration_seconds": duration_seconds,
            "data": scraped_data,
            "stats": stats,
        })
        
        # Send notifications based on validation results
        if notify:
            # Check validation threshold
            min_score = float(os.environ.get("MIN_VALIDATION_SCORE", 70))
            alert_threshold = float(os.environ.get("VALIDATION_ALERT_THRESHOLD", 80))
            
            if validation_score < min_score:
                # Critical validation failure
                await notification_manager.notify_crawl_failed(
                    job_id=job_id,
                    country_code=country_code.upper(),
                    country_name=country_name,
                    error=f"Validation score {validation_score} below minimum {min_score}",
                    error_type="validation_failure",
                    duration_seconds=duration_seconds,
                )
            elif validation_score < alert_threshold:
                # Validation issues but acceptable
                await notification_manager.notify_validation_issues(
                    job_id=job_id,
                    country_code=country_code.upper(),
                    country_name=country_name,
                    issues=validation_issues[:10],  # Top 10 issues
                    validation_score=validation_score,
                )
                # Also send success since data was collected
                await notification_manager.notify_crawl_success(
                    job_id=job_id,
                    country_code=country_code.upper(),
                    country_name=country_name,
                    stats=stats,
                    duration_seconds=duration_seconds,
                )
            else:
                # Success with good validation
                await notification_manager.notify_crawl_success(
                    job_id=job_id,
                    country_code=country_code.upper(),
                    country_name=country_name,
                    stats=stats,
                    duration_seconds=duration_seconds,
                )
        
        logger.info(f"Crawl job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Crawl job {job_id} failed: {e}", exc_info=True)
        
        end_time = datetime.utcnow()
        duration_seconds = (end_time - start_time).total_seconds()
        
        result.update({
            "status": "failed",
            "end_time": end_time.isoformat(),
            "duration_seconds": duration_seconds,
            "errors": result["errors"] + [str(e)],
        })
        
        if notify:
            await notification_manager.notify_crawl_failed(
                job_id=job_id,
                country_code=country_code.upper(),
                country_name=result.get("country_name", country_code),
                error=str(e),
                error_type=type(e).__name__,
                duration_seconds=duration_seconds,
            )
    
    finally:
        # Update job registry
        _job_registry[job_id] = result
    
    return result


async def validate_country_data(
    country_code: str,
    job_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Validate existing customs data for a country without re-crawling.
    
    Args:
        country_code: ISO3 country code
        job_id: Optional job identifier
        
    Returns:
        Dict containing validation results
    """
    if job_id is None:
        job_id = f"validate_{country_code}_{uuid.uuid4().hex[:8]}"
    
    logger.info(f"Starting validation job {job_id} for {country_code}")
    
    try:
        db = get_db()
        
        # Get latest data from database
        data = await db["customs_data"].find_one(
            {"country_code": country_code.upper()},
            sort=[("imported_at", -1)]
        )
        
        if not data:
            return {
                "job_id": job_id,
                "country_code": country_code.upper(),
                "status": "no_data",
                "message": f"No data found for {country_code}",
            }
        
        # Run validators
        validation_issues = []
        
        validators = [
            DataQualityValidator(),
            TariffValidator(),
            ConsistencyValidator(),
        ]
        
        for validator in validators:
            result = validator.validate(data.get("data", {}))
            if not result["valid"]:
                validation_issues.extend(result["issues"])
        
        validation_score = max(0, 100 - len(validation_issues) * 3)
        
        return {
            "job_id": job_id,
            "country_code": country_code.upper(),
            "status": "completed",
            "validation_score": validation_score,
            "issues": validation_issues,
            "issue_count": len(validation_issues),
            "data_timestamp": data.get("imported_at"),
        }
        
    except Exception as e:
        logger.error(f"Validation job {job_id} failed: {e}")
        return {
            "job_id": job_id,
            "country_code": country_code.upper(),
            "status": "failed",
            "error": str(e),
        }


async def schedule_daily_crawls(
    priority: Optional[int] = None,
    countries: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Schedule crawl jobs for all or selected countries.
    
    Args:
        priority: If specified, only crawl countries with this priority (1-3)
        countries: If specified, only crawl these countries (ISO3 codes)
        
    Returns:
        Dict with scheduling results
    """
    logger.info("Starting scheduled crawl batch")
    
    # Determine which countries to crawl
    if countries:
        target_countries = [c.upper() for c in countries]
    elif priority:
        target_countries = [
            code for code, info in AFRICAN_COUNTRIES_REGISTRY.items()
            if info.get("priority", 3).value == priority
        ]
    else:
        # All countries
        target_countries = list(AFRICAN_COUNTRIES_REGISTRY.keys())
    
    logger.info(f"Scheduling crawls for {len(target_countries)} countries")
    
    # Run crawls with concurrency control
    max_concurrent = int(os.environ.get("MAX_CONCURRENT_CRAWLS", 5))
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def crawl_with_semaphore(country_code: str):
        async with semaphore:
            return await crawl_country_customs_data(country_code)
    
    # Execute all crawls
    tasks = [crawl_with_semaphore(code) for code in target_countries]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Summarize results
    success_count = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "success")
    failed_count = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "failed")
    error_count = sum(1 for r in results if isinstance(r, Exception))
    
    summary = {
        "total_countries": len(target_countries),
        "successful": success_count,
        "failed": failed_count,
        "errors": error_count,
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    logger.info(f"Batch crawl completed: {summary}")
    
    return summary


def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    """
    Get the status of a specific job.
    
    Args:
        job_id: Job identifier
        
    Returns:
        Job status dict or None if not found
    """
    return _job_registry.get(job_id)


def get_all_jobs() -> Dict[str, Dict[str, Any]]:
    """
    Get status of all jobs.
    
    Returns:
        Dict mapping job IDs to their status
    """
    return _job_registry.copy()


def clear_old_jobs(max_age_hours: int = 24):
    """
    Clear old job records from registry.
    
    Args:
        max_age_hours: Maximum age of jobs to keep (default: 24 hours)
    """
    cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
    
    to_remove = []
    for job_id, job_data in _job_registry.items():
        start_time_str = job_data.get("start_time")
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            if start_time < cutoff_time:
                to_remove.append(job_id)
    
    for job_id in to_remove:
        del _job_registry[job_id]
    
    if to_remove:
        logger.info(f"Cleared {len(to_remove)} old jobs from registry")
