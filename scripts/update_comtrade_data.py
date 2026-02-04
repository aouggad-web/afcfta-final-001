#!/usr/bin/env python3
"""
Script to update UN COMTRADE trade data for African countries
Run daily via GitHub Actions
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient

# Add backend directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.comtrade_service import comtrade_service
from services.data_source_selector import data_source_selector

# African countries ISO3 codes (54 AfCFTA/ZLECAf members)
# AfCFTA = African Continental Free Trade Area (English)
# ZLECAf = Zone de Libre-Échange Continentale Africaine (French)
AFRICAN_COUNTRIES = [
    "DZA", "AGO", "BEN", "BWA", "BFA", "BDI", "CMR", "CPV", "CAF", "TCD",
    "COM", "COG", "COD", "CIV", "DJI", "EGY", "GNQ", "ERI", "ETH", "GAB",
    "GMB", "GHA", "GIN", "GNB", "KEN", "LSO", "LBR", "LBY", "MDG", "MWI",
    "MLI", "MRT", "MUS", "MAR", "MOZ", "NAM", "NER", "NGA", "RWA", "STP",
    "SEN", "SYC", "SLE", "SOM", "ZAF", "SSD", "SDN", "SWZ", "TZA", "TGO",
    "TUN", "UGA", "ZMB", "ZWE"
]


def main():
    """Main update function"""
    print(f"Starting COMTRADE data update: {datetime.utcnow().isoformat()}")
    
    # MongoDB connection (optional - only if MongoDB is configured)
    mongo_uri = os.getenv("MONGODB_URI")
    db_collection = None
    client = None
    
    if mongo_uri:
        try:
            client = MongoClient(mongo_uri)
            db = client["zlecaf_db"]
            db_collection = db["trade_data"]
            print("✓ Connected to MongoDB")
        except Exception as e:
            print(f"⚠ MongoDB connection failed (continuing without DB): {str(e)}")
            client = None
    else:
        print("ℹ No MongoDB URI configured - running without database storage")
    
    # Get current year
    current_year = str(datetime.now().year)
    
    # Fetch data for African countries
    print(f"\nFetching COMTRADE data for {len(AFRICAN_COUNTRIES)} countries...")
    
    updated_count = 0
    error_count = 0
    skipped_count = 0
    
    for i, country in enumerate(AFRICAN_COUNTRIES):
        try:
            print(f"\n[{i+1}/{len(AFRICAN_COUNTRIES)}] Processing {country}...")
            
            # Add delay between requests to avoid rate limiting (except first request)
            if i > 0:
                import time
                time.sleep(1)
            
            # Get bilateral trade data
            data = comtrade_service.get_bilateral_trade(
                reporter_code=country,
                partner_code="all",
                period=current_year
            )
            
            if data and data.get("data"):
                # Store in MongoDB if available
                if db_collection:
                    try:
                        document = {
                            "source": "UN_COMTRADE",
                            "reporter_country": country,
                            "period": current_year,
                            "data": data["data"],
                            "metadata": data.get("metadata", {}),
                            "updated_at": datetime.utcnow()
                        }
                        
                        db_collection.update_one(
                            {
                                "source": "UN_COMTRADE",
                                "reporter_country": country,
                                "period": current_year
                            },
                            {"$set": document},
                            upsert=True
                        )
                        print(f"✓ Updated {country} (stored in MongoDB)")
                    except Exception as db_error:
                        print(f"⚠ Warning: Failed to store {country} in MongoDB: {str(db_error)}")
                        print(f"✓ Updated {country} (data retrieved but not stored)")
                else:
                    print(f"✓ Updated {country}")
                
                updated_count += 1
            elif data is None:
                # API error occurred
                print(f"✗ Error retrieving data for {country} - skipping")
                error_count += 1
            else:
                # No data available for this country
                print(f"⚠ No data available for {country}")
                skipped_count += 1
                
        except Exception as e:
            error_count += 1
            print(f"✗ Unexpected error for {country}: {str(e)}")
            # Continue processing other countries
            continue
    
    # Run data source comparison
    print("\n" + "="*50)
    print("Comparing data sources...")
    try:
        # Only compare for countries that have data
        comparison_countries = AFRICAN_COUNTRIES[:10]
        comparison = data_source_selector.compare_data_sources(comparison_countries)
        
        # Store comparison results if MongoDB available
        if db_collection:
            try:
                comparison_collection = db_collection.database["data_source_comparisons"]
                comparison_collection.insert_one(comparison)
                print(f"✓ Comparison results stored in MongoDB")
            except Exception as db_error:
                print(f"⚠ Warning: Failed to store comparison in MongoDB: {str(db_error)}")
        
        print(f"Recommended source: {comparison.get('recommended_source', 'N/A')}")
    except Exception as e:
        print(f"⚠ Comparison failed (non-critical): {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"=== Update Complete ===")
    print(f"✓ Successfully updated: {updated_count}")
    print(f"⚠ Skipped (no data): {skipped_count}")
    print(f"✗ Errors: {error_count}")
    print(f"📊 Total processed: {updated_count + skipped_count + error_count}/{len(AFRICAN_COUNTRIES)}")
    print(f"⏰ Timestamp: {datetime.utcnow().isoformat()}")
    print(f"{'='*50}")
    
    if client is not None:
        client.close()
    
    # Exit with success even if some countries failed
    # This allows the workflow to continue with partial data
    if updated_count > 0:
        print("\n✅ Update completed successfully (partial data is acceptable)")
        sys.exit(0)
    else:
        print("\n❌ Update failed - no data retrieved")
        sys.exit(1)


if __name__ == "__main__":
    main()
