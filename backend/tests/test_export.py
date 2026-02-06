"""
Tests for export router endpoints
"""
import pytest
from httpx import AsyncClient
import io
import pandas as pd
from backend.server import app
from backend.routers.export_router import init_db


pytestmark = pytest.mark.asyncio


@pytest.fixture
async def client():
    """Create test client"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def mock_db(monkeypatch):
    """Mock database for testing"""
    class MockCollection:
        async def find_one(self, query, **kwargs):
            if query.get("country_code") == "KEN":
                return {
                    "country_code": "KEN",
                    "imported_at": "2024-01-01T00:00:00",
                    "tariffs": {
                        "tariff_lines": [
                            {
                                "hs_code": "0101.21.00",
                                "description": "Live horses",
                                "unit": "Number",
                                "customs_duty": "25%",
                                "vat": "16%",
                                "source": "test"
                            },
                            {
                                "hs_code": "0102.10.00",
                                "description": "Live cattle",
                                "unit": "Number",
                                "customs_duty": "25%",
                                "vat": "16%",
                                "source": "test"
                            }
                        ]
                    }
                }
            return None
        
        def find(self, query, **kwargs):
            class MockCursor:
                async def to_list(self, length):
                    return [await self.parent.find_one(query)]
                
                def sort(self, *args):
                    return self
            
            cursor = MockCursor()
            cursor.parent = self
            return cursor
    
    class MockDB:
        def __getitem__(self, name):
            return MockCollection()
    
    mock_db_instance = MockDB()
    init_db(mock_db_instance)
    return mock_db_instance


class TestExportTariffsCSV:
    """Test CSV export endpoint"""
    
    async def test_export_tariffs_csv_success(self, client, mock_db):
        """Test successful CSV export"""
        response = await client.get("/api/export/tariffs/csv?country=KEN")
        
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert "attachment" in response.headers["content-disposition"]
        assert "tariffs_KEN_" in response.headers["content-disposition"]
        
        # Check CSV content
        content = response.text
        assert "hs_code" in content
        assert "0101.21.00" in content
        assert "Live horses" in content
    
    async def test_export_tariffs_csv_not_found(self, client, mock_db):
        """Test CSV export for non-existent country"""
        response = await client.get("/api/export/tariffs/csv?country=XXX")
        
        assert response.status_code == 404
        assert "No data" in response.json()["detail"]
    
    async def test_export_tariffs_csv_missing_param(self, client):
        """Test CSV export without country parameter"""
        response = await client.get("/api/export/tariffs/csv")
        
        assert response.status_code == 422  # Validation error


class TestExportTariffsExcel:
    """Test Excel export endpoint"""
    
    async def test_export_tariffs_excel_success(self, client, mock_db):
        """Test successful Excel export"""
        response = await client.get("/api/export/tariffs/excel?countries=KEN")
        
        assert response.status_code == 200
        assert "spreadsheet" in response.headers["content-type"]
        assert "attachment" in response.headers["content-disposition"]
        assert ".xlsx" in response.headers["content-disposition"]
        
        # Verify it's valid Excel by trying to read it
        excel_data = io.BytesIO(response.content)
        df = pd.read_excel(excel_data, sheet_name="KEN")
        
        assert len(df) == 2  # 2 tariff lines
        assert "HS Code" in df.columns
        assert "Description" in df.columns
    
    async def test_export_tariffs_excel_multiple_countries(self, client, mock_db):
        """Test Excel export with multiple countries"""
        response = await client.get("/api/export/tariffs/excel?countries=KEN,TZA")
        
        assert response.status_code == 200
        
        # Should still work even if one country has no data
        excel_data = io.BytesIO(response.content)
        xls = pd.ExcelFile(excel_data)
        
        # At least Kenya should be present
        assert "KEN" in xls.sheet_names
    
    async def test_export_tariffs_excel_missing_param(self, client):
        """Test Excel export without countries parameter"""
        response = await client.get("/api/export/tariffs/excel")
        
        assert response.status_code == 422  # Validation error


class TestExportValidationIntegration:
    """Integration tests for export functionality"""
    
    async def test_csv_format_consistency(self, client, mock_db):
        """Test that CSV format is consistent"""
        response = await client.get("/api/export/tariffs/csv?country=KEN")
        
        content = response.text
        lines = content.strip().split("\n")
        
        # Check header
        header = lines[0].split(",")
        assert "country" in header
        assert "hs_code" in header
        assert "description" in header
        
        # Check data rows have same number of columns as header
        for line in lines[1:]:
            assert len(line.split(",")) == len(header)
    
    async def test_export_filename_format(self, client, mock_db):
        """Test that export filenames have correct format"""
        response = await client.get("/api/export/tariffs/csv?country=KEN")
        
        filename = response.headers["content-disposition"]
        # Format should be: tariffs_KEN_YYYYMMDD.csv
        assert "tariffs_KEN_" in filename
        assert ".csv" in filename
