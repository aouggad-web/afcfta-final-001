# ZLECAf Trade Calculator / Calculateur Commercial ZLECAf

![API Status](https://img.shields.io/badge/API-Online-success)
![Version](https://img.shields.io/badge/version-2.0.0-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-Connected-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A comprehensive tariff calculator and trade information system for the African Continental Free Trade Area (AfCFTA/ZLECAf).

## 🚀 Features

- **Tariff Calculations**: Calculate tariffs between 54 African countries
- **Rules of Origin**: Access ZLECAf rules of origin by HS code
- **Country Profiles**: Detailed economic profiles for all member states
- **Trade Statistics**: Comprehensive trade statistics and projections
- **Real-time Data**: Integration with World Bank and OEC APIs
- **Automated Data Updates**: Daily automated updates from World Bank API and other sources

## 📊 API Endpoints

### Health & Observability

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Simple health check |
| `/api/health/status` | GET | Detailed health status with system checks |

The health endpoints provide real-time monitoring of:
- Database connectivity (MongoDB)
- API endpoints availability
- Data integrity checks
- Service version information

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/` | GET | API welcome message |
| `/api/countries` | GET | List all 54 ZLECAf member countries |
| `/api/country-profile/{country_code}` | GET | Get detailed country economic profile |
| `/api/calculate-tariff` | POST | Calculate tariffs between countries |
| `/api/rules-of-origin/{hs_code}` | GET | Get rules of origin for HS code |
| `/api/statistics` | GET | Get comprehensive ZLECAf statistics |

## 🏥 Health Monitoring

### Health Check Response

**Endpoint**: `GET /api/health`

```json
{
  "status": "healthy",
  "service": "ZLECAf API",
  "version": "2.0.0",
  "timestamp": "2025-01-15T10:30:00.000Z"
}
```

### Detailed Status Response

**Endpoint**: `GET /api/health/status`

```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00.000Z",
  "service": "ZLECAf API",
  "version": "2.0.0",
  "checks": {
    "database": {
      "status": "healthy",
      "message": "MongoDB connection active"
    },
    "api_endpoints": {
      "status": "healthy",
      "available_endpoints": [...]
    },
    "data": {
      "status": "healthy",
      "countries_count": 54,
      "rules_of_origin_sectors": 97
    }
  }
}
```

## 🔧 Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React with Shadcn/UI components
- **Database**: MongoDB
- **External APIs**: World Bank API, OEC API

## 📦 Data Sources

- World Bank - World Development Indicators (updated daily)
- UNCTAD - Tariff data
- OEC - Atlas of Economic Complexity
- AfDB - African Economic Outlook
- IMF - Regional Economic Outlook

Data is automatically updated daily at 2:00 AM UTC via GitHub Actions. See [docs/AUTO_UPDATE_DATA.md](docs/AUTO_UPDATE_DATA.md) for details.

## 🌍 Coverage

- **54 African Countries**
- **97 HS2 Sectors** with rules of origin
- **Real-time Trade Data**
- **Economic Projections** through 2030

## 🚦 Status Badges Explained

- ![API Status](https://img.shields.io/badge/API-Online-success) - API is operational
- ![MongoDB](https://img.shields.io/badge/MongoDB-Connected-green) - Database connection active
- ![Version](https://img.shields.io/badge/version-2.0.0-blue) - Current API version

## 📈 Monitoring Best Practices

1. **Regular Health Checks**: Poll `/api/health` endpoint every 30 seconds
2. **Detailed Status**: Check `/api/health/status` for comprehensive diagnostics
3. **Database Monitoring**: Monitor MongoDB connection status
4. **API Response Times**: Track endpoint response times
5. **Error Rates**: Monitor 4xx and 5xx response rates

## 🔍 Quick Start

### Check API Health

```bash
curl https://your-domain.com/api/health
```

### Get All Countries

```bash
curl https://your-domain.com/api/countries
```

### Calculate Tariff

```bash
curl -X POST https://your-domain.com/api/calculate-tariff \
  -H "Content-Type: application/json" \
  -d '{
    "origin_country": "KE",
    "destination_country": "GH",
    "hs_code": "080300",
    "value": 10000
  }'
```

## 🔄 Automated Data Updates

The system automatically updates economic data daily from external sources:

- **Schedule**: Daily at 2:00 AM UTC
- **Sources**: World Bank API, country profiles, trade statistics
- **Process**: Automated via GitHub Actions
- **Monitoring**: Update reports available in Actions artifacts

For more information, see [docs/AUTO_UPDATE_DATA.md](docs/AUTO_UPDATE_DATA.md).

To manually trigger an update:
1. Go to the Actions tab on GitHub
2. Select "Auto Update Data" workflow
3. Click "Run workflow"

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions, please open an issue on GitHub.
