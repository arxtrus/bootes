"""
Pytest configuration and fixtures for Orbis SDK tests
"""

from unittest.mock import patch

import pytest
from orbis.sdk import Config


@pytest.fixture
def test_config():
    """Fixture providing test configuration"""
    return Config(
        timeout=10,
        max_retries=2,
        retry_delay=0.1,
        default_stock_interval="1d",
        default_stock_period="1y",
        cache_enabled=False,
    )


@pytest.fixture
def mock_requests_get():
    """Fixture providing mocked requests.get"""
    with patch("requests.get") as mock_get:
        yield mock_get


@pytest.fixture
def sample_yahoo_response():
    """Sample Yahoo Finance API response"""
    return {
        "chart": {
            "result": [
                {
                    "timestamp": [1640995200, 1641081600, 1641168000],
                    "indicators": {
                        "quote": [
                            {
                                "open": [182.63, 181.85, 179.61],
                                "high": [182.88, 183.04, 180.17],
                                "low": [177.71, 179.12, 177.49],
                                "close": [177.57, 182.01, 179.70],
                                "volume": [104487900, 76138000, 64062300],
                            }
                        ]
                    },
                }
            ]
        }
    }


@pytest.fixture
def sample_yahoo_quote_response():
    """Sample Yahoo Finance quote response"""
    return {
        "quoteResponse": {
            "result": [
                {
                    "symbol": "AAPL",
                    "shortName": "Apple Inc.",
                    "longName": "Apple Inc.",
                    "regularMarketPrice": 150.25,
                    "regularMarketChange": 2.15,
                    "regularMarketChangePercent": 1.45,
                    "regularMarketVolume": 85000000,
                    "marketCap": 2500000000000,
                    "currency": "USD",
                    "fullExchangeName": "NASDAQ Global Select",
                    "marketState": "REGULAR",
                }
            ]
        }
    }


@pytest.fixture
def sample_forex_response():
    """Sample exchange rate API response"""
    return {
        "base": "USD",
        "date": "2025-01-01",
        "rates": {"EUR": 0.85, "GBP": 0.75, "JPY": 110.0, "KRW": 1300.0, "CAD": 1.25},
        "timestamp": "2025-01-01T12:00:00",
    }


@pytest.fixture
def sample_crypto_price_response():
    """Sample CoinGecko price response"""
    return {
        "bitcoin": {
            "usd": 45000.0,
            "usd_market_cap": 850000000000,
            "usd_24h_vol": 35000000000,
            "usd_24h_change": 2.5,
            "last_updated_at": 1640995200,
        }
    }


@pytest.fixture
def sample_crypto_market_response():
    """Sample CoinGecko market data response"""
    return {
        "id": "bitcoin",
        "symbol": "btc",
        "name": "Bitcoin",
        "market_data": {
            "current_price": {"usd": 45000.0},
            "market_cap": {"usd": 850000000000},
            "market_cap_rank": 1,
            "total_volume": {"usd": 35000000000},
            "high_24h": {"usd": 46000.0},
            "low_24h": {"usd": 44000.0},
            "price_change_24h": 1125.0,
            "price_change_percentage_24h": 2.5,
            "circulating_supply": 19000000,
            "total_supply": 21000000,
            "max_supply": 21000000,
            "ath": {"usd": 69000.0},
            "atl": {"usd": 67.81},
        },
        "last_updated": "2025-01-01T12:00:00.000Z",
    }


@pytest.fixture
def sample_crypto_top_response():
    """Sample CoinGecko top cryptocurrencies response"""
    return [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 45000.0,
            "market_cap": 850000000000,
            "market_cap_rank": 1,
            "total_volume": 35000000000,
            "price_change_percentage_24h": 2.5,
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "current_price": 3200.0,
            "market_cap": 385000000000,
            "market_cap_rank": 2,
            "total_volume": 18000000000,
            "price_change_percentage_24h": 1.8,
        },
    ]


@pytest.fixture
def sample_crypto_search_response():
    """Sample CoinGecko search response"""
    return {
        "coins": [
            {
                "id": "bitcoin",
                "name": "Bitcoin",
                "symbol": "BTC",
                "market_cap_rank": 1,
                "thumb": "https://assets.coingecko.com/coins/images/1/thumb/bitcoin.png",
                "large": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
            }
        ]
    }
