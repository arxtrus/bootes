# Orbis Core API

FastAPI-based RESTful API server that provides financial data through orbis-sdk.

## Features

- **Stock Data**: OHLCV data and real-time quotes via Yahoo Finance
- **Forex Data**: Exchange rate information for major currency pairs
- **Cryptocurrency Data**: Price and market data via CoinGecko  
- **Economic Indicators**: Economic data API (under development)

## API Endpoints

### Stocks
- `GET /api/v1/stocks/{symbol}/price?period=1mo&interval=1d` - Stock price data
- `GET /api/v1/stocks/{symbol}/info` - Real-time stock information

### Forex  
- `GET /api/v1/forex/{pair}/rate?period=1mo` - Exchange rate information (e.g., USD-KRW)
- `GET /api/v1/forex/major-pairs` - Major currency pairs
- `GET /api/v1/forex/supported-currencies` - Supported currencies list

### Crypto
- `GET /api/v1/crypto/{symbol}/price?currency=USD` - Cryptocurrency price
- `GET /api/v1/crypto/{symbol}/market?currency=USD` - Detailed market data
- `GET /api/v1/crypto/top?currency=USD&limit=10` - Top cryptocurrencies by market cap
- `GET /api/v1/crypto/search?query=bitcoin` - Cryptocurrency search

### Economics
- `GET /api/v1/economics/{indicator}` - Economic indicator data (under development)
- `GET /api/v1/economics/indicators` - Available indicators list

### System
- `GET /health` - Health check
- `GET /docs` - API documentation (Swagger UI)
- `GET /redoc` - API documentation (ReDoc)

## Installation and Running

### Requirements
- Python 3.9+
- orbis-sdk installation required

### Development Environment Setup

```bash
# Install dependencies
uv sync --dev

# Run development server
cd src
python -m api.main

# Or use uvicorn directly
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Environment Variables Configuration

You can create a `.env` file to customize configuration:

```bash
# Server Configuration
HOST=0.0.0.0
PORT=8000
RELOAD=true

# CORS Configuration  
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# SDK Configuration
SDK_TIMEOUT=30
SDK_RETRIES=3

# Logging
LOG_LEVEL=INFO
```

## Testing

```bash
# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=api/
```

## 📝 Response Examples

### Stock Price Data
```json
{
  "symbol": "AAPL",
  "period": "1mo", 
  "interval": "1d",
  "data": [
    {
      "timestamp": "2023-01-01T00:00:00",
      "open": 130.0,
      "high": 135.0,
      "low": 128.0, 
      "close": 134.0,
      "volume": 50000000,
      "symbol": "AAPL"
    }
  ],
  "count": 1
}
```

### Error Response
```json
{
  "detail": {
    "error": "No data found for symbol: INVALID"
  }
}
```

## Architecture

```
orbis-core/
├── src/api/
│   ├── main.py          # FastAPI app initialization
│   ├── config.py        # Configuration management
│   └── routers/         # API routers
│       ├── stocks.py    # Stocks API
│       ├── forex.py     # Forex API  
│       ├── crypto.py    # Crypto API
│       └── economics.py # Economics API
├── tests/               # Test code
└── pyproject.toml       # Project configuration
```

## Development Tools

- **FastAPI**: High-performance web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pandas**: Data processing
- **Pytest**: Testing framework
