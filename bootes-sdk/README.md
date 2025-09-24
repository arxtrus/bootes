# bootes SDK

A Python SDK for financial data collection designed for the bootes open-source investment terminal backend. It provides seamless access to stock, forex, and cryptocurrency data from various sources.

## Features

- 📈 **Multiple Data Sources**: Support for stocks, forex, and cryptocurrency data
- 🔌 **FastAPI Compatible**: Easy integration with FastAPI backends
- 🛡️ **Robust Error Handling**: Systematic handling of network errors, API errors, and more
- ⚙️ **Flexible Configuration**: Environment variable and configuration file support
- 🔄 **Extensible Architecture**: Modular structure for easy addition of new data sources
- 🆓 **Free API First**: Prioritizes free data sources that work without API keys

## Supported Data Sources

### Stocks (StockService)
- Yahoo Finance API integration
- OHLCV data retrieval
- Real-time stock quotes
- Multiple time intervals and periods

### Forex (ForexService)
- exchangerate-api.com integration (free)
- Real-time exchange rate data
- Major currency pairs support
- 150+ supported currencies

### Cryptocurrency (CryptoService)
- CoinGecko API integration (free)
- Real-time cryptocurrency prices
- Market data (market cap, volume, etc.)
- Top cryptocurrencies list
- Cryptocurrency search functionality

## Quick Start

### Basic Usage

```python
from bootes.sdk import BootesSDK

# Initialize SDK
sdk = BootesSDK()

# Get stock data
stock_data = sdk.stock.get_data("AAPL", interval="1d", period="1y")
print(f"AAPL data: {len(stock_data)} records")

# Get real-time quote
quote = sdk.stock.get_quote("AAPL")
print(f"AAPL current price: ${quote['regularMarketPrice']}")

# Get forex data
forex_data = sdk.forex.get_rate("USD", "KRW")
print(f"USD/KRW: {forex_data['rate']}")

# Get crypto data
crypto_data = sdk.crypto.get_data("bitcoin", vs_currency="usd")
print(f"Bitcoin: ${crypto_data['price']:,.2f}")
```

### Individual Service Usage

```python
from bootes.sdk import StockService, ForexService, CryptoService

# Initialize individual services
stock = StockService()
forex = ForexService()
crypto = CryptoService()

# Usage remains the same
data = stock.get_data("MSFT")
```

### FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
from bootes.sdk import BootesSDK
from bootes.sdk.exceptions import BootesSDKException

app = FastAPI()
sdk = BootesSDK()

@app.get("/stock/{symbol}")
async def get_stock(symbol: str):
    try:
        data = sdk.stock.get_data(symbol)
        return {"symbol": symbol, "data": data.to_dict("records")}
    except BootesSDKException as e:
        raise HTTPException(status_code=400, detail=str(e))
```

## Configuration

Configure using environment variables:

```bash
# API keys (optional)
export ALPHA_VANTAGE_API_KEY=your_key_here
export FINNHUB_API_KEY=your_key_here

# Request settings
export BOOTES_TIMEOUT=30
export BOOTES_MAX_RETRIES=3
export BOOTES_RETRY_DELAY=1.0

# Default values
export BOOTES_DEFAULT_INTERVAL=1d
export BOOTES_DEFAULT_PERIOD=1y

# Cache settings
export BOOTES_CACHE_ENABLED=true
export BOOTES_CACHE_TTL=300
```

Configure in Python code:

```python
from bootes.sdk import Config, BootesSDK

config = Config(
    timeout=60,
    max_retries=5,
    default_stock_interval="1h"
)

sdk = BootesSDK(config)
```

## API Reference

### StockService

```python
# Get OHLCV data
data = stock.get_data(
    symbol="AAPL",           # Stock symbol
    interval="1d",           # 1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo
    period="1y"              # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
)

# Get real-time quote
quote = stock.get_quote("AAPL")
```

### ForexService

```python
# Get all exchange rates
rates = forex.get_data("USD")

# Get specific currency pair
rate = forex.get_rate("USD", "KRW")

# Get major currency pairs
major_pairs = forex.get_major_pairs()

# Get supported currencies
currencies = forex.get_supported_currencies()
```

### CryptoService

```python
# Get cryptocurrency price
price = crypto.get_data("bitcoin", vs_currency="usd")

# Get detailed market data
market = crypto.get_market_data("bitcoin")

# Get top cryptocurrencies
top = crypto.get_top_cryptos(limit=10)

# Search cryptocurrencies
results = crypto.search_crypto("ethereum")
```

## Exception Handling

The SDK provides various exception types for systematic error handling:

```python
from bootes.sdk.exceptions import (
    BootesSDKException,      # Base exception
    APIException,            # API errors
    DataNotFoundException,   # Data not found
    RateLimitException,      # API rate limits
    ValidationException,     # Input validation errors
    NetworkException         # Network errors
)

try:
    data = sdk.stock.get_data("INVALID")
except DataNotFoundException as e:
    print(f"Data not found: {e.message}")
except ValidationException as e:
    print(f"Validation error: {e.field} - {e.message}")
except APIException as e:
    print(f"API error: {e.status_code} - {e.message}")
```

## Development

### Development Setup

```bash
# Install dependencies
uv sync --dev

# Code formatting
uv run black src/ tests/
uv run isort src/ tests/

# Linting
uv run flake8 src/
uv run mypy src/

# Run tests
uv run pytest tests/ -v --cov=bootes.sdk
```

### Testing

```bash
# Run all tests
uv run pytest

# Test specific service
uv run pytest tests/test_stock.py

# Run with coverage
uv run pytest --cov=bootes.sdk --cov-report=html
```

## Project Structure

```
bootes-sdk/
├── src/bootes/sdk/
│   ├── __init__.py          # Main SDK class
│   ├── config/              # Configuration management
│   ├── exceptions/          # Exception classes
│   ├── interfaces/          # Base interfaces
│   ├── services/            # Data services
│   │   ├── stock.py        # Stock service
│   │   ├── forex.py        # Forex service
│   │   └── crypto.py       # Cryptocurrency service
│   └── utils/              # Utilities
├── examples/               # Usage examples
├── tests/                 # Test code
├── pyproject.toml        # Project configuration
└── README.md
```

## Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) - Stock data
- [exchangerate-api.com](https://exchangerate-api.com/) - Exchange rate data
- [CoinGecko](https://www.coingecko.com/) - Cryptocurrency data
