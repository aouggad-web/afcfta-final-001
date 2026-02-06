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
- **Real-time Data**: Integration with World Bank, UN COMTRADE v1, and OEC APIs
- **Automated Data Updates**: Daily automated updates from multiple data sources
- **📧 Notification System**: Email and Slack notifications for crawl events
- **📊 Data Export**: CSV and Excel export capabilities
- **🐳 Docker Ready**: Complete Docker deployment with docker-compose
- **🌍 54 Countries Supported**: All African countries with automated scrapers

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

### Trade Data Endpoints (NEW)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trade-data/latest` | GET | Get latest trade data using smart source selection |
| `/api/trade-data/compare-sources` | GET | Compare all data sources for freshness |
| `/api/trade-data/comtrade/{reporter}/{partner}` | GET | Get UN COMTRADE bilateral trade data directly |
| `/api/trade-data/wto/{reporter}/{partner}` | GET | Get WTO tariff and trade data directly |

### Export Endpoints (NEW)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/export/tariffs/csv` | GET | Export tariffs as CSV for a country |
| `/api/export/tariffs/excel` | GET | Export tariffs as Excel (multi-sheet for multiple countries) |

**Query Parameters:**
- `country`: Country code (required for CSV)
- `countries`: Comma-separated country codes (required for Excel)
- `latest`: Boolean, get only latest data (default: true)

#### Examples:

**Get Latest Trade Data with Smart Selection:**
```bash
GET /api/trade-data/latest?reporter=KEN&partner=GHA&hs_code=080300
```

**Compare Data Sources:**
```bash
GET /api/trade-data/compare-sources?countries=KEN&countries=GHA&countries=TZA
```

**Direct COMTRADE Access:**
```bash
GET /api/trade-data/comtrade/KEN/GHA?period=2025&hs_code=080300
```

**Direct WTO Access:**
```bash
GET /api/trade-data/wto/KEN/GHA?product_code=080300
```

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
- **External APIs**: World Bank API, OEC API, UN COMTRADE API, WTO API
- **Notifications**: Email (SMTP) and Slack webhooks
- **Task Management**: APScheduler for background jobs
- **Containerization**: Docker and Docker Compose

## 🐳 Docker Deployment

This application is fully containerized and ready for deployment:

```bash
# 1. Clone the repository
git clone https://github.com/aouggad-web/afcfta-final-001.git
cd afcfta-final-001

# 2. Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# 3. Start services
docker-compose up -d

# 4. Check logs
docker-compose logs -f backend
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📧 Notification System

The system supports automated notifications for crawling events:

### Supported Channels
- **Email**: SMTP notifications (Gmail, Outlook, SendGrid, etc.)
- **Slack**: Webhook-based notifications

### Notification Events
- 🚀 Crawl started
- ✅ Crawl successful
- ❌ Crawl failed
- ⚠️ Data validation issues

### Configuration

Set environment variables in `.env`:

```bash
# Email Notifications
EMAIL_NOTIFICATIONS_ENABLED=true
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SMTP_USER=your-email@gmail.com
EMAIL_SMTP_PASSWORD=your-app-password
EMAIL_TO=admin@example.com

# Slack Notifications
SLACK_NOTIFICATIONS_ENABLED=true
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL=#afcfta-monitoring
```

See [NOTIFICATIONS.md](NOTIFICATIONS.md) for detailed setup instructions.

## 📦 Data Sources

- **World Bank** - World Development Indicators (updated daily)
- **UN COMTRADE** - Most recent bilateral trade data (up to 500 calls/day free tier)
- **WTO Data Portal** - Tariff and trade policy data (free access)
- **OEC** - Atlas of Economic Complexity (Observatory of Economic Complexity)
- **UNCTAD** - Tariff data
- **AfDB** - African Economic Outlook
- **IMF** - Regional Economic Outlook

### Smart Data Source Selection

The API automatically selects the best data source based on:
1. **Data freshness** - Most recent data available
2. **API availability** - Rate limits and accessibility
3. **Data coverage** - Specific query requirements

Priority order: **UN COMTRADE** → **OEC** → **World Bank** → **WTO**

Data is automatically updated daily at 2:00 AM UTC via GitHub Actions. See [docs/AUTO_UPDATE_DATA.md](docs/AUTO_UPDATE_DATA.md) for details.

## 🌍 Coverage

- **54 African Countries** - Complete support for all AfCFTA member states
- **97 HS2 Sectors** with rules of origin
- **Real-time Trade Data**
- **Economic Projections** through 2030
- **Regional Tariff Systems**:
  - TEC CEDEAO (ECOWAS) - 15 countries
  - CET EAC (East African Community) - 6 countries
  - TDC CEMAC (Central Africa) - 6 countries
  - SACU (Southern African Customs Union) - 5 countries
  - Individual national tariffs - 22 countries

## 🤖 Automated Crawler System

The system includes automated scrapers for all 54 African countries:

- **Generic Scraper**: Fallback for countries without specific implementations
- **Regional Tariff Support**: Automatic handling of regional customs unions
- **Priority-based Crawling**: High-priority countries (major economies) crawled first
- **Data Validation**: Multi-level validation (quality, consistency, tariff rules)
- **Notification Integration**: Real-time alerts for crawl status

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

For more information, see:
- [docs/AUTO_UPDATE_DATA.md](docs/AUTO_UPDATE_DATA.md) - Automated data update system
- [docs/COMTRADE_INTEGRATION.md](docs/COMTRADE_INTEGRATION.md) - UN COMTRADE v1 API integration guide

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
