"""
Statistics routes - Trade statistics, UNCTAD data
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter(prefix="/statistics")

# Note: This file contains stub routes. 
# The actual implementation remains in server.py until full migration.
# Routes to migrate:
# - GET /statistics
# - GET /trade-performance
# - GET /trade-performance-intra-african
# - GET /statistics/trade-products/*
# - GET /statistics/unctad/*
