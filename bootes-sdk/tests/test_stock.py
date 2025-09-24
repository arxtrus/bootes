"""
Tests for StockService
"""

from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from bootes.sdk.exceptions import (
    DataNotFoundException,
    NetworkException,
    ValidationException,
)
from bootes.sdk.services.stock import StockService


class TestStockService:
    def test_init_with_config(self, test_config):
        """Test StockService initialization with custom config"""
        service = StockService(test_config)
        assert service.config == test_config
        assert service.base_url == "https://query1.finance.yahoo.com/v8/finance/chart"

    def test_init_without_config(self):
        """Test StockService initialization without config"""
        service = StockService()
        assert service.config is not None

    def test_validate_symbol_valid(self):
        """Test symbol validation with valid symbols"""
        service = StockService()

        valid_symbols = ["AAPL", "MSFT", "GOOGL", "TSLA", "BRK.B", "BTC-USD"]
        for symbol in valid_symbols:
            assert service.validate_symbol(symbol) is True

    def test_validate_symbol_invalid(self):
        """Test symbol validation with invalid symbols"""
        service = StockService()

        invalid_symbols = ["", "A" * 11, None, 123, "AAPL$", "AAPL@"]
        for symbol in invalid_symbols:
            assert service.validate_symbol(symbol) is False

    @patch("requests.get")
    def test_get_data_success(self, mock_get, test_config, sample_yahoo_response):
        """Test successful data retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = sample_yahoo_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = StockService(test_config)
        result = service.get_data("AAPL", interval="1d", period="1y")

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert "open" in result.columns
        assert "high" in result.columns
        assert "low" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns
        assert "symbol" in result.columns
        assert result["symbol"].iloc[0] == "AAPL"

        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "AAPL" in args[0]
        assert kwargs["timeout"] == test_config.timeout

    @patch("requests.get")
    def test_get_data_invalid_symbol(self, mock_get, test_config):
        """Test data retrieval with invalid symbol"""
        service = StockService(test_config)

        with pytest.raises(ValidationException) as exc_info:
            service.get_data("INVALID$SYMBOL")

        assert "Invalid stock symbol" in str(exc_info.value)
        mock_get.assert_not_called()

    @patch("requests.get")
    def test_get_data_no_data_found(self, mock_get, test_config):
        """Test data retrieval when no data is found"""
        mock_response = Mock()
        mock_response.json.return_value = {"chart": {"result": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = StockService(test_config)

        with pytest.raises(DataNotFoundException) as exc_info:
            service.get_data("AAPL")

        assert "No data found for symbol: AAPL" in str(exc_info.value)

    @patch("requests.get")
    def test_get_data_network_error(self, mock_get, test_config):
        """Test data retrieval with network error"""
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        service = StockService(test_config)

        with pytest.raises(NetworkException) as exc_info:
            service.get_data("AAPL")

        assert "Failed to fetch data for AAPL" in str(exc_info.value)

    @patch("requests.get")
    def test_get_quote_success(
        self, mock_get, test_config, sample_yahoo_quote_response
    ):
        """Test successful quote retrieval"""
        mock_response = Mock()
        mock_response.json.return_value = sample_yahoo_quote_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = StockService(test_config)
        result = service.get_quote("AAPL")

        assert isinstance(result, dict)
        assert result["symbol"] == "AAPL"
        assert result["shortName"] == "Apple Inc."
        assert result["regularMarketPrice"] == 150.25
        assert "timestamp" in result

        mock_get.assert_called_once()

    @patch("requests.get")
    def test_get_quote_invalid_symbol(self, mock_get, test_config):
        """Test quote retrieval with invalid symbol"""
        service = StockService(test_config)

        with pytest.raises(ValidationException):
            service.get_quote("INVALID$")

        mock_get.assert_not_called()

    @patch("requests.get")
    def test_get_quote_no_data(self, mock_get, test_config):
        """Test quote retrieval when no data is found"""
        mock_response = Mock()
        mock_response.json.return_value = {"quoteResponse": {"result": []}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = StockService(test_config)

        with pytest.raises(DataNotFoundException) as exc_info:
            service.get_quote("INVALID")

        assert "No quote data found for symbol: INVALID" in str(exc_info.value)

    def test_parse_yahoo_data(self, test_config, sample_yahoo_response):
        """Test Yahoo data parsing"""
        service = StockService(test_config)
        result_data = sample_yahoo_response["chart"]["result"][0]

        df = service._parse_yahoo_data(result_data, "AAPL")

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 3
        assert df.index.name == "timestamp"
        assert isinstance(df.index[0], datetime)
        assert df["symbol"].iloc[0] == "AAPL"

    def test_format_symbol(self, test_config):
        """Test symbol formatting"""
        service = StockService(test_config)

        assert service._format_symbol("aapl") == "AAPL"
        assert service._format_symbol("  MSFT  ") == "MSFT"
        assert service._format_symbol("googl") == "GOOGL"

    def test_build_url(self, test_config):
        """Test URL building"""
        service = StockService(test_config)

        base_url = "https://example.com/api"
        params = {"param1": "value1", "param2": "value2"}

        url = service._build_url(base_url, params)
        assert "param1=value1" in url
        assert "param2=value2" in url

        # Test with empty params
        url_empty = service._build_url(base_url, {})
        assert url_empty == base_url

    @patch("requests.get")
    def test_get_data_with_custom_parameters(
        self, mock_get, test_config, sample_yahoo_response
    ):
        """Test data retrieval with custom interval and period"""
        mock_response = Mock()
        mock_response.json.return_value = sample_yahoo_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        service = StockService(test_config)
        result = service.get_data("AAPL", interval="5m", period="1d")

        assert isinstance(result, pd.DataFrame)

        # Check that correct parameters were sent
        args, kwargs = mock_get.call_args
        params = kwargs.get("params", {})
        assert params["interval"] == "5m"
        assert params["period"] == "1d"
