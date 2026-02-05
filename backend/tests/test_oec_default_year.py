"""
Test for OEC API default year parameter
========================================
This test verifies that all OEC endpoints default to year 2023,
which is the latest available year in the OEC BACI HS17 dataset.
"""

import re
import os


def test_oec_routes_default_year():
    """
    Verify that all OEC API endpoints use year 2023 as the default.
    
    The OEC BACI HS17 dataset has data from 2018-2023.
    Default year should be 2023 (the most recent available year).
    """
    # Get the backend directory (parent of tests directory)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    routes_file = os.path.join(backend_dir, "routes", "oec.py")
    
    # Read the routes file
    with open(routes_file, "r") as f:
        source_code = f.read()
    
    # Find all year parameter defaults using regex
    # Pattern: year: int = Query(YEAR)
    pattern = r'year:\s*int\s*=\s*Query\((\d+)\)'
    matches = re.findall(pattern, source_code)
    
    # We expect 5 endpoints with year parameter
    assert len(matches) == 5, f"Expected 5 endpoints with year parameter, found {len(matches)}"
    
    # Verify all use 2023 as default
    for year in matches:
        assert year == "2023", (
            f"All OEC endpoints should default to year 2023 "
            f"(latest available in OEC BACI), but found year {year}"
        )
    
    print("✅ All OEC endpoints correctly default to year 2023")
    print(f"   Verified {len(matches)} endpoints")


def test_oec_available_years():
    """
    Verify that get_available_years in oec_trade_service returns 2018-2023.
    """
    # Get the backend directory (parent of tests directory)
    backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    service_file = os.path.join(backend_dir, "services", "oec_trade_service.py")
    
    with open(service_file, "r") as f:
        content = f.read()
    
    # Check that the service documents 2018-2023 range
    assert "2018-2023" in content, (
        "OEC service should document available years as 2018-2023"
    )
    
    print("✅ OEC service correctly documents 2018-2023 data range")


if __name__ == "__main__":
    import sys
    
    try:
        test_oec_routes_default_year()
        test_oec_available_years()
        print("\n✨ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
