"""
Production routes - FAOSTAT, UNIDO data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter(prefix="/production")

# Note: This file contains stub routes. 
# The actual implementation remains in server.py until full migration.
# Routes to migrate:
# - GET /production/statistics
# - GET /production/macro
# - GET /production/macro/{country_iso3}
# - GET /production/agriculture
# - GET /production/agriculture/{country_iso3}
# - GET /production/manufacturing
# - GET /production/manufacturing/{country_iso3}
# - GET /production/mining
# - GET /production/mining/{country_iso3}
# - GET /production/overview/{country_iso3}
# - GET /production/faostat/*
# - GET /production/unido/*
