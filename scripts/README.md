# AfCFTA Data Scripts

This directory contains utility scripts for data analysis, validation, and corrections for the AfCFTA Trade Calculator.

## CSV Analysis and Validation Tools

### 1. analyze_validation_file.py
**Purpose:** Analyzes Excel validation files and displays their structure, columns, and sample data.

**Usage:**
```bash
python scripts/analyze_validation_file.py
```

**Description:**
- Reads the `validation_master.xlsx` file
- Lists all available sheets
- Displays dimensions, columns, and sample data for each sheet
- Provides detailed analysis of the main validation sheet

**Dependencies:** pandas, numpy

---

### 2. check_missing_csv.py
**Purpose:** Validates CSV completeness by checking if all 54 African countries are present in the CSV data.

**Usage:**
```bash
python scripts/check_missing_csv.py
```

**Description:**
- Compares country ISO codes from the backend database against CSV file
- Reports missing countries
- Validates data completeness

**Dependencies:** csv, backend.server (AFRICAN_COUNTRIES)

---

### 3. export_validation_csv.py
**Purpose:** Converts Excel validation data to CSV format with additional validation columns.

**Usage:**
```bash
python scripts/export_validation_csv.py
```

**Description:**
- Reads the source CSV file: `ZLECAF_54_PAYS_DONNEES_COMPLETES.csv`
- Adds validation columns: STATUS, CORRECTIONS (for GDP, Population, HDI, Sectors), SOURCES, COMMENTS
- Outputs to: `ZLECAF_VALIDATION.csv`
- Displays validation status statistics

**Dependencies:** pandas

**Output Columns Added:**
- STATUT_VALIDATION
- CORRECTIONS_PIB
- CORRECTIONS_POPULATION
- CORRECTIONS_IDH
- CORRECTIONS_SECTEURS
- SOURCES_SUPPLEMENTAIRES
- COMMENTAIRES
- VALIDE_PAR
- DATE_VALIDATION

---

## Data Correction Tools

### 4. fix_lpi_ranks.py
**Purpose:** Updates Logistics Performance Index (LPI) rankings with 2023 World Bank data.

**Usage:**
```bash
python scripts/fix_lpi_ranks.py
```

**Description:**
- Updates `classement_infrastructure_afrique.json` with accurate LPI 2023 scores and world rankings
- Covers ~27 African countries with verified World Bank LPI data
- Displays confirmation of key updates (e.g., Algeria, Angola)

**Data Source:** World Bank LPI 2023 Report & Interactive Data

**Key Updates:**
- LPI scores (1.0-5.0 scale)
- World rankings
- Infrastructure performance metrics

**Dependencies:** json

---

### 5. fix_tangermed_data.py
**Purpose:** Updates Tanger Med port data with accurate performance metrics and authority information.

**Usage:**
```bash
python scripts/fix_tangermed_data.py
```

**Description:**
- Corrects Tanger Med port operational data
- Updates port authority information
- Adds agent details and contact information
- Fixes performance metrics (containers handled, cargo volume, efficiency)

**Dependencies:** json, pathlib, random

**Updates:**
- Container handling capacity
- Cargo volumes
- Port efficiency metrics
- Authority contact information
- Agent listings

---

### 6. fix_tariffs_and_stats.py
**Purpose:** Comprehensive script to correct ZLECAf tariff rates and enrich trade statistics with 2023-2024 data.

**Usage:**
```bash
python scripts/fix_tariffs_and_stats.py
```

**Description:**
- Updates tariff rates for all 98 HS chapters based on official ZLECAf schedules
- Enriches trade statistics with 2023-2024 OEC (Observatory of Economic Complexity) data
- Categorizes products by sensitivity (normal, sensitive, excluded)
- Adds transition period information

**Data Covered:**
- Agricultural products (Chapters 01-24)
- Raw materials and minerals (Chapters 25-27)
- Chemicals (Chapters 28-38)
- Plastics and rubber (Chapters 39-40)
- Textiles (Chapters 50-63)
- Machinery and equipment (Chapters 84-85)
- Vehicles and transport (Chapters 86-89)

**Dependencies:** json, requests, asyncio, datetime

**Trade Statistics:**
- Total intra-African trade 2023-2024
- Growth rates
- ZLECAf implementation rates
- Top exporters and importers
- Sector-specific trade flows

---

## Other Utilities

### 7. update_comtrade_data.py
**Purpose:** Updates trade data from UN COMTRADE API.

**Usage:**
```bash
python scripts/update_comtrade_data.py
```

**Description:**
- Fetches latest trade data from UN COMTRADE v1 API
- Updates bilateral trade statistics
- Handles rate limiting and API authentication

---

## File Path Configuration

Most scripts use hard-coded paths for Docker deployment (`/app/...`). When running locally, you may need to:

1. Update file paths in the scripts to match your local directory structure
2. Set environment variables for data directories
3. Use symbolic links to maintain compatibility

**Example local setup:**
```bash
# Create data directory
mkdir -p data

# Copy validation files
cp validation_master.xlsx data/
cp ZLECAF_*.csv data/

# Update paths in scripts or create symlinks
ln -s data/validation_master.xlsx validation_master.xlsx
```

---

## Dependencies

Install required Python packages:

```bash
pip install pandas numpy openpyxl requests
```

Or use the project's requirements file:

```bash
pip install -r requirements.txt
```

---

## Notes

- **One-time scripts:** Most of these scripts are designed for one-time data corrections or migrations
- **Backup data:** Always backup your data files before running correction scripts
- **Validation:** After running any fix script, verify the output data is correct
- **French documentation:** Some scripts contain French comments and messages (legacy)

---

## Contributing

When adding new scripts:
1. Follow the naming convention: `verb_noun.py` (e.g., `fix_data.py`, `analyze_validation.py`)
2. Add documentation to this README
3. Include usage examples
4. List dependencies
5. Add error handling and logging

---

## Support

For issues or questions about these scripts, please open an issue in the GitHub repository.
