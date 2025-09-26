import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from api.main import app

client = TestClient(app)


@patch('api.routers.stocks.stock_service')
def test_get_stock_price_success(mock_stock_service):
    """Test successful stock price retrieval"""
    # Mock DataFrame response
    mock_df = pd.DataFrame({
        'open': [100.0, 101.0],
        'high': [102.0, 103.0], 
        'low': [99.0, 100.0],
        'close': [101.0, 102.0],
        'volume': [1000000, 1100000],
        'symbol': ['AAPL', 'AAPL']
    })
    mock_df.index = pd.to_datetime(['2023-01-01', '2023-01-02'])
    
    mock_stock_service.get_data.return_value = mock_df
    
    response = client.get("/api/v1/stocks/AAPL/price?period=1mo&interval=1d")
    
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert data["period"] == "1mo"
    assert data["interval"] == "1d"
    assert "data" in data
    assert data["count"] == 2


@patch('api.routers.stocks.stock_service')
def test_get_stock_price_not_found(mock_stock_service):
    """Test stock price retrieval with invalid symbol"""
    from orbis.sdk.exceptions import DataNotFoundException
    
    mock_stock_service.get_data.side_effect = DataNotFoundException("No data found")
    
    response = client.get("/api/v1/stocks/INVALID/price")
    
    assert response.status_code == 404
    data = response.json()
    assert "error" in data["detail"]


@patch('api.routers.stocks.stock_service')
def test_get_stock_info_success(mock_stock_service):
    """Test successful stock info retrieval"""
    mock_quote = {
        "symbol": "AAPL",
        "shortName": "Apple Inc.",
        "regularMarketPrice": 150.25,
        "regularMarketChange": 1.25,
        "regularMarketChangePercent": 0.84,
        "marketCap": 2400000000000,
        "currency": "USD"
    }
    
    mock_stock_service.get_quote.return_value = mock_quote
    
    response = client.get("/api/v1/stocks/AAPL/info")
    
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "AAPL"
    assert "info" in data
    assert data["info"]["symbol"] == "AAPL"


@patch('api.routers.stocks.stock_service')
def test_get_stock_info_validation_error(mock_stock_service):
    """Test stock info retrieval with validation error"""
    from orbis.sdk.exceptions import ValidationException
    
    mock_stock_service.get_quote.side_effect = ValidationException("Invalid symbol")
    
    response = client.get("/api/v1/stocks/INVALID_SYMBOL_TOO_LONG/info")
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data["detail"]


def test_stock_endpoints_require_symbol():
    """Test that stock endpoints require symbol parameter"""
    # Test missing symbol in price endpoint
    response = client.get("/api/v1/stocks//price")
    assert response.status_code == 404
    
    # Test missing symbol in info endpoint  
    response = client.get("/api/v1/stocks//info")
    assert response.status_code == 404