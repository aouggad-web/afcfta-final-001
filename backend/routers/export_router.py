"""
API endpoints pour exporter les données
"""
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from datetime import datetime
import csv
import io
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
import os

router = APIRouter(prefix="/api/export", tags=["export"])

# MongoDB connection - will be initialized from main app
_db = None


def init_db(db):
    """Initialize database connection"""
    global _db
    _db = db


def get_db():
    """Get database instance"""
    if _db is None:
        # Fallback: create connection if not initialized
        mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017/')
        client = AsyncIOMotorClient(mongo_url)
        return client[os.environ.get('DB_NAME', 'afcfta')]
    return _db


@router.get("/tariffs/csv")
async def export_tariffs_csv(
    country: str = Query(..., description="Country code"),
    latest: bool = Query(True, description="Latest only")
):
    """Export tariffs as CSV"""
    try:
        db = get_db()
        query = {"country_code": country}

        if latest:
            data = await db["customs_data"].find_one(query, sort=[("imported_at", -1)])
            if not data:
                raise HTTPException(404, f"No data for {country}")
            data_list = [data]
        else:
            cursor = db["customs_data"].find(query).sort("imported_at", -1)
            data_list = await cursor.to_list(length=None)

        rows = []
        for data in data_list:
            for line in data.get("tariffs", {}).get("tariff_lines", []):
                rows.append({
                    "country": data.get("country_code"),
                    "hs_code": line.get("hs_code", ""),
                    "description": line.get("description", ""),
                    "unit": line.get("unit", ""),
                    "customs_duty": line.get("customs_duty", ""),
                    "vat": line.get("vat", ""),
                    "source": line.get("source", ""),
                    "date": data.get("imported_at", "")
                })

        output = io.StringIO()
        if rows:
            writer = csv.DictWriter(output, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

        filename = f"tariffs_{country}_{datetime.utcnow().strftime('%Y%m%d')}.csv"

        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/tariffs/excel")
async def export_tariffs_excel(
    countries: str = Query(..., description="Comma-separated country codes"),
    latest: bool = Query(True)
):
    """Export tariffs as Excel (multi-sheet)"""
    try:
        db = get_db()
        country_list = [c.strip() for c in countries.split(",")]
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for country in country_list:
                query = {"country_code": country}
                data = await db["customs_data"].find_one(query, sort=[("imported_at", -1)])

                if not data:
                    continue

                rows = []
                for line in data.get("tariffs", {}).get("tariff_lines", []):
                    rows.append({
                        "HS Code": line.get("hs_code"),
                        "Description": line.get("description"),
                        "Unit": line.get("unit"),
                        "Customs Duty": line.get("customs_duty"),
                        "VAT": line.get("vat")
                    })

                if rows:
                    df = pd.DataFrame(rows)
                    df.to_excel(writer, sheet_name=country[:31], index=False)  # Excel sheet name limit is 31 chars

        output.seek(0)
        filename = f"tariffs_{datetime.utcnow().strftime('%Y%m%d')}.xlsx"

        return StreamingResponse(
            io.BytesIO(output.read()),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(500, str(e))
