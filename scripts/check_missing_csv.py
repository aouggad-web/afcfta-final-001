#!/usr/bin/env python3
"""
Check for missing countries in CSV data files.
"""
import csv
import sys
import os

def check_missing_countries(csv_path=None):
    """Check for missing countries in the CSV file.
    
    Args:
        csv_path: Path to the CSV file. If None, tries multiple default locations.
    """
    # Import backend here to allow script to run standalone
    try:
        # Add parent directory to path to allow import
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from backend.server import AFRICAN_COUNTRIES
    except ImportError as e:
        print(f"❌ Error: Could not import backend.server: {e}")
        print("   Make sure you're running from the project root directory")
        print("   and that all dependencies are installed: pip install -r requirements.txt")
        return False
    
    # Get all 54 ISO codes
    all_isos = set(c['iso3'] for c in AFRICAN_COUNTRIES)
    
    if csv_path is None:
        # Try multiple possible paths
        possible_paths = [
            '/app/ZLECAf_ENRICHI_2024_COMMERCE.csv',  # Docker path
            'ZLECAf_ENRICHI_2024_COMMERCE.csv',       # Current directory
        ]
        for path in possible_paths:
            if os.path.exists(path):
                csv_path = path
                break
        
        if csv_path is None:
            print("❌ Error: Could not find ZLECAf_ENRICHI_2024_COMMERCE.csv")
            print(f"   Searched in: {possible_paths}")
            print("   Usage: python check_missing_csv.py [path/to/csv_file.csv]")
            return False
    
    if not os.path.exists(csv_path):
        print(f"❌ Error: File not found: {csv_path}")
        return False
    
    print(f"📂 Processing file: {csv_path}")
    
    # Get ISOs in CSV
    csv_isos = set()
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                csv_isos.add(row['Code_ISO'])
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

    missing = all_isos - csv_isos
    print(f"\n📊 Results:")
    print(f"Total defined countries: {len(all_isos)}")
    print(f"Countries in CSV: {len(csv_isos)}")
    print(f"Missing countries ({len(missing)}): {missing}")
    
    return len(missing) == 0

if __name__ == "__main__":
    # Get file path from command line argument if provided
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    success = check_missing_countries(file_path)
    sys.exit(0 if success else 1)
